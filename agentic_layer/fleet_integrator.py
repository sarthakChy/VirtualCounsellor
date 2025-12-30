from typing import Dict, Any
from agentic_layer.base_fleet_manager import BaseFleetManager
from agentic_layer.college_upskill.college_student_fleet_manager import (
    CollegeStudentFleetManager,
)
from agentic_layer.school_students.school_student_fleet_manager import (
    SchoolStudentFleetManager,
)


class FleetIntegrator:
    """Helper class for integrating fleet managers with the main orchestrator"""

    @staticmethod
    def create_college_fleet(llm_model=None) -> CollegeStudentFleetManager:
        """Create and return configured college student fleet"""
        fleet = CollegeStudentFleetManager(llm_model)
        return fleet

    @staticmethod
    def create_school_student_fleet(llm_model=None) -> SchoolStudentFleetManager:
        """Create and return configured school student fleet"""
        fleet = SchoolStudentFleetManager(llm_model)
        return fleet

    @staticmethod
    def execute_workflow_for_orchestrator(
        fleet: BaseFleetManager,
        user_data: Dict[str, Any],
        conversation_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute fleet workflow and return orchestrator-compatible result"""
        fleet_result = fleet.execute_workflow(user_data, conversation_context)

        # Convert FleetResult to orchestrator-expected format
        return {
            "completed_agents": list(fleet_result.agent_results.keys()),
            "outputs": {
                "fleet_summary": {
                    "status": fleet_result.status.value,
                    "confidence": fleet_result.overall_confidence,
                    "processing_time": fleet_result.total_processing_time,
                    "recommendations": fleet_result.recommendations,
                    "next_actions": fleet_result.next_actions,
                },
                "agent_outputs": {
                    agent_id: {
                        "status": result.status.value,
                        "confidence": result.confidence_score,
                        "data": result.output_data,
                        "warnings": result.warnings,
                    }
                    for agent_id, result in fleet_result.agent_results.items()
                },
            },
            "execution_metadata": fleet_result.metadata,
        }
