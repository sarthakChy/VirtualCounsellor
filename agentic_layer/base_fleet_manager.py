from typing import Dict, List, Any, Optional, TypedDict
from enum import Enum
import logging
from datetime import datetime
import json
from abc import ABC, abstractmethod
from config.agent_config import (
    AgentDependency,
    AgentResult,
    AgentInput,
    FleetExecutionStrategy,
    FleetResult,
    FleetStatus,
    ProcessingStatus,
)
from agentic_layer.base_agent import BaseAgent
from langsmith import Client, traceable
from langchain_core.tracers.langchain import LangChainTracer
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseFleetManager(ABC):
    """Base class for agent fleet managers"""

    def __init__(self, fleet_id: str, fleet_name: str, llm_model=None):
        self.fleet_id = fleet_id
        self.fleet_name = fleet_name
        self.llm_model = llm_model
        self.logger = logging.getLogger(f"fleet.{fleet_id}")

        # Fleet components
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_dependencies: Dict[str, AgentDependency] = {}
        self.execution_strategy = FleetExecutionStrategy.SEQUENTIAL

        # Execution state
        self.execution_start_time = None
        self.execution_history: List[Dict[str, Any]] = []

        # Initialize fleet-specific components
        self._initialize_fleet()
        self._setup_fleet_tracing()

    def _setup_fleet_tracing(self):
        """Setup LangSmith tracing for this fleet"""
        try:
            os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
            os.environ.setdefault("LANGCHAIN_PROJECT", f"fleet-{self.fleet_id}")

            self.langsmith_client = Client()
            self.tracer = LangChainTracer(project_name=f"fleet-{self.fleet_id}")

            self.logger.info(
                f"LangSmith tracing initialized for fleet: {self.fleet_id}"
            )
        except Exception as e:
            self.logger.warning(
                f"LangSmith setup failed for fleet {self.fleet_id}: {e}"
            )
            self.langsmith_client = None
            self.tracer = None

    @abstractmethod
    def _initialize_fleet(self):
        """Initialize fleet-specific agents and dependencies"""
        pass

    @abstractmethod
    def _validate_fleet_input(
        self, user_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """Validate input data for this fleet"""
        pass

    @abstractmethod
    def _create_execution_plan(self, user_data: Dict[str, Any]) -> List[str]:
        """Create execution plan based on available data"""
        pass

    @abstractmethod
    def _generate_fleet_recommendations(
        self, agent_results: Dict[str, AgentResult]
    ) -> List[str]:
        """Generate overall recommendations from agent results"""
        pass

    def add_agent(self, agent: BaseAgent, dependencies: AgentDependency = None):
        """Add an agent to the fleet"""
        self.agents[agent.agent_id] = agent
        if dependencies:
            self.agent_dependencies[agent.agent_id] = dependencies
        self.logger.info(f"Added agent: {agent.agent_name}")

    @traceable(name="fleet_execution", tags=["fleet", "workflow"])
    def execute_workflow(
        self, user_data: Dict[str, Any], conversation_context: Dict[str, Any] = None
    ) -> FleetResult:
        """Execute the complete agent fleet workflow with tracing"""
        self.execution_start_time = datetime.now()

        # Create fleet run metadata
        fleet_metadata = {
            "fleet_id": self.fleet_id,
            "fleet_name": self.fleet_name,
            "agent_count": len(self.agents),
            "user_data_keys": list(user_data.keys()) if user_data else [],
        }

        fleet_run_id = None
        if self.langsmith_client:
            try:
                fleet_run_id = self.langsmith_client.create_run(
                    name=f"fleet_execution_{self.fleet_id}",
                    run_type="chain",
                    inputs=fleet_metadata,
                    tags=["fleet_execution", self.fleet_id],
                )
                self.logger.info(f"Created fleet LangSmith run: {fleet_run_id}")
            except Exception as e:
                self.logger.error(f"Failed to create fleet LangSmith run: {e}")

        try:
            # Validate input with tracing
            is_valid, missing_data = self._validate_fleet_input_with_tracing(user_data)
            if not is_valid:
                result = self._create_failed_result(
                    f"Missing required data: {', '.join(missing_data)}"
                )
                self._log_fleet_to_langsmith(
                    fleet_run_id, result, error=result.metadata.get("failure_reason")
                )
                return result

            # Create execution plan with tracing
            execution_plan = self._create_execution_plan_with_tracing(user_data)

            # Execute agents with tracing
            agent_results = self._execute_agents_with_tracing(
                execution_plan, user_data, conversation_context or {}, fleet_run_id
            )

            # Calculate metrics and create result
            total_time = (datetime.now() - self.execution_start_time).total_seconds()
            overall_confidence = self._calculate_fleet_confidence(agent_results)
            recommendations = self._generate_fleet_recommendations(agent_results)
            next_actions = self._generate_next_actions(agent_results)
            fleet_status = self._determine_fleet_status(agent_results)

            result = FleetResult(
                fleet_id=self.fleet_id,
                fleet_name=self.fleet_name,
                status=fleet_status,
                agent_results=agent_results,
                execution_summary=self._create_execution_summary(agent_results),
                overall_confidence=overall_confidence,
                total_processing_time=total_time,
                recommendations=recommendations,
                next_actions=next_actions,
                metadata={
                    "execution_plan": execution_plan,
                    "successful_agents": [
                        aid
                        for aid, result in agent_results.items()
                        if result.status == ProcessingStatus.COMPLETED
                    ],
                    "failed_agents": [
                        aid
                        for aid, result in agent_results.items()
                        if result.status == ProcessingStatus.FAILED
                    ],
                    "execution_timestamp": self.execution_start_time.isoformat(),
                },
            )

            self._log_fleet_to_langsmith(fleet_run_id, result)
            self._update_execution_history(result)
            return result

        except Exception as e:
            self.logger.error(f"Fleet execution failed: {str(e)}", exc_info=True)
            result = self._create_failed_result(f"Fleet execution error: {str(e)}")
            self._log_fleet_to_langsmith(fleet_run_id, result, error=str(e))
            return result

    @traceable(name="agents_execution", tags=["agents", "fleet"])
    def _execute_agents_with_tracing(
        self,
        execution_plan: List[str],
        user_data: Dict[str, Any],
        conversation_context: Dict[str, Any],
        parent_run_id: str,
    ) -> Dict[str, AgentResult]:
        """Execute agents with enhanced tracing"""
        agent_results = {}
        previous_outputs = {}

        for i, agent_id in enumerate(execution_plan):
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found in fleet")
                continue

            agent = self.agents[agent_id]

            # Create agent-specific run as child of fleet run
            agent_run_id = None
            if self.langsmith_client and parent_run_id:
                try:
                    agent_run_id = self.langsmith_client.create_run(
                        name=f"agent_{agent_id}",
                        run_type="tool",
                        inputs={
                            "agent_id": agent_id,
                            "agent_name": agent.agent_name,
                            "execution_order": i + 1,
                            "dependencies_met": True,  # Could add dependency checking here
                        },
                        parent_run_id=parent_run_id,
                        tags=["agent_execution", agent_id, self.fleet_id],
                    )
                except Exception as e:
                    self.logger.error(f"Failed to create agent run: {e}")

            self.logger.info(
                f"Executing agent: {agent.agent_name} (run: {agent_run_id})"
            )

            # Prepare agent input
            agent_input = AgentInput(
                user_data=user_data,
                conversation_context=conversation_context,
                previous_agent_outputs=previous_outputs.copy(),
                session_metadata={
                    "fleet_id": self.fleet_id,
                    "execution_order": i + 1,
                    "parent_run_id": parent_run_id,
                    "agent_run_id": agent_run_id,
                },
            )

            # Execute agent
            result = agent.execute(agent_input)
            agent_results[agent_id] = result

            # Log agent completion to fleet run
            if self.langsmith_client and agent_run_id:
                try:
                    agent_outputs = {
                        "status": result.status.value,
                        "confidence": result.confidence_score,
                        "processing_time": result.processing_time,
                        "output_size": (
                            len(result.output_data) if result.output_data else 0
                        ),
                    }

                    if result.status == ProcessingStatus.FAILED:
                        self.langsmith_client.update_run(
                            agent_run_id,
                            outputs=agent_outputs,
                            error=result.error_message or "Agent execution failed",
                            end_time=datetime.now(),
                        )
                    else:
                        self.langsmith_client.update_run(
                            agent_run_id, outputs=agent_outputs, end_time=datetime.now()
                        )
                except Exception as e:
                    self.logger.error(f"Failed to update agent run: {e}")

            # Add successful outputs to previous_outputs for next agents
            if result.status == ProcessingStatus.COMPLETED:
                previous_outputs[agent_id] = result

            self.logger.info(
                f"Agent {agent_id} completed with status: {result.status.value}"
            )

        return agent_results

    def _log_fleet_to_langsmith(
        self, run_id: str, result: FleetResult, error: str = None
    ):
        """Log fleet execution results to LangSmith"""
        if not self.langsmith_client or not run_id:
            return

        try:
            outputs = {
                "fleet_status": result.status.value,
                "overall_confidence": result.overall_confidence,
                "total_processing_time": result.total_processing_time,
                "successful_agents": len(
                    [
                        r
                        for r in result.agent_results.values()
                        if r.status == ProcessingStatus.COMPLETED
                    ]
                ),
                "failed_agents": len(
                    [
                        r
                        for r in result.agent_results.values()
                        if r.status == ProcessingStatus.FAILED
                    ]
                ),
                "recommendations_count": len(result.recommendations),
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
            self.logger.error(f"Failed to log fleet to LangSmith: {e}")

    def _calculate_fleet_confidence(
        self, agent_results: Dict[str, AgentResult]
    ) -> float:
        """Calculate overall fleet confidence score"""
        if not agent_results:
            return 0.0

        completed_results = [
            r for r in agent_results.values() if r.status == ProcessingStatus.COMPLETED
        ]

        if not completed_results:
            return 0.0

        avg_confidence = sum(r.confidence_score for r in completed_results) / len(
            completed_results
        )
        completion_rate = len(completed_results) / len(agent_results)

        return round(avg_confidence * completion_rate, 2)

    def _determine_fleet_status(
        self, agent_results: Dict[str, AgentResult]
    ) -> FleetStatus:
        """Determine overall fleet execution status"""
        if not agent_results:
            return FleetStatus.FAILED

        completed = sum(
            1 for r in agent_results.values() if r.status == ProcessingStatus.COMPLETED
        )
        total = len(agent_results)

        if completed == total:
            return FleetStatus.COMPLETED
        elif completed > total / 2:
            return FleetStatus.PARTIALLY_COMPLETED
        else:
            return FleetStatus.FAILED

    def _create_execution_summary(
        self, agent_results: Dict[str, AgentResult]
    ) -> Dict[str, Any]:
        """Create execution summary"""
        return {
            "total_agents": len(agent_results),
            "successful_agents": sum(
                1
                for r in agent_results.values()
                if r.status == ProcessingStatus.COMPLETED
            ),
            "failed_agents": sum(
                1 for r in agent_results.values() if r.status == ProcessingStatus.FAILED
            ),
            "avg_processing_time": sum(
                r.processing_time for r in agent_results.values()
            )
            / len(agent_results),
            "total_warnings": sum(len(r.warnings) for r in agent_results.values()),
        }

    def _generate_next_actions(
        self, agent_results: Dict[str, AgentResult]
    ) -> List[str]:
        """Generate next actions based on agent results"""
        return [
            "Review the detailed analysis and recommendations",
            "Ask follow-up questions for clarification",
            "Begin implementing suggested improvements",
        ]

    def _create_failed_result(self, error_message: str) -> FleetResult:
        """Create a failed fleet result"""
        total_time = 0
        if self.execution_start_time:
            total_time = (datetime.now() - self.execution_start_time).total_seconds()

        return FleetResult(
            fleet_id=self.fleet_id,
            fleet_name=self.fleet_name,
            status=FleetStatus.FAILED,
            agent_results={},
            execution_summary={"error": error_message},
            overall_confidence=0.0,
            total_processing_time=total_time,
            recommendations=[],
            next_actions=["Please provide required data and try again"],
            metadata={
                "failure_reason": error_message,
                "timestamp": datetime.now().isoformat(),
            },
        )

    def _update_execution_history(self, result: FleetResult):
        """Update execution history"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": result.status.value,
            "confidence": result.overall_confidence,
            "processing_time": result.total_processing_time,
            "successful_agents": len(
                [
                    r
                    for r in result.agent_results.values()
                    if r.status == ProcessingStatus.COMPLETED
                ]
            ),
        }

        self.execution_history.append(history_entry)
        if len(self.execution_history) > 10:
            self.execution_history = self.execution_history[-10:]

    @traceable(name="fleet_input_validation", tags=["validation", "fleet"])
    def _validate_fleet_input_with_tracing(self, user_data: Dict[str, Any]):
        """Validate fleet input with tracing"""
        return self._validate_fleet_input(user_data)

    @traceable(name="execution_planning", tags=["planning", "fleet"])
    def _create_execution_plan_with_tracing(self, user_data: Dict[str, Any]):
        """Create execution plan with tracing"""
        return self._create_execution_plan(user_data)
