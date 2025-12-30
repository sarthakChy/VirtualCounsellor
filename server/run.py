import os
import json
import logging
import traceback
from fastapi import BackgroundTasks
from enum import Enum
import threading
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import uuid
import asyncio
import tempfile
import io
from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Body,
    Request,
    File,
    UploadFile,
    Form,
    Depends,
    Header,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

# Import your existing modules
from agentic_layer.agent_orchestrator import MainOrchestrator, UserData
from utils.sten_calculator import StenCalculator
from config.llm_config import llm_manager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ========================== Pydantic Models ==========================


class DemographicInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    current_grade: Optional[int] = None
    school_name: Optional[str] = None
    location: Optional[str] = None
    gender: Optional[str] = None


class DBDAScores(BaseModel):
    CA: Union[str, float, None] = None
    CL: Union[str, float, None] = None
    MA: Union[str, float, None] = None
    NA: Union[str, float, None] = None
    PM: Union[str, float, None] = None
    RA: Union[str, float, None] = None
    SA: Union[str, float, None] = None
    VA: Union[str, float, None] = None


class CIIResults(BaseModel):
    artistic: int = Field(..., ge=0, le=10)
    scientific: int = Field(..., ge=0, le=10)
    social: int = Field(..., ge=0, le=10)
    conventional: int = Field(..., ge=0, le=10)
    enterprising: int = Field(..., ge=0, le=10)
    realistic: int = Field(..., ge=0, le=10)


class AcademicStatus(BaseModel):
    GPA: Optional[float] = None
    current_year: Optional[int] = None
    major_subjects: Optional[List[str]] = None
    extracurriculars: Optional[List[str]] = None
    expected_graduation: Optional[str] = None


class FinancialConstraints(BaseModel):
    max_annual_tuition: Optional[float] = None
    requires_scholarship: Optional[bool] = None
    family_income_range: Optional[str] = None


class GitHubProfile(BaseModel):
    username: Optional[str] = None
    repos: Optional[int] = None
    contributions: Optional[int] = None
    languages: Optional[List[str]] = None
    stars_received: Optional[int] = None


class LinkedInProfile(BaseModel):
    connections: Optional[int] = None
    posts: Optional[int] = None
    recommendations: Optional[int] = None
    profile_completeness: Optional[int] = None


class SchoolStudentRequest(BaseModel):
    demographic_info: Optional[DemographicInfo] = None
    dbda_scores: DBDAScores
    cii_results: CIIResults
    academic_status: Optional[AcademicStatus] = None
    financial_constraints: Optional[FinancialConstraints] = None
    initial_message: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class CollegeUpskillRequest(BaseModel):
    academic_status: Optional[AcademicStatus] = None
    github_profile: Optional[GitHubProfile] = None
    linkedin_profile: Optional[LinkedInProfile] = None
    initial_message: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class CareerTransitionRequest(BaseModel):
    demographic_info: Optional[DemographicInfo] = None
    dbda_scores: DBDAScores
    cii_results: CIIResults
    current_profession: str
    financial_constraints: Optional[FinancialConstraints] = None
    timeline_flexibility: Optional[str] = None
    family_obligations: Optional[Dict[str, Any]] = None
    initial_message: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatMessage(BaseModel):
    session_id: str
    message: str
    user_id: Optional[str] = None


class APIResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# ========================== App Initialization ==========================

app = FastAPI(
    title="Virtual Counselor API",
    version="1.0.0",
    description="AI-powered career counseling system with multiple specialized verticals",
    root_path="/api",
    docs_url="/docs",
)

# ========================== Middleware ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.google.com",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================== Session Status Management ==========================


class SessionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Global session storage (in production, use Redis or database)
session_storage: Dict[str, Dict[str, Any]] = {}
session_lock = threading.Lock()


def update_session_status(
    session_id: str,
    status: SessionStatus,
    data: Optional[Dict] = None,
    error: Optional[str] = None,
):
    """Update session status and data"""
    with session_lock:
        if session_id not in session_storage:
            session_storage[session_id] = {}

        session_storage[session_id].update(
            {
                "status": status,
                "updated_at": datetime.now().isoformat(),
                "data": data,
                "error": error,
            }
        )


def get_session_status(session_id: str) -> Dict[str, Any]:
    """Get current session status and data"""
    with session_lock:
        return session_storage.get(
            session_id,
            {
                "status": SessionStatus.PENDING,
                "updated_at": None,
                "data": None,
                "error": None,
            },
        )


# ========================== Global Variables ==========================

# Initialize orchestrator (singleton pattern)
orchestrator = None


def get_orchestrator():
    global orchestrator
    if orchestrator is None:
        try:
            llm_model = llm_manager.initialize_gemini(
                model_name="gemini-1.5-flash", temperature=0.1, max_tokens=4000
            )
            orchestrator = MainOrchestrator(llm_model=llm_model)
            logger.info("Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize counseling system: {str(e)}",
            )
    return orchestrator


# ========================== Utility Functions ==========================


def create_user_data_from_request(data: dict, vertical_type: str) -> UserData:
    """Convert request data to UserData format"""
    calculator = StenCalculator()
    user_id = data.get("user_id") or f"{vertical_type}_user_{uuid.uuid4().hex[:8]}"
    session_id = data.get("session_id") or f"session_{uuid.uuid4().hex[:8]}"
    dbda_scores = data.get("dbda_scores")
    dem_info = data.get("demographic_info", {})  # Add default empty dict
    grade = dem_info.get("current_grade")
    gender = dem_info.get("gender", "male")

    # Calculate sten scores and extract only the sten_score values
    dbda_sten_results = calculator.calculate_student_stens(
        dbda_scores, grade=grade, gender=gender
    )

    # Extract only the sten scores (integers) from the result dictionary
    dbda_sten_scores = {}
    for ability, result in dbda_sten_results.items():
        dbda_sten_scores[ability] = result["sten_score"]

    print("DBDA sten scores", dbda_sten_scores)

    user_data: UserData = {
        "user_id": user_id,
        "session_id": session_id,
        "demographic_info": data.get("demographic_info"),
        "dbda_scores": dbda_sten_scores,  # Now contains just integers
        "cii_results": data.get("cii_results"),
        "resume_data": None,
        "github_profile": data.get("github_profile"),
        "linkedin_profile": data.get("linkedin_profile"),
        "academic_status": data.get("academic_status"),
        "current_profession": data.get("current_profession"),
        "financial_constraints": data.get("financial_constraints"),
        "timeline_flexibility": data.get("timeline_flexibility"),
        "family_obligations": data.get("family_obligations"),
    }

    return user_data


async def extract_resume_text(file: UploadFile) -> str:
    """Extract text from uploaded resume file"""
    try:
        # Check file type
        if file.content_type not in [
            "application/pdf",
            "text/plain",
            "application/msword",
        ]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF, TXT, or DOC files.",
            )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        try:
            if file.content_type == "application/pdf":
                from langchain_community.document_loaders import PyMuPDFLoader

                loader = PyMuPDFLoader(tmp_file_path)
                pages = loader.load()
                resume_text = "\n\n".join([page.page_content for page in pages])
            else:
                # Handle text files
                with open(tmp_file_path, "r", encoding="utf-8") as f:
                    resume_text = f.read()

            if not resume_text.strip():
                raise HTTPException(
                    status_code=400, detail="No text content found in uploaded file"
                )

            return resume_text

        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume extraction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process resume: {str(e)}"
        )


# ========================== Routes ==========================


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Virtual Counselor API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "verticals": {
                "school_students": "/school-students",
                "college_upskilling": "/college-upskilling",
                "career_transition": "/career-transition",
            },
            "chat": "/chat",
            "utilities": {"health": "/health", "verticals_info": "/verticals"},
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test orchestrator initialization
        orch = get_orchestrator()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "orchestrator": "initialized",
            "verticals": ["school_students", "college_upskilling", "career_transition"],
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@app.get("/verticals")
async def get_verticals_info():
    """Get information about available verticals"""
    try:
        orch = get_orchestrator()
        verticals_info = orch.get_available_verticals()

        return APIResponse(
            success=True,
            data={"verticals": verticals_info, "total_count": len(verticals_info)},
        )
    except Exception as e:
        logger.error(f"Failed to get verticals info: {e}")
        return APIResponse(success=False, error=str(e))


# ========================== Background Task Functions ==========================


async def process_school_student_background(
    user_data: UserData, initial_message: str, session_id: str
):
    """Background task for processing school student analysis"""
    try:
        logger.info(
            f"Starting background processing for school student session: {session_id}"
        )
        update_session_status(session_id, SessionStatus.PROCESSING)

        # Get orchestrator
        orch = get_orchestrator()

        # Execute workflow
        result = orch.start_counseling_session(
            vertical="school_students",
            user_data=user_data,
            initial_message=initial_message,
        )

        if result.get("success"):
            logger.info(f"School student analysis completed for session: {session_id}")
            update_session_status(session_id, SessionStatus.COMPLETED, data=result)
        else:
            logger.warning(f"School student analysis failed: {result.get('error')}")
            update_session_status(
                session_id,
                SessionStatus.FAILED,
                error=result.get("error", "Analysis failed"),
            )

    except Exception as e:
        logger.error(
            f"Background task error for session {session_id}: {e}", exc_info=True
        )
        update_session_status(session_id, SessionStatus.FAILED, error=str(e))


async def process_college_upskilling_background(
    user_data: UserData, initial_message: str, session_id: str
):
    """Background task for processing college upskilling analysis"""
    try:
        logger.info(
            f"Starting background processing for college upskilling session: {session_id}"
        )
        update_session_status(session_id, SessionStatus.PROCESSING)

        # Get orchestrator
        orch = get_orchestrator()

        # Execute workflow
        result = orch.start_counseling_session(
            vertical="college_upskilling",
            user_data=user_data,
            initial_message=initial_message,
        )

        if result.get("success"):
            logger.info(
                f"College upskilling analysis completed for session: {session_id}"
            )
            update_session_status(session_id, SessionStatus.COMPLETED, data=result)
        else:
            logger.warning(f"College upskilling analysis failed: {result.get('error')}")
            update_session_status(
                session_id,
                SessionStatus.FAILED,
                error=result.get("error", "Analysis failed"),
            )

    except Exception as e:
        logger.error(
            f"Background task error for session {session_id}: {e}", exc_info=True
        )
        update_session_status(session_id, SessionStatus.FAILED, error=str(e))


async def process_career_transition_background(
    user_data: UserData, initial_message: str, session_id: str
):
    """Background task for processing career transition analysis"""
    try:
        logger.info(
            f"Starting background processing for career transition session: {session_id}"
        )
        update_session_status(session_id, SessionStatus.PROCESSING)

        # Get orchestrator
        orch = get_orchestrator()

        # Execute workflow
        result = orch.start_counseling_session(
            vertical="career_transition",
            user_data=user_data,
            initial_message=initial_message,
        )

        if result.get("success"):
            logger.info(
                f"Career transition analysis completed for session: {session_id}"
            )
            update_session_status(session_id, SessionStatus.COMPLETED, data=result)
        else:
            logger.warning(f"Career transition analysis failed: {result.get('error')}")
            update_session_status(
                session_id,
                SessionStatus.FAILED,
                error=result.get("error", "Analysis failed"),
            )

    except Exception as e:
        logger.error(
            f"Background task error for session {session_id}: {e}", exc_info=True
        )
        update_session_status(session_id, SessionStatus.FAILED, error=str(e))


# ========================== Modified Vertical Endpoints ==========================


@app.post("/school-students", response_model=APIResponse)
async def analyze_school_student(
    request: SchoolStudentRequest, background_tasks: BackgroundTasks
):
    """
    Analyze school student profile and provide career guidance (Background Processing)

    Returns immediately with session_id. Use /status/{session_id} to check progress.
    """
    try:
        logger.info("Processing school student request (background)")

        # Convert request to dict and then to UserData
        request_dict = request.dict()
        user_data = create_user_data_from_request(request_dict, "school_student")

        session_id = user_data["session_id"]

        # Initialize session status
        update_session_status(session_id, SessionStatus.PENDING)

        # Set default message if not provided
        initial_message = (
            request.initial_message
            or "I need comprehensive academic and career guidance based on my assessment results."
        )

        # Add background task
        background_tasks.add_task(
            process_school_student_background, user_data, initial_message, session_id
        )

        return APIResponse(
            success=True,
            data={
                "message": "Analysis started. Check status using the session_id.",
                "session_id": session_id,
                "status_endpoint": f"/status/{session_id}",
                "estimated_completion_time": "2-5 minutes",
            },
            session_id=session_id,
        )

    except Exception as e:
        logger.error(f"School student endpoint error: {e}", exc_info=True)
        return APIResponse(success=False, error=f"Internal server error: {str(e)}")


@app.post("/college-upskilling", response_model=APIResponse)
async def analyze_college_student_with_resume(
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(...),
    academic_status: Optional[str] = Form(None),
    github_profile: Optional[str] = Form(None),
    linkedin_profile: Optional[str] = Form(None),
    initial_message: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
):
    """
    Analyze college student profile with resume upload (Background Processing)

    Returns immediately with session_id. Use /status/{session_id} to check progress.
    """
    try:
        logger.info("Processing college upskilling request with resume (background)")

        # Extract resume text
        resume_text = await extract_resume_text(resume)

        # Parse optional JSON fields
        parsed_academic_status = None
        if academic_status:
            try:
                parsed_academic_status = json.loads(academic_status)
            except json.JSONDecodeError:
                logger.warning("Invalid academic_status JSON, ignoring")

        parsed_github = None
        if github_profile:
            try:
                parsed_github = json.loads(github_profile)
            except json.JSONDecodeError:
                logger.warning("Invalid github_profile JSON, ignoring")

        parsed_linkedin = None
        if linkedin_profile:
            try:
                parsed_linkedin = json.loads(linkedin_profile)
            except json.JSONDecodeError:
                logger.warning("Invalid linkedin_profile JSON, ignoring")

        # Create user data
        user_id_final = user_id or f"college_user_{uuid.uuid4().hex[:8]}"
        session_id_final = session_id or f"session_{uuid.uuid4().hex[:8]}"

        resume_data = {
            "content": resume_text,
            "extracted_at": datetime.now().isoformat(),
            "source": "api_upload",
            "filename": resume.filename,
        }

        user_data: UserData = {
            "user_id": user_id_final,
            "session_id": session_id_final,
            "demographic_info": None,
            "dbda_scores": None,
            "cii_results": None,
            "resume_data": resume_data,
            "github_profile": parsed_github,
            "linkedin_profile": parsed_linkedin,
            "academic_status": parsed_academic_status,
            "current_profession": None,
            "financial_constraints": None,
            "timeline_flexibility": None,
            "family_obligations": None,
        }

        # Initialize session status
        update_session_status(session_id_final, SessionStatus.PENDING)

        # Set default message
        initial_message_final = (
            json.loads(initial_message)
            or "I want comprehensive career guidance and skill development recommendations based on my profile."
        )

        logger.info(
            {
                "user_data": user_data,
                "initial_message": initial_message_final,
                "session_id": session_id_final,
            }
        )
        # Add background task
        background_tasks.add_task(
            process_college_upskilling_background,
            user_data,
            initial_message_final,
            session_id_final,
        )

        return APIResponse(
            success=True,
            data={
                "message": "Analysis started. Check status using the session_id.",
                "session_id": session_id_final,
                "status_endpoint": f"/status/{session_id_final}",
                "estimated_completion_time": "2-5 minutes",
            },
            session_id=session_id_final,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"College upskilling endpoint error: {e}", exc_info=True)
        return APIResponse(success=False, error=f"Internal server error: {str(e)}")


@app.post("/career-transition", response_model=APIResponse)
async def analyze_career_transition(
    request: CareerTransitionRequest, background_tasks: BackgroundTasks
):
    """
    Analyze career transition feasibility and planning (Background Processing)

    Returns immediately with session_id. Use /status/{session_id} to check progress.
    """
    try:
        logger.info("Processing career transition request (background)")

        # Convert request to UserData format
        request_dict = request.dict()
        user_data = create_user_data_from_request(request_dict, "career_transition")

        session_id = user_data["session_id"]

        # Initialize session status
        update_session_status(session_id, SessionStatus.PENDING)

        # Set default message
        initial_message = (
            request.initial_message
            or "I want to explore career transition options and get a detailed transition plan."
        )

        # Add background task
        background_tasks.add_task(
            process_career_transition_background, user_data, initial_message, session_id
        )

        return APIResponse(
            success=True,
            data={
                "message": "Analysis started. Check status using the session_id.",
                "session_id": session_id,
                "status_endpoint": f"/status/{session_id}",
                "estimated_completion_time": "2-5 minutes",
            },
            session_id=session_id,
        )

    except Exception as e:
        logger.error(f"Career transition endpoint error: {e}", exc_info=True)
        return APIResponse(success=False, error=f"Internal server error: {str(e)}")


# ========================== Status Checking Endpoints ==========================


@app.get("/status/{session_id}", response_model=APIResponse)
async def get_analysis_status(session_id: str):
    """
    Check the status of a background analysis task

    Returns:
    - pending: Analysis is queued
    - processing: Analysis is in progress
    - completed: Analysis is complete with results
    - failed: Analysis failed with error message
    """
    try:
        session_info = get_session_status(session_id)

        return APIResponse(
            success=True,
            data={
                "session_id": session_id,
                "status": session_info["status"],
                "updated_at": session_info["updated_at"],
                "results": (
                    session_info["data"]
                    if session_info["status"] == SessionStatus.COMPLETED
                    else None
                ),
                "error": (
                    session_info["error"]
                    if session_info["status"] == SessionStatus.FAILED
                    else None
                ),
                "can_chat": session_info["status"] == SessionStatus.COMPLETED,
            },
            session_id=session_id,
        )

    except Exception as e:
        logger.error(f"Status check error: {e}")
        return APIResponse(success=False, error=str(e), session_id=session_id)


# ========================== Modified Chat Endpoint ==========================


@app.post("/chat", response_model=APIResponse)
async def chat_with_counselor(request: ChatMessage):
    """
    Continue conversation with the counselor in an existing session

    Note: Chat is only available for sessions with 'completed' status.
    """
    try:
        logger.info(f"Processing chat message for session: {request.session_id}")

        # Check if session is completed
        session_info = get_session_status(request.session_id)
        if session_info["status"] != SessionStatus.COMPLETED:
            return APIResponse(
                success=False,
                error=f"Chat not available. Session status: {session_info['status']}. Please wait for analysis to complete.",
                session_id=request.session_id,
            )

        # Get orchestrator
        orch = get_orchestrator()

        # Handle follow-up question
        result = orch.ask_follow_up_question(
            session_id=request.session_id,
            question=request.message,
            user_id=request.user_id,
        )

        if result.get("success"):
            logger.info(f"Chat response generated for session: {request.session_id}")
            return APIResponse(success=True, data=result, session_id=request.session_id)
        else:
            logger.warning(
                f"Chat failed for session {request.session_id}: {result.get('error')}"
            )
            return APIResponse(
                success=False,
                error=result.get("error", "Failed to process chat message"),
                session_id=request.session_id,
            )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        return APIResponse(
            success=False,
            error=f"Internal server error: {str(e)}",
            session_id=request.session_id,
        )


# ========================== Error Handlers ==========================


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False, error=exc.detail, timestamp=datetime.now().isoformat()
        ).dict(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error="Internal server error",
            timestamp=datetime.now().isoformat(),
        ).dict(),
    )


# ========================== Startup/Shutdown Events ==========================


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Virtual Counselor API...")

    # Pre-initialize orchestrator to catch any startup issues
    try:
        get_orchestrator()
        logger.info("Orchestrator pre-initialized successfully")
    except Exception as e:
        logger.error(f"Failed to pre-initialize orchestrator: {e}")

    logger.info("Virtual Counselor API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Shutting down Virtual Counselor API...")
    # Add any cleanup code here
    logger.info("Virtual Counselor API shut down complete")
