import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import required modules
from langchain_community.document_loaders import PyMuPDFLoader
from agentic_layer.agent_orchestrator import MainOrchestrator, UserData
from config.llm_config import llm_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("college_workflow.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class CollegeWorkflowRunner:
    """Main runner for college skills workflow"""

    def __init__(self, llm_model=None):
        """Initialize the workflow runner"""
        if llm_model is None:
            # Initialize LLM - adjust model name and parameters as needed
            self.llm = llm_manager.initialize_gemini(
                model_name="gemini-2.5-flash", temperature=0.1, max_tokens=4000
            )
        else:
            self.llm = llm_model

        # Initialize orchestrator
        self.orchestrator = MainOrchestrator(llm_model=self.llm)
        logger.info("College Workflow Runner initialized successfully")

    def load_resume_from_pdf(self, pdf_path: str) -> str:
        """Load and extract text content from PDF resume"""
        try:
            logger.info(f"Loading resume from: {pdf_path}")

            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Resume file not found: {pdf_path}")

            loader = PyMuPDFLoader(pdf_path)
            pages = loader.load()
            content = "\n\n".join([page.page_content for page in pages])

            if not content.strip():
                raise ValueError("No content extracted from PDF")

            logger.info(f"Successfully extracted {len(content)} characters from resume")
            return content

        except Exception as e:
            logger.error(f"Error loading resume: {str(e)}")
            raise

    def create_user_data(
        self,
        resume_content: str,
        user_id: str = None,
        session_id: str = None,
        linkedin_profile: Optional[Dict] = None,
        github_profile: Optional[Dict] = None,
        academic_status: Optional[Dict] = None,
        **kwargs,
    ) -> UserData:
        """Create UserData object for the workflow"""

        if user_id is None:
            user_id = f"college_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Structure resume data
        resume_data = {
            "content": resume_content,
            "extracted_at": datetime.now().isoformat(),
            "source": "pdf_upload",
        }

        # Create base user data
        user_data: UserData = {
            "user_id": user_id,
            "session_id": session_id,
            "resume_data": resume_data,
            "demographic_info": None,
            "dbda_scores": None,
            "cii_results": None,
            "raisec_profile": None,
            "github_profile": github_profile,
            "linkedin_profile": linkedin_profile,
            "academic_status": academic_status,
            "current_profession": None,
            "financial_constraints": None,
            "timeline_flexibility": None,
            "family_obligations": None,
        }

        # Add any additional optional data
        for key, value in kwargs.items():
            if hasattr(user_data, key):
                user_data[key] = value
            else:
                logger.warning(f"Unknown user data field: {key}")

        logger.info(f"Created user data for user: {user_id}, session: {session_id}")
        return user_data

    def run_workflow(
        self,
        resume_pdf_path: str,
        initial_message: str = None,
        user_context: Optional[Dict] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Run the complete college skills workflow"""

        try:
            logger.info("=" * 60)
            logger.info("STARTING COLLEGE SKILLS WORKFLOW")
            logger.info("=" * 60)

            # Step 1: Load resume
            logger.info("Step 1: Loading resume from PDF")
            resume_content = self.load_resume_from_pdf(resume_pdf_path)

            # Step 2: Create user data
            logger.info("Step 2: Creating user data structure")

            # Extract optional context if provided
            linkedin_profile = (
                user_context.get("linkedin_profile") if user_context else None
            )
            github_profile = (
                user_context.get("github_profile") if user_context else None
            )
            academic_status = (
                user_context.get("academic_status") if user_context else None
            )

            user_data = self.create_user_data(
                resume_content=resume_content,
                linkedin_profile=linkedin_profile,
                github_profile=github_profile,
                academic_status=academic_status,
                **kwargs,
            )

            # Step 3: Set default message if not provided
            if initial_message is None:
                initial_message = "I want comprehensive career guidance and skill development recommendations based on my profile."

            # Step 4: Run the orchestrator workflow
            logger.info("Step 3: Running orchestrator workflow")
            logger.info(f"Initial message: {initial_message}")

            result = self.orchestrator.start_counseling_session(
                vertical="college_upskilling",
                user_data=user_data,
                initial_message=initial_message,
            )

            # Step 5: Process and enhance results
            logger.info("Step 4: Processing workflow results")
            enhanced_result = self._enhance_results(result, user_data)

            # Step 6: Save results
            self._save_results(enhanced_result, user_data["session_id"])

            logger.info("=" * 60)
            logger.info("COLLEGE SKILLS WORKFLOW COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)

            return enhanced_result

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "workflow_stage": "error",
            }

    def ask_follow_up(
        self, session_id: str, question: str, user_id: str = None
    ) -> Dict[str, Any]:
        """Ask follow-up questions in an existing session"""

        logger.info(f"Processing follow-up question for session: {session_id}")
        logger.info(f"Question: {question}")

        try:
            result = self.orchestrator.ask_follow_up_question(
                session_id=session_id, question=question, user_id=user_id
            )

            logger.info("Follow-up question processed successfully")
            return result

        except Exception as e:
            logger.error(f"Follow-up question failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _enhance_results(
        self, result: Dict[str, Any], user_data: UserData
    ) -> Dict[str, Any]:
        """Enhance results with additional metadata and formatting"""

        enhanced = result.copy()

        # Add workflow metadata
        enhanced["workflow_metadata"] = {
            "workflow_type": "college_upskilling",
            "user_id": user_data["user_id"],
            "session_id": user_data["session_id"],
            "processing_timestamp": datetime.now().isoformat(),
            "data_sources": self._identify_data_sources(user_data),
            "workflow_version": "1.0",
        }

        # Add quick summary for easy access
        if result.get("success") and "outputs" in result:
            enhanced["quick_summary"] = self._create_quick_summary(result["outputs"])

        return enhanced

    def _identify_data_sources(self, user_data: UserData) -> List[str]:
        """Identify which data sources were provided"""
        sources = ["resume"]  # Resume is always required

        if user_data.get("linkedin_profile"):
            sources.append("linkedin")
        if user_data.get("github_profile"):
            sources.append("github")
        if user_data.get("academic_status"):
            sources.append("academic_status")

        return sources

    def _create_quick_summary(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Create a quick summary of key results"""
        summary = {
            "agents_completed": [],
            "key_recommendations": [],
            "confidence_levels": {},
            "next_actions": [],
        }

        # Extract agent completion info
        if "agent_outputs" in outputs:
            for agent_id, agent_data in outputs["agent_outputs"].items():
                if agent_data.get("status") == "completed":
                    summary["agents_completed"].append(agent_id)
                    summary["confidence_levels"][agent_id] = agent_data.get(
                        "confidence", 0
                    )

        # Extract fleet summary info
        if "fleet_summary" in outputs:
            fleet_summary = outputs["fleet_summary"]
            summary["key_recommendations"] = fleet_summary.get("recommendations", [])[
                :5
            ]
            summary["next_actions"] = fleet_summary.get("next_actions", [])[:3]

        return summary

    def _save_results(self, result: Dict[str, Any], session_id: str):
        """Save workflow results to file"""
        try:
            results_dir = Path("workflow_results")
            results_dir.mkdir(exist_ok=True)

            filename = f"college_workflow.json"
            filepath = results_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Results saved to: {filepath}")

        except Exception as e:
            logger.warning(f"Failed to save results: {str(e)}")

    def print_results_summary(self, result: Dict[str, Any]):
        """Print a formatted summary of results"""

        print("\n" + "=" * 80)
        print("COLLEGE SKILLS WORKFLOW RESULTS SUMMARY")
        print("=" * 80)

        if not result.get("success"):
            print(f"❌ WORKFLOW FAILED: {result.get('error', 'Unknown error')}")
            return

        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")

        # Print metadata
        if "workflow_metadata" in result:
            metadata = result["workflow_metadata"]
            print(f"\n📊 Session ID: {metadata.get('session_id')}")
            print(f"📊 Processing Time: {metadata.get('processing_timestamp')}")
            print(f"📊 Data Sources: {', '.join(metadata.get('data_sources', []))}")

        # Print quick summary
        if "quick_summary" in result:
            summary = result["quick_summary"]

            print(f"\n🎯 Agents Completed: {len(summary['agents_completed'])}")
            for agent in summary["agents_completed"]:
                confidence = summary["confidence_levels"].get(agent, 0)
                print(f"   - {agent}: {confidence:.1%} confidence")

            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(summary["key_recommendations"][:3], 1):
                print(f"   {i}. {rec}")

            print(f"\n🚀 Next Actions:")
            for i, action in enumerate(summary["next_actions"][:3], 1):
                print(f"   {i}. {action}")

        print("\n" + "=" * 80)
        print(f"💾 Detailed results saved to workflow_results/")
        print("=" * 80 + "\n")


def main():
    """Main execution function with example usage"""

    # Configuration
    RESUME_PATH = r"/home/sarthak/Downloads/Resume.pdf"

    # Optional: Add additional context data
    user_context = {
        "linkedin_profile": {
            "connections": 150,
            "posts": 5,
            "recommendations": 2,
            "profile_completeness": 80,
        },
        "github_profile": {
            "repos": 12,
            "contributions": 45,
            "languages": ["Python", "JavaScript", "Java"],
            "stars_received": 23,
        },
        "academic_status": {
            "current_year": 4,
            "gpa": 8.5,
            "major_subjects": [
                "Data Structures",
                "Machine Learning",
                "Web Development",
            ],
            "expected_graduation": "2024-05",
        },
    }

    try:
        # Initialize workflow runner
        print("Initializing College Skills Workflow Runner...")
        runner = CollegeWorkflowRunner()

        # Run the workflow
        print("Starting workflow execution...")
        result = runner.run_workflow(
            resume_pdf_path=RESUME_PATH,
            initial_message="I want comprehensive career analysis and skill development recommendations. Please analyze my profile and provide actionable guidance.",
            user_context=user_context,
        )

        # Display results
        runner.print_results_summary(result)

        # Example follow-up question
        if result.get("success") and result.get("session_id"):
            print("\n" + "=" * 50)
            print("EXAMPLE FOLLOW-UP QUESTION")
            print("=" * 50)

            follow_up = runner.ask_follow_up(
                session_id=result["session_id"],
                question="What specific skills should I prioritize if I want to work in data science?",
                user_id=result.get("workflow_metadata", {}).get("user_id"),
            )

            if follow_up.get("success"):
                print("✅ Follow-up processed successfully")
                print("📋 Follow-up response available in detailed results")
            else:
                print(f"❌ Follow-up failed: {follow_up.get('error')}")

        return result

    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    # Run the workflow
    result = main()

    # Optional: Interactive mode
    if result and result.get("success"):
        print("\n" + "=" * 50)
        print("INTERACTIVE MODE")
        print("=" * 50)
        print("You can now ask follow-up questions!")
        print("Type 'exit' to quit, 'help' for commands")

        runner = CollegeWorkflowRunner()
        session_id = result.get("session_id")
        user_id = result.get("workflow_metadata", {}).get("user_id")

        while True:
            try:
                question = input("\n💬 Your question: ").strip()

                if question.lower() == "exit":
                    print("👋 Goodbye!")
                    break
                elif question.lower() == "help":
                    print("Commands:")
                    print("  - Ask any career or skill-related question")
                    print("  - 'exit' to quit")
                    print("  - 'help' to see this message")
                    continue
                elif not question:
                    continue

                follow_up = runner.ask_follow_up(
                    session_id=session_id, question=question, user_id=user_id
                )

                if follow_up.get("success"):
                    # Print key parts of the response
                    outputs = follow_up.get("outputs", {})
                    if "summary" in outputs:
                        print(f"\n📝 Response: {outputs['summary']}")
                    else:
                        print(
                            f"\n📝 Response processed successfully. Check detailed results."
                        )
                else:
                    print(f"❌ Error: {follow_up.get('error')}")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
