from typing import Dict, List, Any, Optional
import json
import logging
from langchain_community.document_loaders import PyMuPDFLoader
from datetime import datetime
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agentic_layer.base_agent import BaseAgent
from config.agent_config import (
    AgentType,
    ResumeAnalysis,
    LinkedInAnalysis,
    GitHubAnalysis,
    AcademicAnalysis,
    ExperienceAnalysis,
    ProfileAnalysisResult,
)
from config.llm_config import llm_manager

# Configure logging
logger = logging.getLogger(__name__)


class ProfileAnalysisAgent(BaseAgent):
    """
    Profile Analysis Agent for College Students

    Analyzes resume, LinkedIn, GitHub, academic status, and experience data
    to provide comprehensive profile assessment and improvement recommendations.
    """

    def __init__(self, llm_model=None):
        super().__init__(
            agent_id="profile_analysis",
            agent_name="Profile Analysis Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config={
                "max_tokens": 4000,
                "temperature": 0.1,  # Low temperature for consistent analysis
                "analysis_depth": "comprehensive",
            },
        )

    def _define_required_inputs(self) -> List[str]:
        """Resume data is required for profile analysis"""
        return ["resume_data"]

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that can enhance analysis"""
        return [
            "linkedin_profile",
            "github_profile",
            "academic_status",
            "internship_experience",
            "project_experience",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the output schema for profile analysis"""
        return {
            "overall_assessment": "Comprehensive profile evaluation",
            "individual_analyses": "Detailed analysis of each input source",
            "recommendations": "Actionable improvement recommendations",
            "competitive_positioning": "Market positioning analysis",
        }

    def _initialize_agent(self):
        """Initialize prompts and parsers for each input type"""

        # Resume analysis components
        self.resume_parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
        self.resume_prompt = PromptTemplate(
            template="""You are an expert technical recruiter and career counselor analyzing a college student's resume.

Analyze the following resume data and provide a comprehensive assessment:

Resume Data:
{resume_data}

Focus on:
- Technical and soft skills extraction
- Education relevance and achievements  
- Work/internship experience quality
- Overall professional presentation
- Career trajectory and interests
- Areas for improvement

Provide specific, actionable insights for a college student seeking career opportunities.

{format_instructions}""",
            input_variables=["resume_data"],
            partial_variables={
                "format_instructions": self.resume_parser.get_format_instructions()
            },
        )

        # LinkedIn analysis components
        self.linkedin_parser = PydanticOutputParser(pydantic_object=LinkedInAnalysis)
        self.linkedin_prompt = PromptTemplate(
            template="""You are a professional networking and personal branding expert analyzing a college student's LinkedIn profile.

Analyze the following LinkedIn profile data:

LinkedIn Data:
{linkedin_data}

Evaluate:
- Professional network quality and size
- Content engagement and thought leadership
- Profile completeness and presentation
- Industry connections and relevance
- Professional visibility and branding

Provide specific recommendations for improving professional presence.

{format_instructions}""",
            input_variables=["linkedin_data"],
            partial_variables={
                "format_instructions": self.linkedin_parser.get_format_instructions()
            },
        )

        # GitHub analysis components
        self.github_parser = PydanticOutputParser(pydantic_object=GitHubAnalysis)
        self.github_prompt = PromptTemplate(
            template="""You are a senior software engineer and technical hiring manager evaluating a college student's GitHub profile.

Analyze the following GitHub profile data:

GitHub Data:
{github_data}

Assess:
- Technical skills and programming language proficiency
- Code quality and project complexity
- Contribution consistency and collaboration
- Portfolio strength and diversity
- Open source involvement

Provide technical recommendations for improving the developer portfolio.

{format_instructions}""",
            input_variables=["github_data"],
            partial_variables={
                "format_instructions": self.github_parser.get_format_instructions()
            },
        )

        # Academic analysis components
        self.academic_parser = PydanticOutputParser(pydantic_object=AcademicAnalysis)
        self.academic_prompt = PromptTemplate(
            template="""You are an academic advisor and career counselor analyzing a college student's academic performance.

Analyze the following academic data:

Academic Status:
{academic_data}

Evaluate:
- Academic performance and trajectory
- Coursework relevance to career goals
- Specialization alignment
- Academic achievements and honors
- Knowledge gaps and learning opportunities

Provide academic guidance for career preparation.

{format_instructions}""",
            input_variables=["academic_data"],
            partial_variables={
                "format_instructions": self.academic_parser.get_format_instructions()
            },
        )

        # Experience analysis components
        self.experience_parser = PydanticOutputParser(
            pydantic_object=ExperienceAnalysis
        )
        self.experience_prompt = PromptTemplate(
            template="""You are an industry professional and career mentor evaluating a college student's practical experience.

Analyze the following experience data:

Internship and Project Experience:
{experience_data}

Assess:
- Practical skills demonstrated
- Industry exposure and relevance
- Project complexity and impact
- Leadership and initiative shown
- Real-world application of knowledge

Provide recommendations for gaining valuable experience.

{format_instructions}""",
            input_variables=["experience_data"],
            partial_variables={
                "format_instructions": self.experience_parser.get_format_instructions()
            },
        )

        # Comprehensive analysis components
        self.final_parser = PydanticOutputParser(pydantic_object=ProfileAnalysisResult)
        self.final_analysis_prompt = PromptTemplate(
            template="""You are a senior career counselor and hiring expert providing comprehensive profile analysis for a college student.

Based on the following individual analyses, provide an integrated assessment:

Resume Analysis:
{resume_analysis}

LinkedIn Analysis (if available):
{linkedin_analysis}

GitHub Analysis (if available):
{github_analysis}

Academic Analysis (if available):
{academic_analysis}

Experience Analysis (if available):
{experience_analysis}

Student Context:
- College student seeking career opportunities
- Likely targeting entry-level to junior positions
- Needs actionable advice for profile improvement
- Must compete in current job market

Provide a comprehensive, strategic analysis that synthesizes all available information into actionable insights.

{format_instructions}""",
            input_variables=[
                "resume_analysis",
                "linkedin_analysis",
                "github_analysis",
                "academic_analysis",
                "experience_analysis",
            ],
            partial_variables={
                "format_instructions": self.final_parser.get_format_instructions()
            },
        )

        self.logger.info("Profile Analysis Agent initialized successfully")

    @traceable(
        name="individual_input_processing",
        tags=["profile_analysis", "input_processing"],
    )
    def _process_individual_inputs(
        self, validated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process each input source with structured LLM analysis - now with tracing"""
        individual_analyses = {}

        # Process resume (required) with tracing
        resume_data = validated_data["required_data"]["resume_data"]
        self.logger.info("Processing resume data")

        resume_analysis = self._analyze_resume_with_tracing(resume_data)
        individual_analyses["resume"] = resume_analysis
        self._add_processing_note("Resume analysis completed successfully")

        # Process optional inputs with tracing
        for input_type in ["linkedin_profile", "github_profile", "academic_status"]:
            if input_type in validated_data["optional_data"]:
                analysis = self._analyze_optional_input_with_tracing(
                    input_type, validated_data["optional_data"][input_type]
                )
                individual_analyses[input_type.split("_")[0]] = (
                    analysis  # linkedin_profile -> linkedin
                )

        # Process experience data with tracing
        experience_data = {}
        if "internship_experience" in validated_data["optional_data"]:
            experience_data["internships"] = validated_data["optional_data"][
                "internship_experience"
            ]
        if "project_experience" in validated_data["optional_data"]:
            experience_data["projects"] = validated_data["optional_data"][
                "project_experience"
            ]

        if experience_data:
            experience_analysis = self._analyze_experience_with_tracing(experience_data)
            individual_analyses["experience"] = experience_analysis

        return individual_analyses

    @traceable(name="resume_analysis", tags=["profile_analysis", "resume", "llm_chain"])
    def _analyze_resume_with_tracing(self, resume_data):
        """Analyze resume with tracing"""
        try:
            resume_chain = self.resume_prompt | self.llm_model | self.resume_parser
            resume_analysis = resume_chain.invoke(
                {"resume_data": json.dumps(resume_data, indent=2)}
            )
            return resume_analysis.dict()
        except Exception as e:
            self.logger.error(f"Resume analysis failed: {e}")
            return {"error": f"Resume analysis failed: {str(e)}"}

    @traceable(
        name="optional_input_analysis",
        tags=["profile_analysis", "optional_inputs", "llm_chain"],
    )
    def _analyze_optional_input_with_tracing(self, input_type: str, data):
        """Analyze optional inputs with tracing"""
        try:
            if input_type == "linkedin_profile":
                chain = self.linkedin_prompt | self.llm_model | self.linkedin_parser
                result = chain.invoke({"linkedin_data": json.dumps(data, indent=2)})
            elif input_type == "github_profile":
                chain = self.github_prompt | self.llm_model | self.github_parser
                result = chain.invoke({"github_data": json.dumps(data, indent=2)})
            elif input_type == "academic_status":
                chain = self.academic_prompt | self.llm_model | self.academic_parser
                result = chain.invoke({"academic_data": json.dumps(data, indent=2)})
            else:
                return {"error": f"Unknown input type: {input_type}"}

            self._add_processing_note(f"{input_type} analysis completed successfully")
            return result.dict()

        except Exception as e:
            self.logger.error(f"{input_type} analysis failed: {e}")
            return {"error": f"{input_type} analysis failed: {str(e)}"}

    @traceable(
        name="experience_analysis", tags=["profile_analysis", "experience", "llm_chain"]
    )
    def _analyze_experience_with_tracing(self, experience_data):
        """Analyze experience data with tracing"""
        try:
            experience_chain = (
                self.experience_prompt | self.llm_model | self.experience_parser
            )
            experience_analysis = experience_chain.invoke(
                {"experience_data": json.dumps(experience_data, indent=2)}
            )
            self._add_processing_note("Experience analysis completed successfully")
            return experience_analysis.dict()
        except Exception as e:
            self.logger.error(f"Experience analysis failed: {e}")
            return {"error": f"Experience analysis failed: {str(e)}"}

    @traceable(
        name="comprehensive_profile_analysis",
        tags=["profile_analysis", "comprehensive", "llm_chain"],
    )
    def _process_core_logic(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic with enhanced tracing"""
        self.logger.info("Starting comprehensive profile analysis")

        # Step 1: Process individual inputs with tracing
        individual_analyses = self._process_individual_inputs(validated_data)

        # Step 2: Perform comprehensive integration analysis with tracing
        self.logger.info("Performing integrated profile analysis")

        comprehensive_analysis = self._create_comprehensive_analysis_with_tracing(
            individual_analyses
        )

        # Compile final result
        result = {
            "comprehensive_analysis": comprehensive_analysis,
            "individual_analyses": individual_analyses,
            "analysis_metadata": {
                "analyzed_components": list(individual_analyses.keys()),
                "missing_components": [
                    comp
                    for comp in ["linkedin", "github", "academic", "experience"]
                    if comp not in individual_analyses
                ],
                "analysis_timestamp": datetime.now().isoformat(),
                "data_sources_count": len(individual_analyses),
            },
            "recommendations_summary": {
                "immediate_actions": comprehensive_analysis.get(
                    "recommended_next_steps", []
                )[:3],
                "profile_improvements": comprehensive_analysis.get(
                    "improvement_priorities", []
                )[:3],
                "competitive_positioning": comprehensive_analysis.get(
                    "profile_positioning", "Not available"
                ),
            },
        }

        return result

    @traceable(
        name="final_comprehensive_analysis",
        tags=["profile_analysis", "final_synthesis", "llm_chain"],
    )
    def _create_comprehensive_analysis_with_tracing(
        self, individual_analyses: Dict[str, Any]
    ):
        """Create comprehensive analysis with tracing"""
        # Prepare data for final analysis
        analysis_inputs = {
            "resume_analysis": json.dumps(
                individual_analyses.get("resume", {}), indent=2
            ),
            "linkedin_analysis": json.dumps(
                individual_analyses.get("linkedin", "Not provided"), indent=2
            ),
            "github_analysis": json.dumps(
                individual_analyses.get("github", "Not provided"), indent=2
            ),
            "academic_analysis": json.dumps(
                individual_analyses.get("academic", "Not provided"), indent=2
            ),
            "experience_analysis": json.dumps(
                individual_analyses.get("experience", "Not provided"), indent=2
            ),
        }

        try:
            final_chain = (
                self.final_analysis_prompt | self.llm_model | self.final_parser
            )
            comprehensive_analysis = final_chain.invoke(analysis_inputs)
            self._add_processing_note("Comprehensive analysis completed successfully")
            return comprehensive_analysis.dict()
        except Exception as e:
            self.logger.error(f"Comprehensive analysis failed: {e}")
            # Return a fallback analysis structure
            return {
                "error": f"Comprehensive analysis failed: {str(e)}",
                "individual_analyses_available": list(individual_analyses.keys()),
            }

    def _calculate_confidence_score(
        self, validated_data: Dict[str, Any], output_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score based on data availability and analysis success"""
        base_confidence = 0.6

        # Boost confidence based on data availability
        available_sources = (
            len(validated_data.get("optional_data", {})) + 1
        )  # +1 for required resume
        max_sources = 5  # resume + 4 optional sources
        data_completeness_boost = (available_sources / max_sources) * 0.3

        # Boost confidence based on analysis success
        individual_analyses = output_data.get("individual_analyses", {})
        successful_analyses = sum(
            1 for analysis in individual_analyses.values() if "error" not in analysis
        )
        analysis_success_boost = (
            successful_analyses / max(len(individual_analyses), 1)
        ) * 0.1

        total_confidence = min(
            1.0, base_confidence + data_completeness_boost + analysis_success_boost
        )
        return round(total_confidence, 2)

    def _parse_llm_response(self, response) -> Dict[str, Any]:
        """Strict JSON parsing without fallback - raises exceptions on failure"""
        content = response.content.strip()

        # Clean markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # Try direct JSON parsing first
        try:
            return json.loads(content)
        except json.JSONDecodeError as json_error:
            # Try with output parser as second attempt
            try:
                parsed_output = self.output_parser.parse(content)
                if hasattr(parsed_output, "dict"):
                    return parsed_output.dict()
                elif isinstance(parsed_output, dict):
                    return parsed_output
                else:
                    raise ValueError(
                        f"Output parser returned unexpected type: {type(parsed_output)}"
                    )
            except Exception as parser_error:
                # Log both errors for debugging
                self.logger.error(f"JSON parsing failed: {json_error}")
                self.logger.error(f"Output parser failed: {parser_error}")
                self.logger.error(f"Raw content that failed to parse: {repr(content)}")

                # Raise a comprehensive error with context
                raise ValueError(
                    f"Failed to parse LLM response. "
                    f"JSON error: {json_error}. "
                    f"Parser error: {parser_error}. "
                    f"Content length: {len(content)} chars"
                )
