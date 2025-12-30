from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime, timedelta
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from agentic_layer.base_agent import BaseAgent
from agentic_layer.school_students.agents.sub_agents.college_matching_sub_agent import (
    CollegeMatchingSubAgent,
)
from agentic_layer.school_students.agents.sub_agents.scholarship_discovery_sub_agent import (
    ScholarshipDiscoverySubAgent,
)
from agentic_layer.school_students.agents.sub_agents.financial_aid_planning_sub_agent import (
    FinancialAidPlanningSubAgent,
)
from config.agent_config import AgentType, ProcessingStatus


class CollegeType(Enum):
    """Types of colleges in Indian system"""

    IIT = "Indian Institute of Technology"
    NIT = "National Institute of Technology"
    IIIT = "Indian Institute of Information Technology"
    GOVERNMENT = "Government College"
    STATE_UNIVERSITY = "State University"
    PRIVATE_UNIVERSITY = "Private University"
    DEEMED_UNIVERSITY = "Deemed University"
    CENTRAL_UNIVERSITY = "Central University"


class ScholarshipCategory(Enum):
    """Categories of scholarships"""

    MERIT_BASED = "Merit-based"
    NEED_BASED = "Need-based"
    MINORITY = "Minority Scholarship"
    GOVERNMENT = "Government Scholarship"
    PRIVATE = "Private/Corporate Scholarship"
    INTERNATIONAL = "International Scholarship"


class CollegeRecommendation(BaseModel):
    """Individual college recommendation"""

    college_name: str = Field(description="Name of the college/university")
    college_type: str = Field(
        description="Type of institution (IIT, NIT, Private, etc.)"
    )
    location: str = Field(description="City and state of the college")
    programs_offered: List[str] = Field(description="Relevant programs for the student")
    admission_requirements: Dict[str, Any] = Field(
        description="Specific admission criteria"
    )
    fees_structure: Dict[str, Any] = Field(description="Detailed fee information")
    ranking_information: Dict[str, Any] = Field(
        description="Rankings and reputation metrics"
    )
    campus_facilities: List[str] = Field(
        description="Key campus facilities and infrastructure"
    )
    placement_statistics: Dict[str, Any] = Field(
        description="Placement and career outcomes"
    )
    pros_and_cons: Dict[str, List[str]] = Field(
        description="Advantages and disadvantages"
    )
    suitability_score: float = Field(description="Match score for this student (0-1)")
    application_timeline: Dict[str, str] = Field(
        description="Key application deadlines"
    )


class ScholarshipOpportunity(BaseModel):
    """Individual scholarship opportunity"""

    scholarship_name: str = Field(description="Name of the scholarship")
    provider: str = Field(description="Organization providing the scholarship")
    scholarship_type: str = Field(description="Category of scholarship")
    eligibility_criteria: List[str] = Field(
        description="Detailed eligibility requirements"
    )
    benefit_amount: str = Field(description="Scholarship amount or percentage coverage")
    application_process: List[str] = Field(description="Steps in application process")
    required_documents: List[str] = Field(
        description="Documents needed for application"
    )
    selection_criteria: List[str] = Field(description="How recipients are selected")
    application_deadlines: Dict[str, str] = Field(description="Important dates")
    renewal_conditions: List[str] = Field(
        description="Conditions for scholarship renewal"
    )
    success_tips: List[str] = Field(description="Tips for successful application")
    compatibility_score: float = Field(
        description="How well student matches criteria (0-1)"
    )


class FinancialAidPlan(BaseModel):
    """Comprehensive financial aid planning"""

    total_estimated_cost: Dict[str, Any] = Field(description="Complete cost breakdown")
    funding_sources: Dict[str, Any] = Field(description="Potential funding options")
    timeline_based_planning: Dict[str, Any] = Field(
        description="Year-wise financial planning"
    )
    cost_optimization_strategies: List[str] = Field(
        description="Ways to reduce educational costs"
    )
    emergency_funding_options: List[str] = Field(description="Backup financial options")
    roi_analysis: Dict[str, Any] = Field(description="Return on investment analysis")


class CollegeScholarshipNavigatorOutput(BaseModel):
    """Structured output for college and scholarship navigation"""

    executive_summary: str = Field(
        description="Overview of college and financial aid guidance"
    )
    recommended_colleges: List[CollegeRecommendation] = Field(
        description="Prioritized college recommendations"
    )
    scholarship_opportunities: List[ScholarshipOpportunity] = Field(
        description="Relevant scholarship options"
    )
    financial_aid_planning: FinancialAidPlan = Field(
        description="Comprehensive financial planning"
    )
    application_strategy: Dict[str, Any] = Field(
        description="Strategic approach to applications"
    )
    geographic_analysis: Dict[str, Any] = Field(
        description="Location-based considerations"
    )
    backup_options: Dict[str, Any] = Field(
        description="Alternative plans and safety options"
    )
    decision_framework: Dict[str, Any] = Field(
        description="How to make final decisions"
    )
    timeline_coordination: Dict[str, Any] = Field(
        description="Coordinating all applications and deadlines"
    )
    next_steps: List[str] = Field(description="Immediate action items")


class CollegeScholarshipNavigatorAgent(BaseAgent):
    """
    Higher Education Advisor and Financial Aid Specialist Agent that recommends colleges,
    courses, and financial aid opportunities aligned with career goals. Specializes in
    Indian higher education landscape, admission processes, and comprehensive financial planning.
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="college_scholarship_navigator",
            agent_name="College and Scholarship Navigator Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config or {},
        )

        # Initialize dynamic sub-agents
        self.college_matching_agent = CollegeMatchingSubAgent(llm_model)
        self.scholarship_discovery_agent = ScholarshipDiscoverySubAgent(llm_model)
        self.financial_aid_planning_agent = FinancialAidPlanningSubAgent(llm_model)

        # Agent expertise areas
        self.expertise_areas = [
            "Indian higher education system navigation",
            "College ranking and suitability analysis",
            "Scholarship and financial aid matching",
            "Admission process optimization",
            "Educational cost-benefit analysis",
            "Geographic and cultural fit assessment",
        ]

        # College categories by entrance exam
        self.entrance_exam_colleges = {
            "JEE Main": {
                "top_tier": [
                    "IIT Delhi",
                    "IIT Bombay",
                    "IIT Madras",
                    "IIT Kanpur",
                    "IIT Kharagpur",
                ],
                "second_tier": [
                    "NIT Trichy",
                    "NIT Warangal",
                    "NIT Surathkal",
                    "IIIT Hyderabad",
                ],
                "private_options": [
                    "BITS Pilani",
                    "VIT Vellore",
                    "Manipal Institute",
                    "SRM University",
                ],
                "specializations": [
                    "Computer Science",
                    "Electronics",
                    "Mechanical",
                    "Civil",
                ],
            },
            "NEET UG": {
                "top_tier": [
                    "AIIMS Delhi",
                    "CMC Vellore",
                    "JIPMER Puducherry",
                    "KGMU Lucknow",
                ],
                "government": [
                    "State Medical Colleges",
                    "Central Universities",
                    "Military Medical Colleges",
                ],
                "private_options": [
                    "Kasturba Medical College",
                    "JSS Medical College",
                    "Amrita Medical College",
                ],
                "specializations": [
                    "General Medicine",
                    "Dental",
                    "Ayurveda",
                    "Homeopathy",
                ],
            },
            "CLAT": {
                "top_tier": [
                    "NLSIU Bangalore",
                    "NALSAR Hyderabad",
                    "WB NUJS Kolkata",
                    "NLIU Bhopal",
                ],
                "government": [
                    "DU Faculty of Law",
                    "BHU Law",
                    "Jamia Law",
                    "Aligarh Law",
                ],
                "private_options": [
                    "Jindal Global Law School",
                    "Symbiosis Law School",
                    "Christ University Law",
                ],
                "specializations": [
                    "Corporate Law",
                    "Criminal Law",
                    "Constitutional Law",
                    "International Law",
                ],
            },
            "CAT": {
                "top_tier": [
                    "IIM Ahmedabad",
                    "IIM Bangalore",
                    "IIM Calcutta",
                    "IIM Lucknow",
                ],
                "government": ["FMS Delhi", "DoMS IIT Delhi", "SJMSOM IIT Bombay"],
                "private_options": [
                    "XLRI Jamshedpur",
                    "ISB Hyderabad",
                    "MDI Gurgaon",
                    "SPJIMR Mumbai",
                ],
                "specializations": [
                    "Finance",
                    "Marketing",
                    "Operations",
                    "HR",
                    "Analytics",
                ],
            },
        }

        # Scholarship categories mapping
        self.scholarship_mapping = {
            "merit_based": {
                "academic_excellence": [
                    "Kishore Vaigyanik Protsahan Yojana",
                    "National Talent Search Examination",
                ],
                "entrance_based": ["JEE Merit Scholarships", "NEET Merit Scholarships"],
                "university_specific": [
                    "Institute Merit Scholarships",
                    "Endowment Scholarships",
                ],
            },
            "need_based": {
                "government": [
                    "Post Matric Scholarships",
                    "Pre Matric Scholarships",
                    "Central Sector Scholarships",
                ],
                "private": [
                    "Tata Scholarships",
                    "Reliance Foundation Scholarships",
                    "Azim Premji Scholarships",
                ],
                "institutional": ["Fee Waiver Programs", "Educational Loan Subsidies"],
            },
            "category_specific": {
                "sc_st": [
                    "National Fellowship for SC/ST",
                    "Post Matric Scholarship SC/ST",
                ],
                "obc": [
                    "Post Matric Scholarship OBC",
                    "Central Sector Scholarship OBC",
                ],
                "minority": [
                    "Maulana Azad National Fellowship",
                    "Minority Scholarship Schemes",
                ],
            },
        }

    def _define_required_inputs(self) -> List[str]:
        """Required inputs for college and scholarship navigation"""
        return []

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that enhance navigation"""
        return [
            "career_goals",
            "educational_pathway",
            "academic_timeline",
            "dbda_scores",
            "cii_results",
            "current_grade",
            "academic_performance",
            "family_preferences",
            "financial_considerations",
            "geographical_preferences",
            "entrance_exam_results",
            "extracurricular_activities",
            "previous_agent_outputs",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of navigation output"""
        return {
            "executive_summary": "str",
            "recommended_colleges": "list",
            "scholarship_opportunities": "list",
            "financial_aid_planning": "dict",
            "application_strategy": "dict",
            "geographic_analysis": "dict",
            "backup_options": "dict",
            "decision_framework": "dict",
            "timeline_coordination": "dict",
            "next_steps": "list",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.output_parser = JsonOutputParser(
            pydantic_object=CollegeScholarshipNavigatorOutput
        )

        # Create the main navigation prompt
        self.navigation_prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "career_pathway",
                "educational_timeline",
                "financial_context",
                "geographic_preferences",
                "academic_achievements",
                "assessment_insights",
                "market_context",
            ],
            template=self._create_navigation_template(),
        )

    def _create_navigation_template(self) -> str:
        """Create the comprehensive navigation prompt template"""
        return """You are an expert Higher Education Advisor and Financial Aid Specialist with deep knowledge of the Indian education system. You help students navigate college selection, admission processes, and financial aid opportunities to achieve their career goals cost-effectively.

STUDENT PROFILE:
{student_profile}

CAREER PATHWAY:
{career_pathway}

EDUCATIONAL TIMELINE:
{educational_timeline}

FINANCIAL CONTEXT:
{financial_context}

GEOGRAPHIC PREFERENCES:
{geographic_preferences}

ACADEMIC ACHIEVEMENTS:
{academic_achievements}

ASSESSMENT INSIGHTS:
{assessment_insights}

MARKET CONTEXT:
{market_context}

NAVIGATION PRINCIPLES:

1. STRATEGIC COLLEGE SELECTION:
   - Match colleges to career goals and academic profile
   - Balance reach, match, and safety schools
   - Consider ROI, placement records, and alumni networks
   - Evaluate program quality, faculty, and research opportunities
   - Factor in location, campus culture, and personal fit

2. COMPREHENSIVE FINANCIAL PLANNING:
   - Estimate total cost of education (tuition, living, extras)
   - Identify all possible funding sources
   - Create year-wise financial timeline
   - Plan for cost increases and unexpected expenses
   - Optimize funding mix for minimum debt burden

3. SCHOLARSHIP OPTIMIZATION:
   - Map student profile to scholarship eligibility
   - Prioritize high-probability, high-value opportunities
   - Create application timeline and strategy
   - Prepare for scholarship-specific requirements
   - Plan for scholarship renewal and maintenance

4. ADMISSION STRATEGY:
   - Optimize application portfolio across institutions
   - Plan for entrance exam performance scenarios
   - Prepare backup options for different outcomes
   - Strategic timing of applications and fee payments
   - Coordinate interviews, counseling, and seat allocation

5. PRACTICAL CONSIDERATIONS:
   - Family financial capacity and comfort zone
   - Geographic constraints and preferences
   - Cultural fit and institutional environment
   - Long-term career impact and network building
   - Risk mitigation and contingency planning

INDIAN HIGHER EDUCATION CONTEXT:
- Entrance exam-based admissions with cutoff systems
- Reservation policies and quota considerations
- Government vs private institution trade-offs
- Regional preferences and local advantages
- Scholarship ecosystem and eligibility criteria
- Educational loan policies and procedures

Please provide comprehensive college and scholarship navigation following this JSON structure:

{format_instructions}

Focus on:
1. Specific college recommendations with detailed analysis
2. Targeted scholarship opportunities with application strategies
3. Complete financial planning with cost optimization
4. Strategic application approach with timeline coordination
5. Decision-making framework for final selections
6. Practical next steps for immediate implementation

Remember: This guidance will influence major life decisions and financial commitments. Provide thorough, realistic recommendations that balance aspiration with practical constraints."""

    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic for college and scholarship navigation"""

        previous_outputs = validated_input.get("previous_agent_outputs", {})

        # Extract user data
        user_data = validated_input.get("user_data", {})

        # Extract career_goals from career_pathway_explorer output
        career_goals = []
        if "career_pathway_explorer" in previous_outputs:
            career_result = previous_outputs["career_pathway_explorer"]
            if career_result.status == ProcessingStatus.COMPLETED:
                careers = career_result.output_data.get(
                    "recommended_career_pathways", []
                )
                career_goals = [
                    career.get("career_title")
                    for career in careers
                    if isinstance(career, dict)
                ]

        if not career_goals:
            career_goals = ["Engineering", "Medicine", "Business"]  # Default fallback

        # Extract educational_pathway from educational_roadmap_planner output
        educational_pathway = []
        if "educational_roadmap_planner" in previous_outputs:
            roadmap_result = previous_outputs["educational_roadmap_planner"]
            if roadmap_result.status == ProcessingStatus.COMPLETED:
                pathways = roadmap_result.output_data.get(
                    "higher_education_pathways", []
                )
                educational_pathway = [
                    pathway.get("degree_type")
                    for pathway in pathways
                    if isinstance(pathway, dict)
                ]

        if not educational_pathway:
            educational_pathway = ["BTech", "MBBS", "BBA"]  # Default fallback

        # Extract academic_timeline from educational_roadmap_planner output
        academic_timeline = {}
        if "educational_roadmap_planner" in previous_outputs:
            roadmap_result = previous_outputs["educational_roadmap_planner"]
            if roadmap_result.status == ProcessingStatus.COMPLETED:
                timeline = roadmap_result.output_data.get("timeline_overview", {})
                academic_timeline = timeline

        if not academic_timeline:
            academic_timeline = {
                "current_focus": "College preparation",
                "timeline": "Grade 12 to Higher Education",
            }

        # Create the required_data structure that the rest of your method expects
        validated_input["required_data"] = {
            "career_goals": career_goals,
            "educational_pathway": educational_pathway,
            "academic_timeline": academic_timeline,
        }

        # Extract required data
        career_goals = validated_input["required_data"]["career_goals"]
        educational_pathway = validated_input["required_data"]["educational_pathway"]
        academic_timeline = validated_input["required_data"]["academic_timeline"]

        # Extract optional context
        optional_data = validated_input["optional_data"]
        previous_outputs = validated_input.get("previous_outputs", {})

        # Get previous agent results for context
        test_interpreter_result = previous_outputs.get("test_score_interpreter")
        stream_advisor_result = previous_outputs.get("academic_stream_advisor")
        career_explorer_result = previous_outputs.get("career_pathway_explorer")
        roadmap_planner_result = previous_outputs.get("educational_roadmap_planner")

        # Prepare comprehensive inputs for navigation
        student_profile = self._prepare_student_profile(optional_data, previous_outputs)
        career_pathway = self._extract_career_pathway(
            career_explorer_result, career_goals
        )
        educational_timeline = self._extract_educational_timeline(
            roadmap_planner_result, academic_timeline
        )
        financial_context = self._prepare_financial_context(optional_data)
        geographic_preferences = self._extract_geographic_preferences(optional_data)
        academic_achievements = self._assess_academic_achievements(
            optional_data, previous_outputs
        )
        assessment_insights = self._consolidate_assessment_insights(
            test_interpreter_result, stream_advisor_result
        )
        market_context = self._prepare_market_context(career_pathway)

        # Add processing note
        self._add_processing_note(
            "Starting comprehensive college and scholarship navigation"
        )

        try:
            # Generate navigation using LLM
            prompt_input = {
                "student_profile": student_profile,
                "career_pathway": career_pathway,
                "educational_timeline": educational_timeline,
                "financial_context": financial_context,
                "geographic_preferences": geographic_preferences,
                "academic_achievements": academic_achievements,
                "assessment_insights": assessment_insights,
                "market_context": market_context,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            formatted_prompt = self.navigation_prompt.format(**prompt_input)

            # Get LLM response
            llm_response = self.llm_model.invoke(formatted_prompt)

            # Convert to dictionary and add metadata
            result = self._parse_llm_response(llm_response)

            # Add navigation metadata
            result["navigation_metadata"] = {
                "advisor_role": "Higher Education Advisor and Financial Aid Specialist",
                "specialization": "Indian Higher Education System",
                "guidance_date": datetime.now().isoformat(),
                "methodology": "Comprehensive College and Scholarship Navigation",
                "based_on_assessments": self._list_assessment_sources(previous_outputs),
            }

            # Add computational analysis using sub-agents
            college_matching_result = self.college_matching_agent.match_colleges(
                student_profile=student_profile,
                career_goals=career_pathway,
                academic_profile=academic_achievements,
                preferences=geographic_preferences,
                constraints=financial_context,
            )

            result["dynamic_college_matching"] = college_matching_result
            self._add_processing_note("Dynamic college matching completed successfully")

            scholarship_result = self.scholarship_discovery_agent.discover_scholarships(
                student_profile=student_profile,
                academic_achievements=academic_achievements,
                financial_need=financial_context,
                career_pathway=career_pathway,
                demographic_info=optional_data.get("demographic_info", {}),
            )

            result["dynamic_scholarship_discovery"] = scholarship_result
            self._add_processing_note(
                "Dynamic scholarship discovery completed successfully"
            )

            financial_aid_result = (
                self.financial_aid_planning_agent.create_financial_plan(
                    student_profile=student_profile,
                    college_costs=self._estimate_college_costs(
                        result["recommended_colleges"]
                    ),
                    family_income=self._extract_family_income(financial_context),
                    scholarship_potential=scholarship_result["total_potential_funding"],
                    loan_preferences=optional_data.get("loan_preferences", "Moderate"),
                )
            )

            result["dynamic_financial_planning"] = financial_aid_result
            self._add_processing_note(
                "Dynamic financial planning completed successfully"
            )

            # Add practical guidance
            result["practical_guidance"] = {
                "immediate_actions": result["dynamic_college_matching"]["next_steps"],
                "scholarship_application_timeline": result[
                    "dynamic_scholarship_discovery"
                ]["application_schedule"],
                "financial_preparation": result["dynamic_financial_planning"][
                    "preparation_checklist"
                ],
                "decision_support": self._create_decision_support_framework(result),
                "family_discussion_points": self._generate_family_discussion_points(
                    result
                ),
            }

            self._add_processing_note(
                "College and scholarship navigation completed successfully"
            )
            return result

        except Exception as e:
            self.logger.error(f"Error in navigation: {str(e)}")
            self._add_processing_note(f"Navigation error: {str(e)}")
            raise

    def _prepare_student_profile(
        self, optional_data: Dict[str, Any], previous_outputs: Dict[str, Any]
    ) -> str:
        """Prepare comprehensive student profile for navigation"""
        profile_parts = []

        # Basic information
        current_grade = optional_data.get("current_grade", "12")
        profile_parts.append(f"Current Grade: {current_grade}")

        # Academic performance
        if optional_data.get("academic_performance"):
            profile_parts.append(
                f"Academic Performance: {optional_data['academic_performance']}"
            )

        # Assessment insights
        if optional_data.get("dbda_scores"):
            valid_scores = {
                k: v for k, v in optional_data["dbda_scores"].items() if v is not None
            }
            top_aptitudes = sorted(
                valid_scores.items(), key=lambda x: x[1], reverse=True
            )[:2]
            aptitude_summary = ", ".join(
                [apt.replace("_", " ").title() for apt, _ in top_aptitudes]
            )
            profile_parts.append(f"Top Aptitude Areas: {aptitude_summary}")

        # Extracurricular achievements
        if optional_data.get("extracurricular_activities"):
            activities = optional_data["extracurricular_activities"]
            if isinstance(activities, list):
                profile_parts.append(f"Activities: {', '.join(activities)}")
            else:
                profile_parts.append(f"Activities: {activities}")

        # Previous agent insights
        if previous_outputs:
            if "academic_stream_advisor" in previous_outputs:
                stream_result = previous_outputs["academic_stream_advisor"]
                if stream_result.status == ProcessingStatus.COMPLETED:
                    profile_parts.append(
                        "Academic stream guidance completed - preferences identified"
                    )

        return (
            "\n".join(profile_parts)
            if profile_parts
            else "Student profile under development"
        )

    def _extract_career_pathway(self, career_explorer_result, career_goals) -> str:
        """Extract career pathway from previous analysis"""
        if (
            career_explorer_result
            and career_explorer_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = career_explorer_result.output_data

            career_parts = []
            if output_data.get("executive_summary"):
                career_parts.append(
                    f"Career Analysis: {output_data['executive_summary']}"
                )

            if output_data.get("recommended_career_pathways"):
                pathways = output_data["recommended_career_pathways"]
                if isinstance(pathways, list) and len(pathways) > 0:
                    top_pathway = pathways[0]
                    if isinstance(top_pathway, dict):
                        career_title = top_pathway.get(
                            "career_title", "Primary career path"
                        )
                        career_field = top_pathway.get("career_field", "")
                        career_parts.append(
                            f"Primary Career Goal: {career_title} in {career_field}"
                        )

            return "\n".join(career_parts)
        else:
            return f"Career Goals: {career_goals}"

    def _extract_educational_timeline(
        self, roadmap_planner_result, academic_timeline
    ) -> str:
        """Extract educational timeline from roadmap planning"""
        if (
            roadmap_planner_result
            and roadmap_planner_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = roadmap_planner_result.output_data

            timeline_parts = []
            if output_data.get("executive_summary"):
                timeline_parts.append(
                    f"Educational Roadmap: {output_data['executive_summary']}"
                )

            if output_data.get("timeline_overview"):
                timeline_overview = output_data["timeline_overview"]
                if isinstance(timeline_overview, dict):
                    for key, value in timeline_overview.items():
                        if isinstance(value, str) and len(value) < 200:
                            timeline_parts.append(
                                f"{key.replace('_', ' ').title()}: {value}"
                            )

            return "\n".join(timeline_parts)
        else:
            return f"Academic Timeline: {academic_timeline}"

    def _prepare_financial_context(self, optional_data: Dict[str, Any]) -> str:
        """Prepare financial context for navigation"""
        financial_parts = []

        if optional_data.get("financial_considerations"):
            financial_parts.append(
                f"Financial Situation: {optional_data['financial_considerations']}"
            )

        if optional_data.get("family_preferences"):
            preferences = optional_data["family_preferences"]
            if (
                "budget" in str(preferences).lower()
                or "cost" in str(preferences).lower()
            ):
                financial_parts.append(f"Family Preferences: {preferences}")

        return (
            "\n".join(financial_parts)
            if financial_parts
            else "Middle-class family seeking cost-effective options"
        )

    def _extract_geographic_preferences(self, optional_data: Dict[str, Any]) -> str:
        """Extract geographic preferences and constraints"""
        geo_parts = []

        if optional_data.get("geographical_preferences"):
            geo_parts.append(
                f"Location Preferences: {optional_data['geographical_preferences']}"
            )

        if optional_data.get("family_preferences"):
            preferences = optional_data["family_preferences"]
            if any(
                word in str(preferences).lower()
                for word in ["local", "nearby", "home", "city", "state"]
            ):
                geo_parts.append(f"Family Location Preferences: {preferences}")

        return (
            "\n".join(geo_parts)
            if geo_parts
            else "Open to various locations based on quality and opportunities"
        )

    def _assess_academic_achievements(
        self, optional_data: Dict[str, Any], previous_outputs: Dict[str, Any]
    ) -> str:
        """Assess academic achievements and competitive positioning"""
        achievement_parts = []

        # Academic performance
        if optional_data.get("academic_performance"):
            achievement_parts.append(
                f"Academic Record: {optional_data['academic_performance']}"
            )

        # Entrance exam results if available
        if optional_data.get("entrance_exam_results"):
            achievement_parts.append(
                f"Entrance Exam Performance: {optional_data['entrance_exam_results']}"
            )

        # Assessment scores
        if optional_data.get("dbda_scores"):
            scores = optional_data["dbda_scores"]
            valid_scores = {k: v for k, v in scores.items() if v is not None}
            avg_score = (
                sum(valid_scores.values()) / len(valid_scores) if valid_scores else 0
            )
            achievement_parts.append(
                f"Aptitude Assessment: Average score {avg_score:.1f}"
            )

        # Extracurricular achievements
        if optional_data.get("extracurricular_activities"):
            achievement_parts.append("Strong extracurricular engagement")

        return "\n".join(achievement_parts)

    def _consolidate_assessment_insights(
        self, test_interpreter_result, stream_advisor_result
    ) -> str:
        """Consolidate insights from assessment interpretation"""
        insight_parts = []

        if (
            test_interpreter_result
            and test_interpreter_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = test_interpreter_result.output_data
            if output_data.get("key_recommendations"):
                recommendations = output_data["key_recommendations"]
                if isinstance(recommendations, list):
                    insight_parts.extend(recommendations[:2])  # Top 2 recommendations

        if (
            stream_advisor_result
            and stream_advisor_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = stream_advisor_result.output_data
            if output_data.get("recommended_streams"):
                streams = output_data["recommended_streams"]
                if isinstance(streams, list) and len(streams) > 0:
                    top_stream = streams[0]
                    if isinstance(top_stream, dict):
                        stream_name = top_stream.get("stream_type", "Primary stream")
                        insight_parts.append(
                            f"Recommended academic focus: {stream_name}"
                        )

        return (
            "\n".join(insight_parts)
            if insight_parts
            else "Assessment insights being processed"
        )

    def _prepare_market_context(self, career_pathway: str) -> str:
        """Prepare market context for career pathway"""
        market_parts = [
            "Current Indian higher education landscape:",
            "- Engineering: High competition, strong placement opportunities",
            "- Medicine: Limited seats, high social value and earning potential",
            "- Business: Growing demand, diverse specialization options",
            "- Liberal Arts: Emerging field with creative career opportunities",
            "",
            "Key trends:",
            "- Digital skills integration across all fields",
            "- Industry-academia collaboration increasing",
            "- International exposure opportunities growing",
            "- Entrepreneurship support in educational institutions",
        ]

        return "\n".join(market_parts)

    def _list_assessment_sources(self, previous_outputs: Dict[str, Any]) -> List[str]:
        """List the assessment sources used in navigation"""
        sources = []
        for agent_id in [
            "test_score_interpreter",
            "academic_stream_advisor",
            "career_pathway_explorer",
            "educational_roadmap_planner",
        ]:
            if agent_id in previous_outputs:
                result = previous_outputs[agent_id]
                if result.status == ProcessingStatus.COMPLETED:
                    sources.append(result.agent_name)
        return sources

    def _estimate_college_costs(
        self, recommended_colleges: List[Dict]
    ) -> Dict[str, float]:
        """Estimate costs from recommended colleges"""
        if not recommended_colleges:
            return {
                "tuition_range": 200000,
                "living_costs": 100000,
                "total_annual": 300000,
            }

        # Extract cost information from recommendations
        costs = []
        for college in recommended_colleges:
            if isinstance(college, dict) and college.get("fees_structure"):
                fees = college["fees_structure"]
                if isinstance(fees, dict) and "annual_tuition" in fees:
                    costs.append(float(fees["annual_tuition"]))

        if costs:
            return {
                "average_tuition": sum(costs) / len(costs),
                "tuition_range": max(costs) - min(costs),
                "living_costs": 120000,  # Estimated living costs
                "total_annual": (sum(costs) / len(costs)) + 120000,
            }
        else:
            return {
                "tuition_range": 250000,
                "living_costs": 120000,
                "total_annual": 370000,
            }

    def _extract_family_income(self, financial_context: str) -> str:
        """Extract family income level from financial context"""
        context_lower = financial_context.lower()

        if any(
            word in context_lower for word in ["low", "limited", "tight", "struggling"]
        ):
            return "Lower Income"
        elif any(
            word in context_lower
            for word in ["high", "comfortable", "affluent", "well-off"]
        ):
            return "Higher Income"
        else:
            return "Middle Income"

    def _create_decision_support_framework(
        self, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create decision support framework from results"""
        return {
            "college_selection_criteria": [
                "Career alignment and program quality",
                "Financial feasibility and ROI",
                "Location and cultural fit",
                "Placement records and alumni network",
            ],
            "scholarship_prioritization": [
                "Application deadline urgency",
                "Probability of success",
                "Award amount vs effort required",
                "Renewal sustainability",
            ],
            "financial_decision_points": [
                "Total debt burden acceptable to family",
                "Expected career earning potential",
                "Alternative funding sources availability",
                "Timeline for financial return",
            ],
        }

    def _generate_family_discussion_points(self, result: Dict[str, Any]) -> List[str]:
        """Generate points for family discussion"""
        return [
            "Review recommended colleges together and discuss preferences",
            "Discuss financial capacity and comfortable debt levels",
            "Plan for scholarship application deadlines and requirements",
            "Consider geographic preferences and cultural fit factors",
            "Evaluate backup options and contingency plans",
            "Discuss expected career outcomes vs investment required",
            "Plan for application fee budgets and documentation timeline",
            "Consider family support system during college years",
            "Discuss expectations for student's academic performance",
            "Plan for regular family meetings to track progress",
        ]

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
