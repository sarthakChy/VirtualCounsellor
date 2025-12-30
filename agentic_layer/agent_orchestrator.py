from typing import Dict, List, Optional, Any, TypedDict, Literal
from enum import Enum
import logging
import os
from langsmith import Client, traceable
from config.langsmith_config import LangSmithConfig, initialize_langsmith
from langchain.memory import ConversationBufferWindowMemory
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agentic_layer.fleet_integrator import FleetIntegrator
from config.llm_config import llm_manager
import json
from datetime import datetime
import io
import base64
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Vertical(Enum):
    """Supported verticals in the career counseling system"""

    SCHOOL_STUDENTS = "school_students"
    COLLEGE_UPSKILLING = "college_upskilling"
    CAREER_TRANSITION = "career_transition"


class WorkflowState(TypedDict):
    """State structure for the orchestrator workflow"""

    messages: List[Dict[str, Any]]
    selected_vertical: Optional[str]
    user_data: Dict[str, Any]
    current_agent: Optional[str]
    agent_outputs: Dict[str, Any]
    conversation_context: Dict[str, Any]
    error_state: Optional[str]
    workflow_step: Optional[str]
    processing_complete: bool
    final_response: Optional[Dict[str, Any]]  # Add this explicitly


class UserData(TypedDict):
    """Structure for user input data across verticals"""

    # Common data
    user_id: str
    session_id: str
    demographic_info: Optional[Dict[str, Any]]

    # Assessment data (for school students and career transition)
    dbda_scores: Optional[Dict[str, float]]
    cii_results: Optional[Dict[str, Any]]

    # College student specific data
    resume_data: Optional[Dict[str, Any]]
    github_profile: Optional[Dict[str, Any]]
    linkedin_profile: Optional[Dict[str, Any]]
    academic_status: Optional[Dict[str, Any]]

    # Career transition specific data
    current_profession: Optional[str]
    financial_constraints: Optional[Dict[str, Any]]
    timeline_flexibility: Optional[str]
    family_obligations: Optional[Dict[str, Any]]


class VerticalValidator:
    """Handles vertical validation and data requirements"""

    def __init__(self):
        self.vertical_requirements = {
            Vertical.SCHOOL_STUDENTS: {
                "name": "School Students (Grades 9-12)",
                "description": "Career exploration and academic stream guidance for high school students",
                "required_fields": ["dbda_scores", "cii_results"],
                "optional_fields": ["demographic_info"],
                "workflow_agents": [
                    "test_score_interpreter",
                    "academic_stream_advisor",
                    "career_pathway_explorer",
                    "educational_roadmap_planner",
                    "college_scholarship_navigator",
                ],
            },
            Vertical.COLLEGE_UPSKILLING: {
                "name": "College Students (Upskilling & Career Optimization)",
                "description": "Profile analysis and career optimization for current students",
                "required_fields": ["resume_data"],
                "optional_fields": [
                    "github_profile",
                    "linkedin_profile",
                    "academic_status",
                ],
                "workflow_agents": [
                    "profile_analysis",
                    "market_intelligence",
                    "skill_development_strategist",
                    "career_optimization_planner",
                    "opportunity_matcher",
                ],
            },
            Vertical.CAREER_TRANSITION: {
                "name": "Career Transition/Switch",
                "description": "Comprehensive analysis for career change with constraints consideration",
                "required_fields": ["dbda_scores", "cii_results", "current_profession"],
                "optional_fields": [
                    "financial_constraints",
                    "timeline_flexibility",
                    "family_obligations",
                ],
                "workflow_agents": [
                    "transition_feasibility_analyzer",
                    "transferable_skills_mapper",
                    "financial_impact_calculator",
                    "alternative_pathway_designer",
                    "timeline_optimization",
                ],
            },
        }

    def get_vertical_info(self, vertical: str = None) -> Dict[str, Any]:
        """Get information about verticals"""
        if vertical:
            if vertical in [v.value for v in Vertical]:
                return self.vertical_requirements[Vertical(vertical)]
            else:
                return {"error": f"Invalid vertical: {vertical}"}

        return {v.value: info for v, info in self.vertical_requirements.items()}

    def validate_user_data(
        self, vertical: str, user_data: UserData
    ) -> tuple[bool, List[str], List[str]]:
        """Validate user data for selected vertical"""
        if vertical not in [v.value for v in Vertical]:
            return False, [f"Invalid vertical: {vertical}"], []

        vertical_enum = Vertical(vertical)
        requirements = self.vertical_requirements[vertical_enum]

        required_fields = requirements["required_fields"]
        optional_fields = requirements["optional_fields"]

        missing_required = []
        available_optional = []

        # Check required fields
        for field in required_fields:
            if field not in user_data or user_data[field] is None:
                missing_required.append(field)

        # Check available optional fields
        for field in optional_fields:
            if field in user_data and user_data[field] is not None:
                available_optional.append(field)

        is_valid = len(missing_required) == 0
        return is_valid, missing_required, available_optional


class ConversationManager:
    """Manages conversation context and memory"""

    def __init__(self):
        self.memory = ConversationBufferWindowMemory(k=10)
        self.session_contexts: Dict[str, Dict] = {}

    def initialize_session(self, session_id: str, vertical: str) -> Dict[str, Any]:
        """Initialize a new session context"""
        context = {
            "session_id": session_id,
            "vertical": vertical,
            "started_at": datetime.now().isoformat(),
            "current_step": "initialized",
            "completed_agents": [],
            "agent_outputs": {},
            "user_preferences": {},
        }

        self.session_contexts[session_id] = context
        return context

    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session context"""
        if session_id in self.session_contexts:
            self.session_contexts[session_id].update(updates)

    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Get session context"""
        return self.session_contexts.get(session_id, {})


class MainOrchestrator:
    """Main orchestration system for Virtual Career Counselor with explicit vertical selection"""

    def __init__(self, llm_model=None):
        logger.info("Initializing LangSmith configuration...")
        initialize_langsmith()

        self._setup_orchestrator_langsmith()
        if llm_model is None:
            llm_model = llm_manager.get_llm()

        self.llm_model = llm_model
        self.validator = VerticalValidator()
        self.conversation_manager = ConversationManager()

        # Agent fleet placeholders - will be implemented with actual agents
        self.agent_fleets = {
            Vertical.SCHOOL_STUDENTS: self._create_school_student_agents(),
            Vertical.COLLEGE_UPSKILLING: self._create_college_student_agents(),
            # Vertical.CAREER_TRANSITION: self._create_career_transition_agents()
        }

        # Initialize workflow
        self.workflow = self._build_workflow_graph()
        initialize_langsmith()

    def _setup_orchestrator_langsmith(self):
        """Setup orchestrator-specific LangSmith components"""
        try:
            # Create orchestrator-specific client and tracer
            self.langsmith_client = LangSmithConfig.create_client()
            self.tracer = LangSmithConfig.create_tracer("orchestrator-main")

            # Get standard config for orchestrator
            self.langsmith_config = LangSmithConfig.get_run_config(
                "main_orchestrator", tags=["orchestrator", "main_workflow"]
            )

            logger.info("Orchestrator LangSmith setup completed successfully")
        except Exception as e:
            logger.warning(f"Orchestrator LangSmith setup failed: {e}")
            self.langsmith_client = None
            self.tracer = None
            self.langsmith_config = {}

    def _build_workflow_graph(self) -> StateGraph:
        """Build the main orchestration workflow"""
        workflow = StateGraph(WorkflowState)

        # Define workflow nodes
        workflow.add_node("validate_input", self._validate_input)
        workflow.add_node("initialize_vertical", self._initialize_vertical)
        workflow.add_node("execute_vertical_workflow", self._execute_vertical_workflow)
        workflow.add_node("handle_follow_up", self._handle_follow_up)
        workflow.add_node("generate_final_response", self._generate_final_response)
        workflow.add_node("handle_error", self._handle_error)

        # Define workflow edges
        workflow.add_edge(START, "validate_input")

        workflow.add_conditional_edges(
            "validate_input",
            self._input_validation_condition,
            {
                "valid": "initialize_vertical",
                "follow_up": "handle_follow_up",
                "error": "handle_error",
            },
        )

        workflow.add_edge("initialize_vertical", "execute_vertical_workflow")
        workflow.add_edge("execute_vertical_workflow", "generate_final_response")
        workflow.add_edge("handle_follow_up", "generate_final_response")
        workflow.add_edge("generate_final_response", END)
        workflow.add_edge("handle_error", END)

        return workflow.compile(checkpointer=MemorySaver())

    def _validate_input(self, state: WorkflowState) -> WorkflowState:
        """Validate input data and vertical selection with tracing"""

        @traceable(name="validate_input_node", tags=["validation", "workflow_node"])
        def validate_with_tracing(state_data):
            logger.info("Validating input data")

            # Check if vertical is explicitly provided
            if not state.get("selected_vertical"):
                state["error_state"] = (
                    "No vertical selected. Please choose from: school_students, college_upskilling, career_transition"
                )
                state["workflow_step"] = "error"
                return state

            # Validate the selected vertical
            vertical = state["selected_vertical"]
            user_data = state.get("user_data", {})

            is_valid, missing_required, available_optional = (
                self.validator.validate_user_data(vertical, user_data)
            )

            if is_valid:
                state["workflow_step"] = "valid"
                state["conversation_context"] = {
                    "validation_status": "passed",
                    "available_optional_data": available_optional,
                    "vertical_info": self.validator.get_vertical_info(vertical),
                }
                logger.info(f"Validation passed for vertical: {vertical}")
            else:
                # Check if this might be a follow-up question from existing session
                session_id = user_data.get("session_id")
                if session_id and self.conversation_manager.get_session_context(
                    session_id
                ):
                    state["workflow_step"] = "follow_up"
                    logger.info("Treating as follow-up question from existing session")
                else:
                    state["error_state"] = (
                        f"Missing required data for {vertical}: {', '.join(missing_required)}"
                    )
                    state["workflow_step"] = "error"
                    logger.warning(f"Validation failed: missing {missing_required}")

            return state

        try:
            updated_state = validate_with_tracing(dict(state))
            state.update(updated_state)
            return state
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            state["error_state"] = f"Validation error: {str(e)}"
            state["workflow_step"] = "error"
            return state

    def _initialize_vertical(self, state: WorkflowState) -> WorkflowState:
        """Initialize vertical-specific processing"""
        vertical = state["selected_vertical"]
        user_data = state["user_data"]
        session_id = user_data.get(
            "session_id", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        logger.info(f"Initializing vertical processing: {vertical}")

        # Initialize session context
        session_context = self.conversation_manager.initialize_session(
            session_id, vertical
        )

        state["conversation_context"].update(
            {
                "session_context": session_context,
                "workflow_agents": self.validator.get_vertical_info(vertical)[
                    "workflow_agents"
                ],
                "processing_plan": self._create_processing_plan(vertical, user_data),
            }
        )

        return state

    def _execute_vertical_workflow(self, state: WorkflowState) -> WorkflowState:
        """Execute the vertical-specific agent workflow - FIXED"""
        vertical = state["selected_vertical"]
        logger.info(f"Executing workflow for vertical: {vertical}")

        # Get the agent fleet for this vertical
        agent_fleet = self.agent_fleets.get(Vertical(vertical))

        if not agent_fleet:
            logger.error(f"No agent fleet found for vertical: {vertical}")
            state["error_state"] = f"Agent fleet not available for vertical: {vertical}"
            state["processing_complete"] = False
            return state

        # Execute the workflow using the INTEGRATION LAYER
        try:
            # Use FleetIntegrator to execute and get orchestrator-compatible result
            workflow_result = FleetIntegrator.execute_workflow_for_orchestrator(
                fleet=agent_fleet,
                user_data=state["user_data"],
                conversation_context=state["conversation_context"],
            )

            # The integration layer returns orchestrator-compatible format
            state["agent_outputs"] = workflow_result["outputs"]
            state["processing_complete"] = True

            logger.info(f"Fleet execution completed successfully for {vertical}")
            logger.info(f"Agent outputs keys: {list(state['agent_outputs'].keys())}")

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            state["error_state"] = f"Processing failed: {str(e)}"
            state["processing_complete"] = False

        return state

    def _handle_follow_up(self, state: WorkflowState) -> WorkflowState:
        """Handle follow-up questions from existing sessions"""
        user_data = state["user_data"]
        session_id = user_data.get("session_id")

        logger.info(f"Handling follow-up for session: {session_id}")

        session_context = self.conversation_manager.get_session_context(session_id)

        if not session_context:
            state["error_state"] = (
                "Session not found. Please start a new counseling session."
            )
            return state

        # For now, create a simple follow-up response
        # TODO: Implement proper conversation agent
        state["agent_outputs"] = {
            "follow_up_response": "This is a follow-up question handler. Full implementation pending.",
            "session_context": session_context,
        }
        state["processing_complete"] = True

        return state

    def _generate_final_response(self, state: WorkflowState) -> WorkflowState:
        """Generate the final response for the user - FIXED VERSION"""
        logger.info("Generating final response")
        logger.info(f"State keys: {list(state.keys())}")
        logger.info(f"Agent outputs available: {bool(state.get('agent_outputs'))}")
        logger.info(f"Processing complete: {state.get('processing_complete', False)}")

        agent_outputs = state.get("agent_outputs", {})
        vertical = state.get("selected_vertical")
        session_context = state.get("conversation_context", {}).get(
            "session_context", {}
        )
        error_state = state.get("error_state")

        # Handle error case first
        if error_state:
            logger.warning(f"Generating error response: {error_state}")
            response = {
                "success": False,
                "error": error_state,
                "vertical_options": self.validator.get_vertical_info(),
                "suggested_actions": self._get_error_suggestions(error_state),
                "timestamp": datetime.now().isoformat(),
            }
            state["final_response"] = response
            logger.info("Error response generated successfully")
            return state

        # Check if we have valid outputs
        if not agent_outputs:
            logger.warning("No agent outputs available for response generation")
            response = {
                "success": False,
                "error": "No analysis results available",
                "timestamp": datetime.now().isoformat(),
                "debug_info": {
                    "processing_complete": state.get("processing_complete", False),
                    "vertical": vertical,
                    "session_context_available": bool(session_context),
                },
            }
            state["final_response"] = response
            logger.info("Empty outputs response generated")
            return state

        # Generate successful response
        try:
            response = {
                "success": True,
                "vertical": vertical,
                "session_id": session_context.get("session_id"),
                "timestamp": datetime.now().isoformat(),
                "outputs": agent_outputs,
                "summary": self._generate_response_summary(agent_outputs, vertical),
                "next_actions": self._suggest_next_actions(agent_outputs, vertical),
                "conversation_context": {
                    "can_ask_follow_up": True,
                    "vertical_workflow_complete": state.get(
                        "processing_complete", False
                    ),
                },
            }

            state["final_response"] = response
            logger.info("Successful final response generated")
            logger.info(f"Response has outputs: {bool(response.get('outputs'))}")
            return state

        except Exception as e:
            logger.error(f"Error generating successful response: {e}", exc_info=True)
            # Fallback error response
            response = {
                "success": False,
                "error": f"Failed to generate response: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }
            state["final_response"] = response
            return state

    def _handle_error(self, state: WorkflowState) -> WorkflowState:
        """Handle errors in the workflow"""
        error = state.get("error_state", "Unknown error occurred")
        logger.error(f"Handling error: {error}")

        response = {
            "success": False,
            "error": error,
            "vertical_options": self.validator.get_vertical_info(),
            "suggested_actions": self._get_error_suggestions(error),
            "timestamp": datetime.now().isoformat(),
        }

        state["final_response"] = response
        return state

    def _input_validation_condition(self, state: WorkflowState) -> str:
        """Determine the next step based on input validation"""
        return state.get("workflow_step", "error")

    def _create_processing_plan(
        self, vertical: str, user_data: UserData
    ) -> Dict[str, Any]:
        """Create a processing plan based on available data"""
        vertical_info = self.validator.get_vertical_info(vertical)
        agents = vertical_info["workflow_agents"]

        # Determine which agents can run based on available data
        available_data = [k for k, v in user_data.items() if v is not None]

        return {
            "planned_agents": agents,
            "available_data": available_data,
            "estimated_duration": f"{len(agents) * 2} minutes",
            "processing_order": agents,
        }

    def _generate_response_summary(
        self, agent_outputs: Dict[str, Any], vertical: str
    ) -> str:
        """Generate a summary of the analysis"""
        if not agent_outputs:
            return "Analysis could not be completed due to missing data."

        summaries = {
            "school_students": "Comprehensive career exploration analysis completed for high school student.",
            "college_upskilling": "Profile analysis and career optimization strategy developed.",
            "career_transition": "Career transition feasibility and planning analysis completed.",
        }

        return summaries.get(vertical, "Career counseling analysis completed.")

    def _suggest_next_actions(
        self, agent_outputs: Dict[str, Any], vertical: str
    ) -> List[str]:
        """Suggest next actions based on the analysis"""
        base_actions = [
            "Review the detailed recommendations provided",
            "Ask follow-up questions for clarification",
            "Save this analysis for future reference",
        ]

        vertical_actions = {
            "school_students": [
                "Discuss findings with parents/guardians",
                "Meet with school counselor",
                "Research recommended colleges and courses",
            ],
            "college_upskilling": [
                "Update your resume and LinkedIn profile",
                "Start working on recommended skill development",
                "Begin networking in target industries",
            ],
            "career_transition": [
                "Create a detailed transition timeline",
                "Start building skills for target career",
                "Assess financial preparation needs",
            ],
        }

        return base_actions + vertical_actions.get(vertical, [])

    def _get_error_suggestions(self, error: str) -> List[str]:
        """Get suggestions based on error type"""
        if "Missing required data" in error:
            return [
                "Please provide all required assessment data",
                "Complete the necessary tests/evaluations",
                "Contact support if you need help gathering data",
            ]
        elif "No vertical selected" in error:
            return [
                "Choose School Students for grades 9-12 guidance",
                "Choose College Upskilling for current students",
                "Choose Career Transition for career change analysis",
            ]
        else:
            return [
                "Try again with complete information",
                "Contact technical support if the problem persists",
            ]

    def _create_school_student_agents(self):
        """Create school student agent fleet"""
        return FleetIntegrator.create_school_student_fleet(self.llm_model)

    def _create_college_student_agents(self):
        """Create college student agent fleet"""
        return FleetIntegrator.create_college_fleet(self.llm_model)

    # Public interface methods
    def start_counseling_session(
        self, vertical: str, user_data: UserData, initial_message: str = None
    ) -> Dict[str, Any]:
        """Start a new counseling session"""
        config = {
            "configurable": {
                "thread_id": user_data.get(
                    "session_id", f"thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
            },
            "callbacks": [self.tracer] if self.tracer else [],
        }
        if self.langsmith_client:
            try:
                run_id = self.langsmith_client.create_run(
                    name="career_counseling_session",
                    run_type="chain",
                    inputs={
                        "vertical": vertical,
                        "user_id": user_data.get("user_id", "unknown"),
                        "session_id": user_data.get("session_id", "unknown"),
                    },
                    tags=["orchestrator", "main_workflow", vertical],
                )
                config["run_id"] = run_id
                logger.info(f"Created LangSmith run: {run_id}")
            except Exception as e:
                logger.error(f"Failed to create LangSmith run: {e}")

        messages = []
        if initial_message:
            messages.append({"role": "user", "content": initial_message})

        initial_state: WorkflowState = {
            "messages": messages,
            "selected_vertical": vertical,
            "user_data": user_data,
            "current_agent": None,
            "agent_outputs": {},
            "conversation_context": {},
            "error_state": None,
            "workflow_step": None,
            "processing_complete": False,
            "final_response": None,  # Initialize this explicitly
        }

        try:
            logger.info(f"Starting workflow execution for vertical: {vertical}")
            result = self.workflow.invoke(initial_state, config=config)
            logger.info("Workflow execution completed")
            logger.info(f"Result keys: {list(result.keys())}")
            logger.info(f"Final response present: {bool(result.get('final_response'))}")

            # Log successful completion to LangSmith
            if self.langsmith_client and config.get("run_id"):
                self.langsmith_client.update_run(
                    config["run_id"],
                    outputs={
                        "success": result.get("final_response", {}).get(
                            "success", False
                        )
                    },
                    end_time=datetime.now(),
                )

            final_response = result.get("final_response")
            if not final_response:
                logger.error("No final_response in workflow result")
                logger.error(f"Available result keys: {list(result.keys())}")
                # Let's check what we actually have in the result
                for key, value in result.items():
                    if isinstance(value, dict):
                        logger.error(f"Result[{key}] keys: {list(value.keys())}")

                return {
                    "success": False,
                    "error": "Workflow completed but no final response generated",
                    "timestamp": datetime.now().isoformat(),
                    "debug_info": {
                        "result_keys": list(result.keys()),
                        "processing_complete": result.get("processing_complete", False),
                        "agent_outputs_available": bool(result.get("agent_outputs")),
                        "error_state": result.get("error_state"),
                    },
                }

            logger.info("Final response successfully retrieved")
            return final_response

        except Exception as e:
            # Log errors to LangSmith
            if self.langsmith_client and config.get("run_id"):
                self.langsmith_client.update_run(
                    config["run_id"], error=str(e), end_time=datetime.now()
                )

            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": f"System error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }

    def ask_follow_up_question(
        self, session_id: str, question: str, user_id: str = None
    ) -> Dict[str, Any]:
        """Handle follow-up questions in existing session"""

        user_data = {"session_id": session_id, "user_id": user_id or "default_user"}

        messages = [{"role": "user", "content": question}]

        initial_state: WorkflowState = {
            "messages": messages,
            "selected_vertical": None,  # Will be determined from session
            "user_data": user_data,
            "current_agent": None,
            "agent_outputs": {},
            "conversation_context": {},
            "error_state": None,
            "workflow_step": None,
            "processing_complete": False,
            "final_response": None,
        }

        try:
            config = {"configurable": {"thread_id": session_id}}
            result = self.workflow.invoke(initial_state, config=config)
            return result.get("final_response", {"error": "No response generated"})
        except Exception as e:
            logger.error(f"Follow-up processing failed: {str(e)}")
            return {
                "success": False,
                "error": f"System error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }

    def get_available_verticals(self) -> Dict[str, Any]:
        """Get information about available verticals"""
        return self.validator.get_vertical_info()
