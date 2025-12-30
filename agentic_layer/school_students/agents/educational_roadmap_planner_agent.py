from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime, timedelta
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from agentic_layer.base_agent import BaseAgent
from agentic_layer.school_students.agents.sub_agents.timeline_planning_sub_agent import (
    TimelinePlanningSubAgent,
)
from agentic_layer.school_students.agents.sub_agents.resource_planning_sub_agent import (
    ResourcePlanningSubAgent,
)
from config.agent_config import AgentType, ProcessingStatus


class EducationLevel(Enum):
    """Education levels in Indian system"""

    GRADE_9 = "Grade 9"
    GRADE_10 = "Grade 10"
    GRADE_11 = "Grade 11"
    GRADE_12 = "Grade 12"
    UNDERGRADUATE = "Undergraduate"
    POSTGRADUATE = "Postgraduate"


class EntranceExamType(Enum):
    """Major entrance exams in India"""

    JEE_MAIN = "JEE Main"
    JEE_ADVANCED = "JEE Advanced"
    NEET_UG = "NEET UG"
    NEET_PG = "NEET PG"
    CLAT = "CLAT"
    UPSC_CSE = "UPSC Civil Services"
    GATE = "GATE"
    CAT = "CAT"
    XAT = "XAT"
    BITSAT = "BITSAT"


class GradeMilestone(BaseModel):
    """Milestone for a specific grade"""

    grade: str = Field(description="Grade level (9, 10, 11, 12)")
    academic_focus: List[str] = Field(
        description="Key academic priorities for this grade"
    )
    subject_priorities: Dict[str, str] = Field(description="Subject-wise focus areas")
    entrance_exam_preparation: List[str] = Field(
        description="Entrance exam preparation activities"
    )
    extracurricular_recommendations: List[str] = Field(
        description="Recommended extracurricular activities"
    )
    skill_development_goals: List[str] = Field(
        description="Skills to develop during this grade"
    )
    assessment_milestones: List[str] = Field(
        description="Key assessments and benchmarks"
    )
    college_preparation_activities: List[str] = Field(
        description="College/career preparation activities"
    )
    timeline_considerations: Dict[str, Any] = Field(
        description="Important timing considerations"
    )


class EntranceExamStrategy(BaseModel):
    """Strategy for specific entrance exams"""

    exam_name: str = Field(description="Name of entrance exam")
    preparation_timeline: str = Field(description="When to start and timeline")
    subject_priorities: List[str] = Field(
        description="Subject-wise preparation priorities"
    )
    preparation_strategy: List[str] = Field(
        description="Preparation approach and methods"
    )
    coaching_recommendations: str = Field(
        description="Coaching requirements and recommendations"
    )
    mock_test_schedule: List[str] = Field(description="Mock test and practice schedule")
    difficulty_assessment: str = Field(
        description="Expected difficulty and competition level"
    )
    success_factors: List[str] = Field(description="Key factors for success")


class HigherEducationPathway(BaseModel):
    """Higher education pathway details"""

    degree_type: str = Field(description="Type of degree (BTech, MBBS, BA, etc.)")
    duration: str = Field(description="Duration of the program")
    entry_requirements: List[str] = Field(description="Requirements for admission")
    top_institutions: List[str] = Field(
        description="Top colleges/universities for this path"
    )
    specialization_options: List[str] = Field(description="Available specializations")
    career_outcomes: List[str] = Field(
        description="Career opportunities after graduation"
    )
    financial_considerations: Dict[str, Any] = Field(
        description="Cost and financial aid information"
    )


class EducationalRoadmapPlannerOutput(BaseModel):
    """Structured output for educational roadmap planning"""

    executive_summary: str = Field(description="Overview of the educational roadmap")
    grade_wise_milestones: List[GradeMilestone] = Field(
        description="Detailed grade-wise planning"
    )
    entrance_exam_strategies: List[EntranceExamStrategy] = Field(
        description="Entrance exam preparation plans"
    )
    higher_education_pathways: List[HigherEducationPathway] = Field(
        description="Post-12th education options"
    )
    subject_selection_guidance: Dict[str, Any] = Field(
        description="Subject and elective selection advice"
    )
    timeline_overview: Dict[str, Any] = Field(
        description="Overall timeline and critical decision points"
    )
    backup_plans: List[str] = Field(
        description="Alternative pathways and contingency plans"
    )
    resource_requirements: Dict[str, Any] = Field(
        description="Resources needed (financial, time, support)"
    )
    progress_monitoring: Dict[str, Any] = Field(
        description="How to track progress and adjust plans"
    )
    next_steps: List[str] = Field(description="Immediate action items")


class EducationalRoadmapPlannerAgent(BaseAgent):
    """
    Academic Planning Specialist Agent that creates comprehensive educational roadmaps
    from current grade through higher education. Specializes in Indian education system
    pathways, entrance exam strategies, and milestone-based planning for school students.
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="educational_roadmap_planner",
            agent_name="Educational Roadmap Planner Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config or {},
        )
        self.timeline_planning_agent = TimelinePlanningSubAgent(llm_model)
        self.resource_planning_agent = ResourcePlanningSubAgent(llm_model)

        # Agent expertise areas
        self.expertise_areas = [
            "Indian education system pathway planning",
            "Grade-wise milestone development (9th-12th)",
            "Entrance exam preparation strategies",
            "Higher education pathway mapping",
            "Academic timeline optimization",
            "Subject selection and career alignment",
        ]

        # Stream-based entrance exam mapping
        self.stream_exam_mapping = {
            "Science (PCM)": {
                "primary_exams": ["JEE Main", "JEE Advanced", "BITSAT", "VITEEE"],
                "specialized_exams": ["GATE", "ISRO", "DRDO"],
                "preparation_subjects": ["Mathematics", "Physics", "Chemistry"],
                "coaching_recommended": "Strongly recommended for competitive exams",
            },
            "Science (PCB)": {
                "primary_exams": ["NEET UG", "AIIMS", "JIPMER"],
                "specialized_exams": ["NEET PG", "AIAPGET", "IIIT Entrance"],
                "preparation_subjects": ["Physics", "Chemistry", "Biology"],
                "coaching_recommended": "Essential for medical entrance exams",
            },
            "Science (PCMB)": {
                "primary_exams": ["JEE Main", "NEET UG", "BITSAT"],
                "specialized_exams": [
                    "Dual degree entrance exams",
                    "Research entrance tests",
                ],
                "preparation_subjects": [
                    "Mathematics",
                    "Physics",
                    "Chemistry",
                    "Biology",
                ],
                "coaching_recommended": "Recommended for competitive preparation",
            },
            "Commerce (Math)": {
                "primary_exams": [
                    "CA Foundation",
                    "CMA Foundation",
                    "Company Secretary",
                ],
                "specialized_exams": ["CLAT", "DU Entrance", "BBA Entrance"],
                "preparation_subjects": ["Mathematics", "Accountancy", "Economics"],
                "coaching_recommended": "Beneficial for professional courses",
            },
            "Commerce (No Math)": {
                "primary_exams": ["CLAT", "DU Entrance", "Hotel Management Entrance"],
                "specialized_exams": ["Mass Communication Entrance", "BBA Entrance"],
                "preparation_subjects": ["Business Studies", "Economics", "English"],
                "coaching_recommended": "Required for law and management entrance",
            },
            "Arts/Humanities": {
                "primary_exams": ["CLAT", "UPSC CSE", "DU Entrance"],
                "specialized_exams": [
                    "Mass Communication",
                    "Social Work Entrance",
                    "Education Entrance",
                ],
                "preparation_subjects": [
                    "History",
                    "Political Science",
                    "Geography",
                    "English",
                ],
                "coaching_recommended": "Essential for civil services preparation",
            },
        }

        # Grade-wise focus areas
        self.grade_focus_mapping = {
            "9": {
                "academic_priority": "Foundation building and concept clarity",
                "skill_focus": [
                    "Study habits",
                    "Time management",
                    "Basic research skills",
                ],
                "preparation_activities": [
                    "Explore interests",
                    "Build subject fundamentals",
                    "Develop reading habits",
                ],
                "decision_timeline": "Stream awareness and initial exploration",
            },
            "10": {
                "academic_priority": "Board exam preparation and stream decision",
                "skill_focus": ["Exam techniques", "Subject mastery", "Goal setting"],
                "preparation_activities": [
                    "Stream selection",
                    "Career counseling",
                    "Board exam preparation",
                ],
                "decision_timeline": "Final stream selection by end of 10th grade",
            },
            "11": {
                "academic_priority": "Stream specialization and entrance exam foundation",
                "skill_focus": [
                    "Specialized subject knowledge",
                    "Entrance exam awareness",
                    "Advanced study methods",
                ],
                "preparation_activities": [
                    "Entrance exam foundation",
                    "Subject specialization",
                    "College research",
                ],
                "decision_timeline": "Entrance exam selection and preparation planning",
            },
            "12": {
                "academic_priority": "Board exams and entrance exam preparation",
                "skill_focus": [
                    "Intensive preparation",
                    "Stress management",
                    "Decision making",
                ],
                "preparation_activities": [
                    "Final preparations",
                    "College applications",
                    "Scholarship applications",
                ],
                "decision_timeline": "College selection and admission processes",
            },
        }

        # Higher education pathways mapping
        self.education_pathways = {
            "Engineering": {
                "degrees": ["BTech", "BE", "BTech+MTech (Dual)"],
                "top_institutions": ["IITs", "NITs", "IIITs", "BITS", "DTU", "VIT"],
                "specializations": [
                    "Computer Science",
                    "Electronics",
                    "Mechanical",
                    "Civil",
                    "Chemical",
                ],
                "entry_exams": ["JEE Main", "JEE Advanced", "BITSAT"],
                "duration": "4 years (BTech), 5 years (Dual Degree)",
                "career_outcomes": [
                    "Software Engineer",
                    "Design Engineer",
                    "Research Engineer",
                    "Product Manager",
                ],
            },
            "Medicine": {
                "degrees": ["MBBS", "BDS", "BAMS", "BHMS"],
                "top_institutions": [
                    "AIIMS",
                    "CMCs",
                    "JIPMER",
                    "State Medical Colleges",
                ],
                "specializations": [
                    "Internal Medicine",
                    "Surgery",
                    "Pediatrics",
                    "Radiology",
                ],
                "entry_exams": ["NEET UG"],
                "duration": "5.5 years (MBBS), 5 years (BDS)",
                "career_outcomes": [
                    "Doctor",
                    "Surgeon",
                    "Specialist",
                    "Medical Researcher",
                ],
            },
            "Business": {
                "degrees": ["BBA", "BCom", "BMS", "BBM"],
                "top_institutions": ["IIMs", "XLRI", "FMS", "SRCC", "LSR"],
                "specializations": ["Finance", "Marketing", "HR", "Operations"],
                "entry_exams": ["CAT", "XAT", "DU Entrance", "IPM"],
                "duration": "3 years (UG), 2 years (MBA)",
                "career_outcomes": ["Manager", "Consultant", "Analyst", "Entrepreneur"],
            },
            "Law": {
                "degrees": ["BA LLB", "BBA LLB", "LLB"],
                "top_institutions": ["NLUs", "DU Faculty of Law", "BHU", "Jamia"],
                "specializations": [
                    "Corporate Law",
                    "Criminal Law",
                    "Constitutional Law",
                ],
                "entry_exams": ["CLAT", "AILET", "LSAT"],
                "duration": "5 years (Integrated), 3 years (LLB)",
                "career_outcomes": [
                    "Lawyer",
                    "Judge",
                    "Legal Advisor",
                    "Civil Servant",
                ],
            },
        }

    def _define_required_inputs(self) -> List[str]:
        """Required inputs for educational roadmap planning"""
        return []  # Only current_grade is truly required

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that enhance roadmap planning"""
        return [
            "current_grade",
            "recommended_streams",
            "career_interests",  # These come from user_data or previous agents
            "dbda_scores",
            "cii_results",
            "academic_performance",
            "family_preferences",
            "financial_considerations",
            "geographical_preferences",
            "extracurricular_activities",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of roadmap planning output"""
        return {
            "executive_summary": "str",
            "grade_wise_milestones": "list",
            "entrance_exam_strategies": "list",
            "higher_education_pathways": "list",
            "subject_selection_guidance": "dict",
            "timeline_overview": "dict",
            "backup_plans": "list",
            "resource_requirements": "dict",
            "progress_monitoring": "dict",
            "next_steps": "list",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.output_parser = JsonOutputParser(
            pydantic_object=EducationalRoadmapPlannerOutput
        )

        # Create the main roadmap planning prompt
        self.planning_prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "current_academic_status",
                "stream_recommendations",
                "career_goals",
                "assessment_insights",
                "contextual_factors",
                "planning_framework",
            ],
            template=self._create_planning_template(),
        )

    def _create_planning_template(self) -> str:
        """Create the comprehensive roadmap planning prompt template"""
        return """You are an expert Academic Planning Specialist with extensive knowledge of the Indian education system. You create detailed, realistic educational roadmaps that guide students from their current grade through higher education, ensuring alignment with their aptitudes, interests, and career goals.

STUDENT PROFILE:
{student_profile}

CURRENT ACADEMIC STATUS:
{current_academic_status}

RECOMMENDED ACADEMIC STREAMS:
{stream_recommendations}

IDENTIFIED CAREER GOALS:
{career_goals}

ASSESSMENT INSIGHTS:
{assessment_insights}

CONTEXTUAL FACTORS:
{contextual_factors}

EDUCATIONAL PLANNING FRAMEWORK:
{planning_framework}

ROADMAP PLANNING PRINCIPLES:

1. HOLISTIC DEVELOPMENT APPROACH:
   - Balance academic rigor with personal growth
   - Include skill development alongside knowledge acquisition
   - Consider extracurricular activities for holistic development
   - Plan for stress management and well-being

2. INDIAN EDUCATION SYSTEM ALIGNMENT:
   - Align with CBSE/ICSE/State board requirements
   - Plan for board exam success (10th and 12th)
   - Strategic preparation for entrance exams
   - Consider reservation policies and quota systems

3. MILESTONE-BASED PLANNING:
   - Create specific, measurable goals for each grade
   - Establish clear timelines and deadlines
   - Build progressive complexity in learning
   - Include regular assessment and course correction

4. CAREER-GOAL ALIGNMENT:
   - Ensure all activities support long-term career objectives
   - Maintain flexibility for evolving interests
   - Include exposure to real-world applications
   - Plan for industry-relevant skill development

5. PRACTICAL CONSIDERATIONS:
   - Factor in family financial situation
   - Consider geographical constraints
   - Plan for resource requirements (books, coaching, technology)
   - Include backup options for contingencies

6. ENTRANCE EXAM STRATEGY:
   - Start preparation at optimal timing
   - Balance board exams with entrance exam prep
   - Include mock tests and performance analysis
   - Plan for multiple exam attempts if needed

IMPORTANT INDIAN EDUCATION CONTEXT:
- Stream selection in 11th grade is crucial for career paths
- Board exam scores affect college admissions
- Entrance exams are highly competitive with limited seats
- Coaching institutes play significant role in preparation
- Merit-based selection with reservation considerations
- Financial aid and scholarship opportunities available

Please provide a comprehensive educational roadmap following this JSON structure:

{format_instructions}

Focus on:
1. Specific, actionable milestones for each grade level
2. Detailed entrance exam preparation strategies
3. Clear timelines with critical decision points
4. Resource requirements and financial planning
5. Backup plans for different scenarios
6. Progress monitoring and adjustment mechanisms

Remember: This roadmap will guide critical educational decisions. Provide practical, achievable plans that balance ambition with realism, considering the student's specific circumstances and the competitive nature of Indian education."""

    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic for educational roadmap planning"""
        # Get previous agent outputs from the agent input
        previous_outputs = validated_input.get("previous_agent_outputs", {})

        # Extract current grade from user data
        user_data = validated_input.get("user_data", {})
        current_grade = user_data.get("current_grade")

        # Extract recommended_streams from academic_stream_advisor output
        recommended_streams = []
        if "academic_stream_advisor" in previous_outputs:
            stream_result = previous_outputs["academic_stream_advisor"]
            if stream_result.status == ProcessingStatus.COMPLETED:
                streams = stream_result.output_data.get("recommended_streams")
                recommended_streams = [
                    stream.get("stream_type")
                    for stream in streams
                    if isinstance(stream, dict)
                ]

        if not recommended_streams:
            recommended_streams = [
                "Science (PCM)",
                "Science (PCB)",
                "Commerce (Math)",
            ]  # Default fallback

        # Extract career_interests from career_pathway_explorer output
        career_interests = []
        if "career_pathway_explorer" in previous_outputs:
            career_result = previous_outputs["career_pathway_explorer"]
            if career_result.status == ProcessingStatus.COMPLETED:
                careers = career_result.output_data.get(
                    "recommended_career_pathways", []
                )
                career_interests = [
                    career.get("career_title")
                    for career in careers
                    if isinstance(career, dict)
                ]

        if not career_interests:
            career_interests = [
                "Engineering",
                "Medicine",
                "Business",
            ]  # Default fallback

        # Create the required_data structure that the rest of your method expects
        validated_input["required_data"] = {
            "current_grade": current_grade,
            "recommended_streams": recommended_streams,
            "career_interests": career_interests,
        }

        # Extract required data
        current_grade = validated_input["required_data"]["current_grade"]
        recommended_streams = validated_input["required_data"]["recommended_streams"]
        career_interests = validated_input["required_data"]["career_interests"]

        # Extract optional context
        optional_data = validated_input["optional_data"]
        previous_outputs = validated_input.get("previous_outputs", {})

        # Get previous agent results for context
        test_interpreter_result = previous_outputs.get("test_score_interpreter")
        stream_advisor_result = previous_outputs.get("academic_stream_advisor")
        career_explorer_result = previous_outputs.get("career_pathway_explorer")

        # Prepare comprehensive inputs for roadmap planning
        student_profile = self._prepare_student_profile(optional_data, current_grade)
        current_academic_status = self._assess_current_academic_status(
            current_grade, optional_data
        )
        stream_recommendations = self._extract_stream_recommendations(
            stream_advisor_result, recommended_streams
        )
        career_goals = self._extract_career_goals(
            career_explorer_result, career_interests
        )
        assessment_insights = self._extract_assessment_insights(
            test_interpreter_result, optional_data
        )
        contextual_factors = self._prepare_contextual_factors(optional_data)
        planning_framework = self._create_planning_framework(current_grade)

        # Add processing note
        self._add_processing_note("Starting comprehensive educational roadmap planning")

        try:
            # Generate roadmap using LLM
            prompt_input = {
                "student_profile": student_profile,
                "current_academic_status": current_academic_status,
                "stream_recommendations": stream_recommendations,
                "career_goals": career_goals,
                "assessment_insights": assessment_insights,
                "contextual_factors": contextual_factors,
                "planning_framework": planning_framework,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            formatted_prompt = self.planning_prompt.format(**prompt_input)

            # Get LLM response
            llm_response = self.llm_model.invoke(formatted_prompt)

            # Convert to dictionary and add metadata
            result = self._parse_llm_response(llm_response)

            # Add roadmap metadata
            result["roadmap_metadata"] = {
                "planner_role": "Academic Planning Specialist",
                "education_system": "Indian Education System",
                "planning_date": datetime.now().isoformat(),
                "current_grade": current_grade,
                "planning_horizon": self._calculate_planning_horizon(current_grade),
                "methodology": "Milestone-based Educational Planning",
                "based_on_assessments": self._list_assessment_sources(
                    test_interpreter_result,
                    stream_advisor_result,
                    career_explorer_result,
                ),
            }

            # Add computational analysis
            result["computational_analysis"] = {
                "timeline_analysis": self._calculate_timeline_metrics(current_grade),
                "entrance_exam_priorities": self._prioritize_entrance_exams(
                    stream_recommendations, career_goals
                ),
                "resource_estimation": self._estimate_resource_requirements(
                    recommended_streams, current_grade
                ),
                "success_probability_factors": self._analyze_success_factors(
                    optional_data, current_grade
                ),
                "critical_decision_points": self._identify_critical_decisions(
                    current_grade
                ),
            }

            relevant_exams = self._extract_relevant_entrance_exams(
                result["entrance_exam_strategies"]
            )
            constraints = {
                "financial": optional_data.get("financial_considerations"),
                "geographical": optional_data.get("geographical_preferences"),
                "family": optional_data.get("family_preferences"),
                "academic_performance": optional_data.get("academic_performance"),
            }

            timeline_result = self.timeline_planning_agent.generate_timeline(
                student_profile=student_profile,
                current_grade=current_grade,
                career_goals=career_goals,
                entrance_exams=relevant_exams,
                constraints=constraints,
            )

            result["timeline_planning"] = timeline_result
            self._add_processing_note(
                "Dynamic timeline planning generated successfully"
            )

            resource_result = self.resource_planning_agent.generate_resource_plan(
                student_profile=student_profile,
                career_pathway=self._summarize_career_pathway(career_explorer_result),
                financial_context=optional_data.get(
                    "financial_considerations", "Middle-class family"
                ),
                location_context=optional_data.get(
                    "geographical_preferences", "Urban India"
                ),
                grade_timeline=f"Grade {current_grade} to Grade 12 + Higher Education",
            )

            result["resource_planning"] = resource_result
            self._add_processing_note(
                "Dynamic resource planning generated successfully"
            )

            # Replace the hardcoded practical_guidance with this dynamic version:
            result["practical_guidance"] = {
                "immediate_actions": result["timeline_planning"][
                    "immediate_action_plan"
                ],
                "resource_optimization": result["resource_planning"][
                    "alternative_resource_options"
                ],
                "monitoring_schedule": result["timeline_planning"][
                    "monthly_review_schedule"
                ],
                "support_system": result["resource_planning"][
                    "support_system_requirements"
                ],
                "financial_planning": result["resource_planning"]["financial_planning"],
            }

            self._add_processing_note(
                "Educational roadmap planning completed successfully"
            )
            return result

        except Exception as e:
            self.logger.error(f"Error in roadmap planning: {str(e)}")
            self._add_processing_note(f"Roadmap planning error: {str(e)}")
            raise

    def _extract_relevant_entrance_exams(
        self, entrance_strategies: List[Dict]
    ) -> List[str]:
        """Extract relevant entrance exams from strategies"""
        exams = []
        for strategy in entrance_strategies:
            if isinstance(strategy, dict):
                exam_name = strategy.get("exam_name")
                if exam_name:
                    exams.append(exam_name)
        return exams

    def _summarize_career_pathway(self, career_explorer_result) -> str:
        """Summarize career pathway for resource planning"""
        if (
            not career_explorer_result
            or career_explorer_result.status != ProcessingStatus.COMPLETED
        ):
            return "General academic pathway with multiple career options"

        output_data = career_explorer_result.output_data
        pathways = output_data.get("recommended_career_pathways", [])

        if pathways and len(pathways) > 0:
            top_pathway = pathways[0]
            if isinstance(top_pathway, dict):
                career_title = top_pathway.get("career_title", "Various careers")
                career_field = top_pathway.get("career_field", "Multiple fields")
                return f"Primary pathway: {career_title} in {career_field}"

        return "Multiple career pathways under consideration"

    def _prepare_student_profile(
        self, optional_data: Dict[str, Any], current_grade: str
    ) -> str:
        """Prepare comprehensive student profile for roadmap planning"""
        profile_parts = []

        # Basic information
        profile_parts.append(f"Current Grade: {current_grade}")

        # Academic performance context
        if optional_data.get("academic_performance"):
            profile_parts.append(
                f"Academic Performance: {optional_data['academic_performance']}"
            )

        # Extracurricular activities
        if optional_data.get("extracurricular_activities"):
            activities = optional_data["extracurricular_activities"]
            if isinstance(activities, list):
                profile_parts.append(f"Current Activities: {', '.join(activities)}")
            else:
                profile_parts.append(f"Current Activities: {activities}")

        # Learning preferences and strengths (from assessments if available)
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

        if optional_data.get("cii_results"):
            top_interests = sorted(
                optional_data["cii_results"].items(), key=lambda x: x[1], reverse=True
            )[:2]
            interest_summary = ", ".join(
                [interest.replace("_", " ").title() for interest, _ in top_interests]
            )
            profile_parts.append(f"Top Interest Areas: {interest_summary}")

        return (
            "\n".join(profile_parts)
            if profile_parts
            else f"Student currently in {current_grade}"
        )

    def _assess_current_academic_status(
        self, current_grade: str, optional_data: Dict[str, Any]
    ) -> str:
        """Assess current academic status and readiness"""
        status_parts = []

        # Grade-specific status
        grade_num = self._extract_grade_number(current_grade)

        if grade_num == 9:
            status_parts.append(
                "Foundation building phase - focusing on concept clarity and study habits"
            )
            status_parts.append(
                "Stream selection awareness stage - exploring different academic paths"
            )
        elif grade_num == 10:
            status_parts.append(
                "Board exam preparation year - crucial for academic foundation"
            )
            status_parts.append(
                "Stream decision timeline - must finalize by end of academic year"
            )
        elif grade_num == 11:
            status_parts.append(
                "Stream specialization year - intensive subject focus required"
            )
            status_parts.append(
                "Entrance exam preparation foundation - building competitive exam readiness"
            )
        elif grade_num == 12:
            status_parts.append(
                "Final preparation year - board exams and entrance exams"
            )
            status_parts.append("College application and admission process management")

        # Academic performance context
        performance = optional_data.get("academic_performance", "").lower()
        if "excellent" in performance or "outstanding" in performance:
            status_parts.append("Strong academic foundation provides excellent options")
        elif "good" in performance or "above average" in performance:
            status_parts.append(
                "Solid academic foundation with room for strategic improvement"
            )
        elif "average" in performance:
            status_parts.append(
                "Needs focused effort to improve competitive positioning"
            )
        elif performance and ("below" in performance or "weak" in performance):
            status_parts.append(
                "Requires intensive support and structured improvement plan"
            )

        return "\n".join(status_parts)

    def _extract_stream_recommendations(
        self, stream_advisor_result, recommended_streams
    ) -> str:
        """Extract and format stream recommendations from previous agent"""
        if (
            stream_advisor_result
            and stream_advisor_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = stream_advisor_result.output_data

            stream_parts = []
            if output_data.get("executive_summary"):
                stream_parts.append(
                    f"Stream Advisory Summary: {output_data['executive_summary']}"
                )

            # Extract recommended streams
            if output_data.get("recommended_streams"):
                stream_parts.append("Recommended Academic Streams:")
                streams = output_data["recommended_streams"]
                if isinstance(streams, list):
                    for i, stream in enumerate(streams[:3], 1):
                        if isinstance(stream, dict):
                            stream_name = stream.get("stream_type", f"Stream {i}")
                            suitability = stream.get(
                                "suitability_score", "Not specified"
                            )
                            stream_parts.append(
                                f"{i}. {stream_name} (Suitability: {suitability})"
                            )

                            # Add career pathways if available
                            if stream.get("career_pathways"):
                                pathways = stream["career_pathways"][
                                    :3
                                ]  # Top 3 pathways
                                stream_parts.append(
                                    f"   Key Career Paths: {', '.join(pathways)}"
                                )

            return "\n".join(stream_parts)
        else:
            # Fallback to basic recommended streams
            if isinstance(recommended_streams, list):
                return f"Recommended Streams: {', '.join(recommended_streams)}"
            elif isinstance(recommended_streams, str):
                return f"Recommended Stream: {recommended_streams}"
            else:
                return "Stream recommendations under analysis"

    def _extract_career_goals(self, career_explorer_result, career_interests) -> str:
        """Extract career goals from career pathway explorer"""
        if (
            career_explorer_result
            and career_explorer_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = career_explorer_result.output_data

            career_parts = []
            if output_data.get("executive_summary"):
                career_parts.append(
                    f"Career Exploration Summary: {output_data['executive_summary']}"
                )

            # Extract top career pathways
            if output_data.get("recommended_career_pathways"):
                career_parts.append("Top Career Pathways:")
                pathways = output_data["recommended_career_pathways"]
                if isinstance(pathways, list):
                    for i, pathway in enumerate(pathways[:3], 1):
                        if isinstance(pathway, dict):
                            career_title = pathway.get("career_title", f"Career {i}")
                            suitability = pathway.get(
                                "suitability_score", "Not specified"
                            )
                            career_parts.append(
                                f"{i}. {career_title} (Suitability: {suitability})"
                            )

                            # Add educational requirements if available
                            if pathway.get("educational_requirements"):
                                edu_reqs = pathway["educational_requirements"][
                                    :2
                                ]  # Top 2 requirements
                                career_parts.append(
                                    f"   Education: {', '.join(edu_reqs)}"
                                )

            return "\n".join(career_parts)
        else:
            # Fallback to basic career interests
            if isinstance(career_interests, list):
                return f"Career Interests: {', '.join(career_interests)}"
            elif isinstance(career_interests, str):
                return f"Career Interest: {career_interests}"
            else:
                return "Career goals under exploration"

    def _extract_assessment_insights(
        self, test_interpreter_result, optional_data: Dict[str, Any]
    ) -> str:
        """Extract key insights from assessment interpretation"""
        if (
            test_interpreter_result
            and test_interpreter_result.status == ProcessingStatus.COMPLETED
        ):
            output_data = test_interpreter_result.output_data

            insight_parts = []
            if output_data.get("executive_summary"):
                insight_parts.append(
                    f"Assessment Overview: {output_data['executive_summary']}"
                )

            # Key recommendations from assessment
            if output_data.get("key_recommendations"):
                insight_parts.append("Assessment-Based Recommendations:")
                recommendations = output_data["key_recommendations"]
                if isinstance(recommendations, list):
                    for rec in recommendations[:3]:  # Top 3 recommendations
                        insight_parts.append(f"- {rec}")

            # Psychological insights relevant to planning
            if output_data.get("psychological_insights"):
                psychological = output_data["psychological_insights"]
                if isinstance(psychological, dict):
                    for key, value in psychological.items():
                        if isinstance(value, str) and len(value) < 150:
                            insight_parts.append(f"Psychological Insight: {value}")
                            break

            return "\n".join(insight_parts)
        else:
            # Basic assessment data if available
            insight_parts = []
            if optional_data.get("dbda_scores"):
                top_aptitudes = sorted(
                    optional_data["dbda_scores"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:2]
                aptitudes = [
                    apt.replace("_", " ").title() for apt, score in top_aptitudes
                ]
                insight_parts.append(f"Top Aptitudes: {', '.join(aptitudes)}")

            if optional_data.get("cii_results"):
                top_interests = sorted(
                    optional_data["cii_results"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:2]
                interests = [
                    interest.replace("_", " ").title()
                    for interest, score in top_interests
                ]
                insight_parts.append(f"Top Interests: {', '.join(interests)}")

            return (
                "\n".join(insight_parts)
                if insight_parts
                else "Assessment insights being analyzed"
            )

    def _prepare_contextual_factors(self, optional_data: Dict[str, Any]) -> str:
        """Prepare contextual factors affecting roadmap planning"""
        factors = []

        # Family preferences and constraints
        if optional_data.get("family_preferences"):
            factors.append(f"Family Preferences: {optional_data['family_preferences']}")

        # Financial considerations
        if optional_data.get("financial_considerations"):
            factors.append(
                f"Financial Context: {optional_data['financial_considerations']}"
            )

        # Geographic constraints
        if optional_data.get("geographical_preferences"):
            factors.append(
                f"Geographic Preferences: {optional_data['geographical_preferences']}"
            )

        # Current extracurricular engagement
        if optional_data.get("extracurricular_activities"):
            factors.append(
                f"Current Activities: {optional_data['extracurricular_activities']}"
            )

        return (
            "\n".join(factors)
            if factors
            else "No specific contextual constraints identified"
        )

    def _create_planning_framework(self, current_grade: str) -> str:
        """Create planning framework based on current grade"""
        grade_num = self._extract_grade_number(current_grade)

        framework_parts = [
            "EDUCATIONAL ROADMAP PLANNING FRAMEWORK:",
            "",
            "GRADE-WISE FOCUS AREAS:",
        ]

        # Add grade-specific focus based on current grade and future grades
        for grade in range(grade_num, 13):  # From current grade to 12th
            if str(grade) in self.grade_focus_mapping:
                grade_info = self.grade_focus_mapping[str(grade)]
                framework_parts.append(f"\nGrade {grade}:")
                framework_parts.append(
                    f"- Academic Priority: {grade_info['academic_priority']}"
                )
                framework_parts.append(
                    f"- Skill Focus: {', '.join(grade_info['skill_focus'])}"
                )
                framework_parts.append(
                    f"- Key Activities: {', '.join(grade_info['preparation_activities'])}"
                )
                framework_parts.append(f"- Timeline: {grade_info['decision_timeline']}")

        # Add entrance exam framework
        framework_parts.extend(
            [
                "",
                "ENTRANCE EXAM PREPARATION FRAMEWORK:",
                "- JEE Preparation: Start foundation in 11th, intensive in 12th",
                "- NEET Preparation: Biology focus from 11th, integrated preparation",
                "- CLAT Preparation: Current affairs and legal awareness from 11th",
                "- Board Exam Balance: Maintain 60% board, 40% entrance exam focus",
                "",
                "HIGHER EDUCATION PATHWAYS:",
                "- Engineering: IITs, NITs, Private Colleges",
                "- Medicine: Government Medical Colleges, Private Medical Colleges",
                "- Business: Top B-Schools, Commerce Programs",
                "- Liberal Arts: Ashoka, O.P. Jindal, DU Colleges",
            ]
        )

        return "\n".join(framework_parts)

    def _extract_grade_number(self, current_grade: str) -> int:
        """Extract numeric grade from grade string"""
        import re

        match = re.search(r"\d+", str(current_grade))
        return int(match.group()) if match else 10

    def _calculate_planning_horizon(self, current_grade: str) -> str:
        """Calculate planning horizon based on current grade"""
        grade_num = self._extract_grade_number(current_grade)
        years_to_12th = 12 - grade_num + 1

        if years_to_12th <= 0:
            return "Post-12th planning (1-4 years)"
        elif years_to_12th == 1:
            return "Immediate planning (1 year to 12th + 4 years higher education)"
        else:
            return f"Long-term planning ({years_to_12th} years to 12th + 4 years higher education)"

    def _list_assessment_sources(
        self, test_result, stream_result, career_result
    ) -> List[str]:
        """List the assessment sources used in planning"""
        sources = []
        if test_result and test_result.status == ProcessingStatus.COMPLETED:
            sources.append("DBDA Aptitude Assessment")
            sources.append("Career Interest Inventory (CII)")
        if stream_result and stream_result.status == ProcessingStatus.COMPLETED:
            sources.append("Academic Stream Analysis")
        if career_result and career_result.status == ProcessingStatus.COMPLETED:
            sources.append("Career Pathway Exploration")
        return sources

    def _calculate_timeline_metrics(self, current_grade: str) -> Dict[str, Any]:
        """Calculate timeline-related metrics"""
        grade_num = self._extract_grade_number(current_grade)

        return {
            "years_to_12th": max(0, 12 - grade_num + 1),
            "years_to_college": max(0, 12 - grade_num + 2),  # +1 year for college entry
            "critical_decision_years": [11, 12] if grade_num <= 11 else [12],
            "preparation_timeline": {
                "stream_selection": (
                    "End of Grade 10" if grade_num <= 10 else "Already decided"
                ),
                "entrance_exam_prep": "Grade 11-12" if grade_num <= 11 else "Grade 12",
                "college_applications": (
                    "Grade 12" if grade_num <= 12 else "Current year"
                ),
            },
        }

    def _prioritize_entrance_exams(
        self, stream_recommendations: str, career_goals: str
    ) -> List[Dict[str, Any]]:
        """Prioritize entrance exams based on streams and career goals"""
        priorities = []

        # Extract likely streams and careers for prioritization
        if "Science (PCM)" in stream_recommendations or "Engineering" in career_goals:
            priorities.append(
                {
                    "exam": "JEE Main",
                    "priority": "High",
                    "preparation_time": "18-24 months",
                    "success_factors": [
                        "Math proficiency",
                        "Physics concepts",
                        "Chemistry fundamentals",
                    ],
                }
            )
            priorities.append(
                {
                    "exam": "JEE Advanced",
                    "priority": "Medium",
                    "preparation_time": "24+ months",
                    "success_factors": [
                        "JEE Main qualification",
                        "Advanced problem solving",
                    ],
                }
            )

        if "Science (PCB)" in stream_recommendations or "Medicine" in career_goals:
            priorities.append(
                {
                    "exam": "NEET UG",
                    "priority": "High",
                    "preparation_time": "18-24 months",
                    "success_factors": [
                        "Biology mastery",
                        "Chemistry concepts",
                        "Physics basics",
                    ],
                }
            )

        if "Commerce" in stream_recommendations or "Business" in career_goals:
            priorities.append(
                {
                    "exam": "CAT",
                    "priority": "Medium",
                    "preparation_time": "12-18 months",
                    "success_factors": [
                        "Quantitative aptitude",
                        "Verbal ability",
                        "Logical reasoning",
                    ],
                }
            )

        return priorities

    def _estimate_resource_requirements(
        self, recommended_streams: str, current_grade: str
    ) -> Dict[str, Any]:
        """Estimate resource requirements for the educational journey"""
        grade_num = self._extract_grade_number(current_grade)

        base_requirements = {
            "financial": {
                "coaching_fees": "₹50,000 - ₹2,00,000 per year",
                "study_materials": "₹10,000 - ₹25,000 total",
                "mock_tests": "₹5,000 - ₹15,000 per year",
                "college_fees": "Varies by institution type",
            },
            "time_commitment": {
                "study_hours_per_day": "6-8 hours for competitive prep",
                "coaching_hours": "3-4 hours if enrolled",
                "self_study_ratio": "60% self-study, 40% guided learning",
            },
            "support_system": [
                "Family support for motivation and logistics",
                "Peer group for healthy competition",
                "Mentor guidance for strategy",
                "Professional counseling for stress management",
            ],
        }

        # Adjust based on streams
        if "Science" in recommended_streams:
            base_requirements["specialized_resources"] = [
                "Laboratory access for practicals",
                "Advanced mathematics coaching",
                "Science competition participation",
            ]

        return base_requirements

    def _analyze_success_factors(
        self, optional_data: Dict[str, Any], current_grade: str
    ) -> List[str]:
        """Analyze factors contributing to success probability"""
        success_factors = []

        # Academic performance factor
        performance = optional_data.get("academic_performance", "").lower()
        if "excellent" in performance:
            success_factors.append(
                "Strong academic foundation provides competitive advantage"
            )
        elif "good" in performance:
            success_factors.append("Solid academic base with potential for improvement")
        else:
            success_factors.append("Academic performance needs focused improvement")

        # Extracurricular engagement
        if optional_data.get("extracurricular_activities"):
            success_factors.append(
                "Active extracurricular engagement shows well-rounded development"
            )

        # Family support
        if optional_data.get("family_preferences"):
            success_factors.append("Family involvement in educational decisions")

        # Time availability (based on grade)
        grade_num = self._extract_grade_number(current_grade)
        if grade_num <= 10:
            success_factors.append(
                "Ample time for strategic preparation and skill building"
            )
        elif grade_num == 11:
            success_factors.append(
                "Adequate time for focused preparation with proper planning"
            )
        else:
            success_factors.append("Limited time requires intensive, focused effort")

        return success_factors

    def _identify_critical_decisions(self, current_grade: str) -> List[Dict[str, str]]:
        """Identify critical decision points in the educational journey"""
        grade_num = self._extract_grade_number(current_grade)
        decisions = []

        if grade_num <= 10:
            decisions.append(
                {
                    "decision": "Stream Selection",
                    "timeline": "End of Grade 10",
                    "impact": "Determines career pathway options",
                    "key_factors": "Aptitude, interest, career goals alignment",
                }
            )

        if grade_num <= 11:
            decisions.append(
                {
                    "decision": "Entrance Exam Selection",
                    "timeline": "Beginning of Grade 11",
                    "impact": "Defines preparation strategy and college options",
                    "key_factors": "Career goals, preparation capacity, success probability",
                }
            )

        if grade_num <= 11:
            decisions.append(
                {
                    "decision": "Coaching vs Self-Study",
                    "timeline": "Grade 11",
                    "impact": "Learning approach and resource allocation",
                    "key_factors": "Learning style, financial capacity, local options",
                }
            )

        decisions.append(
            {
                "decision": "College Selection and Applications",
                "timeline": "Grade 12",
                "impact": "Determines higher education institution",
                "key_factors": "Entrance exam performance, preferences, financial considerations",
            }
        )

        return decisions

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
