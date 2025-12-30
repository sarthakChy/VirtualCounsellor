import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
# Import required modules
from agentic_layer.agent_orchestrator import MainOrchestrator, UserData
from config.llm_config import llm_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("school_students_workflow.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SchoolStudentWorkflowRunner:
    """Main runner for school student career exploration workflow"""

    def __init__(self, llm_model=None):
        """Initialize the workflow runner"""
        if llm_model is None:
            self.llm = llm_manager.initialize_gemini(
                model_name="gemini-1.5-flash", temperature=0.1, max_tokens=4000
            )
        else:
            self.llm = llm_model

        # Initialize orchestrator
        self.orchestrator = MainOrchestrator(llm_model=self.llm)
        logger.info("School Student Workflow Runner initialized successfully")

    def create_user_data(
        self,
        demographic_info: Optional[Dict] = None,
        dbda_scores: Optional[Dict] = None,
        cii_results: Optional[Dict] = None,
        user_id: str = None,
        session_id: str = None,
        **kwargs,
    ) -> UserData:
        """Create UserData object for the workflow"""

        if user_id is None:
            user_id = f"school_student_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        user_data: UserData = {
            "user_id": user_id,
            "session_id": session_id,
            "demographic_info": demographic_info,
            "dbda_scores": dbda_scores,
            "cii_results": cii_results,
            "resume_data": None,
            "github_profile": None,
            "linkedin_profile": None,
            "academic_status": kwargs.get("academic_status"),
            "current_profession": None,
            "financial_constraints": kwargs.get("financial_constraints"),
            "timeline_flexibility": None,
            "family_obligations": None,
        }

        # Add any additional optional data
        for key, value in kwargs.items():
            if key in user_data:
                user_data[key] = value
            else:
                logger.warning(f"Unknown user data field: {key}")

        logger.info(f"Created user data for user: {user_id}, session: {session_id}")
        return user_data

    def run_workflow(
        self, user_data_path: str, initial_message: str = None, **kwargs
    ) -> Dict[str, Any]:
        """Run the complete school student workflow"""

        try:
            logger.info("=" * 60)
            logger.info("STARTING SCHOOL STUDENT WORKFLOW")
            logger.info("=" * 60)

            # Step 1: Load user data from JSON
            logger.info("Step 1: Loading user data from JSON file")
            if not os.path.exists(user_data_path):
                raise FileNotFoundError(f"User data file not found: {user_data_path}")

            with open(user_data_path, "r") as f:
                raw_user_data = json.load(f)

            # Step 2: Create user data structure
            logger.info("Step 2: Creating user data structure")
            user_data = self.create_user_data(
                dbda_scores=raw_user_data.get("dbda_scores"),
                cii_results=raw_user_data.get("cii_results"),
                demographic_info=raw_user_data.get("demographic_info"),
                **kwargs,
            )

            # Step 3: Set default message if not provided
            if initial_message is None:
                initial_message = "I need comprehensive academic and career guidance based on my assessment results."

            # Step 4: Run the orchestrator workflow
            logger.info("Step 3: Running orchestrator workflow")
            logger.info(f"Initial message: {initial_message}")
            result = self.orchestrator.start_counseling_session(
                vertical="school_students",
                user_data=user_data,
                initial_message=initial_message,
            )

            # Step 5: Process and return results
            logger.info("Step 4: Workflow results received")
            self._save_results(result, user_data["session_id"])

            logger.info("=" * 60)
            logger.info("SCHOOL STUDENT WORKFLOW COMPLETED")
            logger.info("=" * 60)

            return result

        except Exception as e:
            logger.error(f"Error running school student workflow: {str(e)}")
            return {"success": False, "error": str(e)}

    def _save_results(self, result: Dict[str, Any], session_id: str):
        """Save workflow results to file"""
        try:
            results_dir = Path("school_students_results")
            results_dir.mkdir(exist_ok=True)

            filename = f"school_students_vertical.json"
            filepath = results_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Results saved to: {filepath}")

        except Exception as e:
            logger.warning(f"Failed to save results: {str(e)}")


if __name__ == "__main__":
    # Create a dummy user data file for testing with corrected DBDA domains and optional data
    dummy_data = {
        "demographic_info": {
            "name": "Jane Doe",
            "age": 16,
            "current_grade": "11th Grade",
            "school_name": "Amity International School, Noida, Sector-44",
        },
        "dbda_scores": {
            "administrative": 7.0,
            "entertainment": 9.2,
            "defense": 5.5,
            "sports": 8.1,
            "creative": 9.5,
            "performing": 9.0,
            "medical": 6.3,
            "technical": 8.0,
            "experimental": 8.8,
            "computational": 7.5,
            "humanitarian": 8.9,
            "educational": 7.8,
            "nature": 6.1,
            "clerical": 6.5,
        },
        "cii_results": {
            "artistic": 9,
            "scientific": 8,
            "social": 6,
            "conventional": 5,
            "enterprising": 7,
            "realistic": 6,
        },
        "academic_status": {
            "GPA": 3.8,
            "extracurriculars": ["Debate Club", "Robotics Team"],
        },
        "financial_constraints": {
            "max_annual_tuition": 15000,
            "requires_scholarship": True,
        },
    }

    data_file_path = "dummy_school_data.json"
    with open(data_file_path, "w") as f:
        json.dump(dummy_data, f, indent=4)

    runner = SchoolStudentWorkflowRunner()

    # Run the workflow
    final_result = runner.run_workflow(user_data_path=data_file_path)

    # Print a summary of the final result
    print("\n\n=== FINAL WORKFLOW SUMMARY ===")
    if final_result and final_result.get("success", True):
        print("✅ Workflow executed successfully!")

        # Access outputs from the orchestrator's final response
        final_response_data = final_result.get("final_response", {})
        summary = final_response_data.get("outputs", {}).get("fleet_summary", {})
        recommendations = summary.get("recommendations", "No recommendations found.")

        print("\n📝 Recommendations:")
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print(json.dumps(recommendations, indent=2))
    else:
        print("❌ Workflow failed.")
        print(f"Error: {final_result.get('error', 'Unknown error')}")

    # Clean up dummy data file
    os.remove(data_file_path)
