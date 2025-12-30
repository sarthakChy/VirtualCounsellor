from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging
from datetime import datetime
import os
from dataclasses import dataclass
from langsmith import Client, traceable
from langchain_core.tracers.langchain import LangChainTracer
from config.agent_config import AgentType, AgentInput, AgentResult, ProcessingStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all agents in the Virtual Career Counselor system.
    Provides common functionality and enforces interface consistency.
    """

    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: AgentType,
        llm_model=None,
        config: Dict[str, Any] = None,
    ):
        """
        Initialize base agent

        Args:
            agent_id: Unique identifier for the agent
            agent_name: Human-readable name for the agent
            agent_type: Type of agent (vertical_specific, shared, utility)
            llm_model: Language model instance
            config: Agent-specific configuration
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.llm_model = llm_model
        self.config = config or {}

        # Initialize logging for this agent
        self.logger = logging.getLogger(f"agent.{agent_id}")

        # Processing metadata
        self.processing_start_time = None
        self.processing_history: List[Dict[str, Any]] = []

        # Agent capabilities and requirements
        self.required_inputs = self._define_required_inputs()
        self.optional_inputs = self._define_optional_inputs()
        self.output_schema = self._define_output_schema()

        # Initialize agent-specific components
        self._initialize_agent()
        self._setup_langsmith_tracing()

    def _setup_langsmith_tracing(self):
        """Setup LangSmith tracing for this agent"""
        try:
            # Ensure environment variables are set
            os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
            os.environ.setdefault("LANGCHAIN_PROJECT", f"agent-{self.agent_id}")

            # Initialize LangSmith client
            self.langsmith_client = Client()
            self.tracer = LangChainTracer(project_name=f"agent-{self.agent_id}")

            self.logger.info(
                f"LangSmith tracing initialized for agent: {self.agent_id}"
            )
        except Exception as e:
            self.logger.warning(
                f"LangSmith setup failed for agent {self.agent_id}: {e}"
            )
            self.langsmith_client = None
            self.tracer = None

    @abstractmethod
    def _define_required_inputs(self) -> List[str]:
        """Define required inputs for this agent"""
        pass

    @abstractmethod
    def _define_optional_inputs(self) -> List[str]:
        """Define optional inputs that can enhance processing"""
        pass

    @abstractmethod
    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of this agent's output"""
        pass

    @abstractmethod
    def _initialize_agent(self):
        """Initialize agent-specific components (prompts, parsers, etc.)"""
        pass

    @abstractmethod
    def _process_core_logic(self, validated_input: AgentInput) -> Dict[str, Any]:
        """
        Core processing logic - must be implemented by each agent

        Args:
            validated_input: Validated input data

        Returns:
            Dict containing the agent's analysis/output
        """
        pass

    def validate_input(
        self, agent_input: AgentInput
    ) -> tuple[bool, List[str], Dict[str, Any]]:
        """
        Validate input data for this agent

        Returns:
            Tuple of (is_valid, missing_requirements, validated_data)
        """
        user_data = agent_input.get("user_data", {})
        missing_requirements = []

        # Check required inputs
        for required_field in self.required_inputs:
            if not self._check_field_availability(required_field, user_data):
                missing_requirements.append(required_field)

        # Collect available optional inputs
        available_optional = {}
        for optional_field in self.optional_inputs:
            if self._check_field_availability(optional_field, user_data):
                available_optional[optional_field] = self._extract_field_data(
                    optional_field, user_data
                )

        is_valid = len(missing_requirements) == 0

        validated_data = {
            "required_data": {
                field: self._extract_field_data(field, user_data)
                for field in self.required_inputs
                if field not in missing_requirements
            },
            "optional_data": available_optional,
            "context_data": agent_input.get("conversation_context", {}),
            "previous_outputs": agent_input.get("previous_agent_outputs", {}),
            "session_metadata": agent_input.get("session_metadata", {}),
        }

        return is_valid, missing_requirements, validated_data

    def _check_field_availability(
        self, field_name: str, user_data: Dict[str, Any]
    ) -> bool:
        """Check if a field is available and not None/empty"""
        if field_name in user_data:
            value = user_data[field_name]
            if value is not None:
                # Additional checks for different data types
                if isinstance(value, (list, dict, str)) and len(value) == 0:
                    return False
                return True
        return False

    def _extract_field_data(self, field_name: str, user_data: Dict[str, Any]) -> Any:
        """Extract field data with optional preprocessing"""
        return user_data.get(field_name)

    @traceable(name="agent_execution", tags=["agent", "main_execution"])
    def execute(self, agent_input: AgentInput) -> AgentResult:
        """Main execution method with tracing"""
        self.processing_start_time = datetime.now()

        # Create run metadata
        run_metadata = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type.value,
            "input_keys": list(agent_input.keys()) if agent_input else [],
        }

        if self.langsmith_client:
            try:
                run_id = self.langsmith_client.create_run(
                    name=f"execute_{self.agent_id}",
                    run_type="chain",
                    inputs=run_metadata,
                    tags=["agent_execution", self.agent_id, self.agent_type.value],
                )
                self.logger.info(
                    f"Created LangSmith run: {run_id} for agent: {self.agent_id}"
                )
            except Exception as e:
                self.logger.error(f"Failed to create LangSmith run: {e}")
                run_id = None
        else:
            run_id = None

        try:
            # Validate input with tracing
            is_valid, missing_requirements, validated_data = (
                self._validate_input_with_tracing(agent_input)
            )

            if not is_valid:
                result = self._create_failed_result(
                    f"Missing required inputs: {', '.join(missing_requirements)}"
                )
                self._log_to_langsmith(run_id, result, error=result.error_message)
                return result

            # Execute core processing logic with tracing
            output_data = self._process_core_logic_with_tracing(validated_data)

            # Calculate processing metrics
            processing_time = (
                datetime.now() - self.processing_start_time
            ).total_seconds()
            confidence_score = self._calculate_confidence_score(
                validated_data, output_data
            )

            # Create successful result
            result = AgentResult(
                agent_id=self.agent_id,
                agent_name=self.agent_name,
                status=ProcessingStatus.COMPLETED,
                output_data=output_data,
                confidence_score=confidence_score,
                processing_time=processing_time,
                metadata={
                    "input_summary": self._create_input_summary(validated_data),
                    "processing_notes": getattr(self, "_processing_notes", []),
                    "data_quality_assessment": self._assess_data_quality(
                        validated_data
                    ),
                },
            )

            self._log_to_langsmith(run_id, result)
            self._update_processing_history(result)

            return result

        except Exception as e:
            self.logger.error(f"Error in {self.agent_name}: {str(e)}", exc_info=True)
            result = self._create_failed_result(f"Processing error: {str(e)}")
            self._log_to_langsmith(run_id, result, error=str(e))
            return result

    def _create_failed_result(self, error_message: str) -> AgentResult:
        """Create a failed result with error information"""
        processing_time = 0
        if self.processing_start_time:
            processing_time = (
                datetime.now() - self.processing_start_time
            ).total_seconds()

        return AgentResult(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            status=ProcessingStatus.FAILED,
            output_data={},
            confidence_score=0.0,
            processing_time=processing_time,
            error_message=error_message,
            metadata={"failure_timestamp": datetime.now().isoformat()},
        )

    def _calculate_confidence_score(
        self, validated_data: Dict[str, Any], output_data: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score based on data availability and processing success
        Override in subclasses for more sophisticated confidence calculation
        """
        base_confidence = 0.7  # Base confidence for successful processing

        # Boost confidence based on optional data availability
        optional_boost = len(validated_data.get("optional_data", {})) * 0.05

        # Boost confidence based on output completeness
        output_completeness = len(output_data) / max(len(self.output_schema), 1)
        completeness_boost = output_completeness * 0.2

        total_confidence = min(
            1.0, base_confidence + optional_boost + completeness_boost
        )
        return round(total_confidence, 2)

    def _create_input_summary(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of input data for metadata"""
        return {
            "required_fields_count": len(validated_data.get("required_data", {})),
            "optional_fields_count": len(validated_data.get("optional_data", {})),
            "has_previous_outputs": len(validated_data.get("previous_outputs", {})) > 0,
            "context_available": len(validated_data.get("context_data", {})) > 0,
        }

    def _assess_data_quality(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the quality of input data
        Override in subclasses for specific data quality checks
        """
        return {
            "overall_quality": "good",  # good/fair/poor
            "data_completeness": len(validated_data.get("required_data", {}))
            / max(len(self.required_inputs), 1),
            "quality_notes": [],
        }

    def _update_processing_history(self, result: AgentResult):
        """Update processing history for this agent"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": result.status.value,
            "confidence": result.confidence_score,
            "processing_time": result.processing_time,
            "output_keys": (
                list(result.output_data.keys()) if result.output_data else []
            ),
        }

        self.processing_history.append(history_entry)

        # Keep only last 10 entries
        if len(self.processing_history) > 10:
            self.processing_history = self.processing_history[-10:]

    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type.value,
            "required_inputs": self.required_inputs,
            "optional_inputs": self.optional_inputs,
            "output_schema": self.output_schema,
            "processing_history_count": len(self.processing_history),
            "config": self.config,
        }

    def can_process(self, user_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Check if this agent can process given user data

        Returns:
            Tuple of (can_process, missing_requirements)
        """
        missing = []
        for required_field in self.required_inputs:
            if not self._check_field_availability(required_field, user_data):
                missing.append(required_field)

        return len(missing) == 0, missing

    # Utility methods for subclasses
    def _create_system_prompt(
        self, role_description: str, context_info: str = ""
    ) -> str:
        """Helper to create system prompts"""
        base_prompt = f"""You are a {role_description} in a Virtual Career Counselor system.

Agent Information:
- Agent ID: {self.agent_id}
- Agent Name: {self.agent_name}
- Specialization: {role_description}

{context_info}

Guidelines:
- Provide evidence-based, actionable insights
- Be supportive and encouraging while being realistic
- Consider cultural context and Indian education/career landscape
- Structure your output clearly and professionally
- Acknowledge limitations and suggest next steps when appropriate
"""
        return base_prompt

    def _format_assessment_scores(self, scores: Dict[str, Any]) -> str:
        """Helper to format assessment scores for prompts"""
        if not scores:
            return "No assessment scores available"

        formatted_scores = []
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                formatted_scores.append(f"- {key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, dict):
                formatted_scores.append(f"- {key.replace('_', ' ').title()}:")
                for subkey, subvalue in value.items():
                    formatted_scores.append(
                        f"  - {subkey.replace('_', ' ').title()}: {subvalue}"
                    )

        return "\n".join(formatted_scores)

    def _add_processing_note(self, note: str):
        """Add a processing note for metadata"""
        if not hasattr(self, "_processing_notes"):
            self._processing_notes = []
        self._processing_notes.append(
            {"timestamp": datetime.now().isoformat(), "note": note}
        )

    def reset_processing_state(self):
        """Reset processing state for reuse"""
        self.processing_start_time = None
        self._processing_notes = []

    @traceable(name="input_validation", tags=["validation"])
    def _validate_input_with_tracing(self, agent_input: AgentInput):
        """Validate input with tracing"""
        return self.validate_input(agent_input)

    @traceable(name="core_processing", tags=["processing"])
    def _process_core_logic_with_tracing(self, validated_data: Dict[str, Any]):
        """Process core logic with tracing"""
        return self._process_core_logic(validated_data)

    def _log_to_langsmith(self, run_id: str, result: AgentResult, error: str = None):
        """Log execution results to LangSmith"""
        if not self.langsmith_client or not run_id:
            return

        try:
            outputs = {
                "status": result.status.value,
                "confidence_score": result.confidence_score,
                "processing_time": result.processing_time,
                "output_keys": (
                    list(result.output_data.keys()) if result.output_data else []
                ),
            }

            if error:
                self.langsmith_client.update_run(
                    run_id, outputs=outputs, error=error, end_time=datetime.now()
                )
            else:
                self.langsmith_client.update_run(
                    run_id, outputs=outputs, end_time=datetime.now()
                )
        except Exception as e:
            self.logger.error(f"Failed to log to LangSmith: {e}")
