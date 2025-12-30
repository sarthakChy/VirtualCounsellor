import os
import logging
from langsmith import Client
from langchain_core.tracers.langchain import LangChainTracer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class LangSmithConfig:
    """Centralized LangSmith configuration"""

    @staticmethod
    def setup_environment():
        """Setup LangSmith environment variables"""
        # Load from .env file first
        load_dotenv()

        # Verify API key is loaded
        api_key = os.getenv("LANGCHAIN_API_KEY")
        if not api_key:
            logger.warning(
                "LANGCHAIN_API_KEY not found in environment variables. Please check your .env file."
            )
            return False

        # Set required environment variables (only if not already set)
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGCHAIN_PROJECT", "career-counselor-system")
        os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

        logger.info(f"LangSmith environment configured with API key: {api_key[:10]}...")
        return True

    @staticmethod
    def create_client() -> Client:
        """Create LangSmith client with error handling"""
        try:
            # Verify API key is available
            api_key = os.getenv("LANGCHAIN_API_KEY")
            if not api_key:
                logger.error(
                    "LANGCHAIN_API_KEY not found. Cannot create LangSmith client."
                )
                return None

            client = Client()
            # Test the connection
            try:
                # This will raise an exception if the API key is invalid
                client.list_runs(limit=1)
                logger.info("LangSmith client created and authenticated successfully")
            except Exception as auth_error:
                logger.error(f"LangSmith authentication failed: {auth_error}")
                return None

            return client
        except Exception as e:
            logger.error(f"Failed to create LangSmith client: {e}")
            return None

    @staticmethod
    def create_tracer(project_name: str = None) -> LangChainTracer:
        """Create LangChain tracer with error handling"""
        try:
            tracer = LangChainTracer(
                project_name=project_name or "career-counselor-system"
            )
            logger.info(f"LangChain tracer created for project: {project_name}")
            return tracer
        except Exception as e:
            logger.error(f"Failed to create LangChain tracer: {e}")
            return None

    @staticmethod
    def get_run_config(component_name: str, tags: list = None) -> dict:
        """Get standard run configuration"""
        config = {
            "callbacks": [],
            "tags": tags or [component_name],
            "metadata": {
                "component": component_name,
                "system": "virtual-career-counselor",
            },
        }

        tracer = LangSmithConfig.create_tracer()
        if tracer:
            config["callbacks"].append(tracer)

        return config


# Add this to your main orchestrator initialization
def initialize_langsmith():
    """Initialize LangSmith for the entire system"""
    success = LangSmithConfig.setup_environment()
    if success:
        logger.info("LangSmith initialization complete")
        return True
    else:
        logger.error("LangSmith initialization failed - tracing will be disabled")
        return False
