from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from agentic_layer.base_agent import BaseAgent
from agentic_layer.school_students.agents.sub_agents.practical_guidance_sub_agent import (
    PracticalGuidanceSubAgent,
)
from agentic_layer.school_students.agents.sub_agents.career_readiness_sub_agent import (
    CareerReadinessSubAgent,
)
from config.agent_config import AgentType, ProcessingStatus


class CareerField(Enum):
    """Major career fields in Indian context"""

    ENGINEERING_TECHNOLOGY = "Engineering & Technology"
    MEDICINE_HEALTHCARE = "Medicine & Healthcare"
    BUSINESS_MANAGEMENT = "Business & Management"
    FINANCE_BANKING = "Finance & Banking"
    RESEARCH_ACADEMIA = "Research & Academia"
    CIVIL_SERVICES = "Civil Services & Government"
    LAW_LEGAL = "Law & Legal Services"
    CREATIVE_ARTS = "Creative Arts & Media"
    SOCIAL_SERVICES = "Social Services & NGO"
    EDUCATION_TRAINING = "Education & Training"
    DEFENSE_SECURITY = "Defense & Security"
    ENTREPRENEURSHIP = "Entrepreneurship & Startups"


class CareerPathway(BaseModel):
    """Individual career pathway with detailed information"""

    career_title: str = Field(description="Specific career title/role")
    career_field: str = Field(description="Broader career field category")
    suitability_score: float = Field(
        description="Suitability based on student profile (0.0-1.0)"
    )
    pathway_description: str = Field(description="What this career involves day-to-day")
    educational_requirements: List[str] = Field(
        description="Required education and qualifications"
    )
    entry_timeline: str = Field(
        description="Time from 12th grade to entry-level position"
    )
    skill_requirements: List[str] = Field(description="Key skills needed for success")
    aptitude_alignment: List[str] = Field(description="How student's aptitudes align")
    interest_alignment: List[str] = Field(description="How student's interests align")
    career_progression: List[str] = Field(description="Typical career advancement path")
    salary_outlook: Dict[str, str] = Field(
        description="Salary ranges at different career stages"
    )
    job_market_outlook: str = Field(description="Future demand and opportunities")
    challenges_considerations: List[str] = Field(
        description="Potential challenges to consider"
    )
    success_factors: List[str] = Field(
        description="What leads to success in this career"
    )
    related_careers: List[str] = Field(description="Similar or related career options")


class CareerExplorationInsights(BaseModel):
    """Insights from career exploration analysis"""

    aptitude_career_mapping: Dict[str, List[str]] = Field(
        description="How aptitudes map to career clusters"
    )
    interest_career_alignment: Dict[str, List[str]] = Field(
        description="How interests align with career options"
    )
    stream_career_pathways: Dict[str, List[str]] = Field(
        description="Career pathways from recommended streams"
    )
    emerging_opportunities: List[str] = Field(
        description="New and emerging career opportunities"
    )
    skill_development_priorities: List[str] = Field(
        description="Skills to develop for target careers"
    )


class CareerPathwayExplorerOutput(BaseModel):
    """Structured output for career pathway exploration"""

    executive_summary: str = Field(
        description="Overview of career exploration findings"
    )
    recommended_career_pathways: List[CareerPathway] = Field(
        description="Top career pathway recommendations"
    )
    career_exploration_insights: CareerExplorationInsights = Field(
        description="Analytical insights"
    )
    career_readiness_assessment: Dict[str, Any] = Field(
        description="Student's readiness for different career paths"
    )
    exploration_activities: List[str] = Field(
        description="Suggested career exploration activities"
    )
    mentorship_recommendations: List[str] = Field(
        description="Types of mentors to seek"
    )
    timeline_planning: Dict[str, Any] = Field(
        description="Career planning timeline considerations"
    )
    decision_support_framework: Dict[str, Any] = Field(
        description="Framework for career decision making"
    )
    next_steps: List[str] = Field(
        description="Immediate next steps for career exploration"
    )


class CareerPathwayExplorerAgent(BaseAgent):
    """
    Career Guidance Specialist for Young Adults Agent that translates stream recommendations
    into specific career possibilities with realistic timelines for school students (grades 9-12).
    Specializes in age-appropriate career exploration and Indian education-career pathway mapping.
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="career_pathway_explorer",
            agent_name="Career Pathway Explorer Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config or {},
        )

        self.practical_guidance_agent = PracticalGuidanceSubAgent(llm_model)
        self.career_readiness_agent = CareerReadinessSubAgent(llm_model)

        # Agent expertise areas
        self.expertise_areas = [
            "Career exploration for Indian school students (grades 9-12)",
            "Stream-to-career pathway mapping",
            "Age-appropriate career guidance (14-18 years)",
            "Educational pathway planning",
            "Career market analysis for young adults",
            "Aptitude-interest-career alignment",
        ]

        # Comprehensive stream-to-career mapping for Indian context
        self.stream_career_mapping = {
            "Science (PCM)": {
                "primary_careers": [
                    "Engineering (All branches)",
                    "Architecture",
                    "Computer Science",
                    "Data Science",
                    "Aerospace Technology",
                    "Robotics",
                    "AI/ML Specialist",
                    "Research Scientist",
                    "Patent Attorney",
                    "Technical Consultant",
                    "Product Manager (Tech)",
                ],
                "emerging_careers": [
                    "Cybersecurity Specialist",
                    "Blockchain Developer",
                    "IoT Engineer",
                    "Space Technology",
                    "Clean Energy Engineer",
                    "Quantum Computing",
                ],
                "entry_pathways": [
                    "JEE Main/Advanced",
                    "State Engineering Entrance",
                    "BITSAT",
                    "Private University Exams",
                ],
            },
            "Science (PCB)": {
                "primary_careers": [
                    "Doctor (MBBS)",
                    "Dentist (BDS)",
                    "Veterinarian",
                    "Pharmacist",
                    "Physiotherapist",
                    "Biotechnologist",
                    "Microbiologist",
                    "Genetic Counselor",
                    "Medical Research",
                    "Clinical Psychology",
                    "Nutrition Specialist",
                    "Public Health",
                ],
                "emerging_careers": [
                    "Bioinformatics Specialist",
                    "Stem Cell Researcher",
                    "Precision Medicine",
                    "Digital Health",
                    "Telemedicine",
                    "Biomedical Engineering",
                ],
                "entry_pathways": [
                    "NEET-UG",
                    "NEET-PG",
                    "State Medical Entrance",
                    "AIIMS",
                    "JIPMER",
                ],
            },
            "Science (PCMB)": {
                "primary_careers": [
                    "Medical Engineering",
                    "Biomedical Engineering",
                    "Biotechnology",
                    "Bioengineering",
                    "Medical Research",
                    "Healthcare Technology",
                    "Pharmaceutical Engineering",
                    "Clinical Data Analysis",
                    "Medical Device Development",
                ],
                "emerging_careers": [
                    "Healthcare AI",
                    "Digital Therapeutics",
                    "Personalized Medicine",
                    "Medical Robotics",
                    "Regenerative Medicine",
                ],
                "entry_pathways": [
                    "JEE + NEET options",
                    "Dual degree programs",
                    "Integrated courses",
                ],
            },
            "Commerce (Math)": {
                "primary_careers": [
                    "Chartered Accountant",
                    "Investment Banker",
                    "Financial Analyst",
                    "Actuary",
                    "Business Analyst",
                    "Management Consultant",
                    "Economics Researcher",
                    "Data Analyst",
                    "Risk Manager",
                    "Corporate Finance",
                    "Entrepreneur",
                ],
                "emerging_careers": [
                    "Fintech Specialist",
                    "Cryptocurrency Analyst",
                    "ESG Analyst",
                    "Algorithmic Trading",
                    "Digital Banking",
                    "Startup Ecosystem",
                ],
                "entry_pathways": [
                    "CA Foundation",
                    "CMA",
                    "Company Secretary",
                    "BBA/BMS",
                    "Economics Honors",
                ],
            },
            "Commerce (No Math)": {
                "primary_careers": [
                    "Human Resources",
                    "Marketing Manager",
                    "Sales Manager",
                    "Business Development",
                    "Retail Management",
                    "Event Management",
                    "Public Relations",
                    "Digital Marketing",
                    "Content Marketing",
                    "Social Media Strategy",
                    "Brand Management",
                ],
                "emerging_careers": [
                    "Influencer Marketing",
                    "Customer Experience Design",
                    "Growth Hacking",
                    "Social Commerce",
                    "Creator Economy",
                    "Sustainable Business",
                ],
                "entry_pathways": [
                    "BBA/BMS",
                    "Mass Communication",
                    "Hotel Management",
                    "Fashion Management",
                ],
            },
            "Arts/Humanities": {
                "primary_careers": [
                    "Civil Services (IAS/IPS)",
                    "Lawyer",
                    "Journalist",
                    "Teacher/Professor",
                    "Social Worker",
                    "Counselor",
                    "Historian",
                    "Archaeologist",
                    "Translator",
                    "Foreign Service",
                    "NGO Leadership",
                    "Policy Researcher",
                ],
                "emerging_careers": [
                    "Policy Analyst",
                    "Social Impact Consultant",
                    "Digital Content Creator",
                    "UX Writer",
                    "Cultural Heritage Manager",
                    "Sustainability Consultant",
                ],
                "entry_pathways": [
                    "UPSC",
                    "CLAT",
                    "Mass Communication",
                    "BA Liberal Arts",
                    "Social Work",
                ],
            },
        }

        # Aptitude-career cluster mapping
        self.aptitude_career_clusters = {
            "computational": [
                "Data Science",
                "Software Engineering",
                "Financial Analysis",
                "Research",
            ],
            "experimental": [
                "Scientific Research",
                "R&D",
                "Laboratory Medicine",
                "Clinical Research",
            ],
            "technical": [
                "Engineering",
                "Technology Development",
                "Technical Consulting",
                "Product Development",
            ],
            "medical": [
                "Healthcare",
                "Medical Research",
                "Biotechnology",
                "Public Health",
            ],
            "administrative": [
                "Management",
                "Civil Services",
                "Operations",
                "Project Management",
            ],
            "humanitarian": [
                "Social Work",
                "NGO",
                "Teaching",
                "Counseling",
                "Public Service",
            ],
            "educational": [
                "Teaching",
                "Training",
                "Educational Technology",
                "Academic Research",
            ],
            "creative": ["Design", "Media", "Arts", "Content Creation", "Marketing"],
            "nature": [
                "Environmental Science",
                "Agriculture",
                "Forestry",
                "Marine Biology",
            ],
            "clerical": [
                "Administration",
                "Documentation",
                "Compliance",
                "Operations Support",
            ],
        }

        # Interest-career alignment mapping
        self.interest_career_alignment = {
            "administrative": ["Management", "Civil Services", "Operations", "HR"],
            "entertainment": [
                "Media",
                "Film",
                "Television",
                "Event Management",
                "Sports",
            ],
            "defense": ["Military", "Police", "Security Services", "Intelligence"],
            "sports": ["Sports Management", "Fitness", "Sports Medicine", "Coaching"],
            "creative": ["Design", "Arts", "Architecture", "Fashion", "Media"],
            "performing": ["Theatre", "Music", "Dance", "Media", "Entertainment"],
            "medical": ["Healthcare", "Medicine", "Research", "Biotechnology"],
            "technical": ["Engineering", "Technology", "R&D", "Innovation"],
            "experimental": ["Research", "Science", "Laboratory", "Innovation"],
            "computational": [
                "IT",
                "Data Science",
                "Analytics",
                "Software Development",
            ],
            "humanitarian": ["Social Work", "NGO", "Public Service", "Community Work"],
            "educational": ["Teaching", "Training", "Academic Research", "EdTech"],
            "nature": ["Environmental", "Agriculture", "Biology", "Conservation"],
            "clerical": ["Administration", "Documentation", "Support Services"],
        }

    def _define_required_inputs(self) -> List[str]:
        """Required inputs for career pathway exploration"""
        return ["dbda_scores", "cii_results"]

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that enhance career exploration"""
        return [
            "current_grade",
            "academic_performance",
            "extracurricular_activities",
            "career_aspirations",
            "family_background",
            "geographical_preferences",
            "financial_considerations",
            "previous_agent_outputs",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of career exploration output"""
        return {
            "executive_summary": "str",
            "recommended_career_pathways": "list",
            "career_exploration_insights": "dict",
            "career_readiness_assessment": "dict",
            "exploration_activities": "list",
            "mentorship_recommendations": "list",
            "timeline_planning": "dict",
            "decision_support_framework": "dict",
            "next_steps": "list",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.output_parser = JsonOutputParser(
            pydantic_object=CareerPathwayExplorerOutput
        )

        # Create the main career exploration prompt
        self.exploration_prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "assessment_analysis",
                "stream_recommendations",
                "aptitude_insights",
                "interest_patterns",
                "career_context",
                "exploration_framework",
            ],
            template=self._create_exploration_template(),
        )

    def _create_exploration_template(self) -> str:
        """Create the comprehensive career exploration prompt template"""
        return """You are an expert Career Guidance Specialist specializing in helping school students (grades 9-12) explore career pathways. Your role is to translate assessment results and stream recommendations into specific, age-appropriate career possibilities with realistic timelines and practical guidance.

STUDENT PROFILE:
{student_profile}

ASSESSMENT ANALYSIS:
{assessment_analysis}

RECOMMENDED ACADEMIC STREAMS:
{stream_recommendations}

APTITUDE INSIGHTS:
{aptitude_insights}

INTEREST PATTERNS:
{interest_patterns}

CAREER EXPLORATION CONTEXT:
{career_context}

CAREER EXPLORATION FRAMEWORK:
{exploration_framework}

CAREER EXPLORATION GUIDELINES:

1. AGE-APPROPRIATE APPROACH (14-18 years):
   - Use inspiring but realistic language
   - Focus on exploration rather than final decisions
   - Emphasize growth potential and skill development
   - Address common teenage concerns about career choices
   - Provide hope while being honest about challenges

2. INDIAN EDUCATION CONTEXT:
   - Align career pathways with Indian educational system
   - Consider entrance exams and admission processes
   - Include both traditional and emerging career options
   - Factor in family expectations and societal pressures
   - Address myths about certain careers being "superior"

3. COMPREHENSIVE CAREER MAPPING:
   - Connect aptitudes and interests to specific careers
   - Provide multiple pathways to similar career goals
   - Include timeline from 12th grade to career entry
   - Address skill development requirements
   - Consider market demand and future opportunities

4. PRACTICAL CONSIDERATIONS:
   - Include salary expectations and career progression
   - Address challenges and success factors
   - Provide exploration activities and next steps
   - Suggest mentorship and guidance opportunities
   - Consider geographical and financial constraints

5. BALANCED PERSPECTIVE:
   - Present both opportunities and challenges honestly
   - Include traditional and non-traditional career paths
   - Address gender stereotypes where relevant
   - Encourage exploration of multiple options
   - Support informed decision-making

IMPORTANT CAREER EXPLORATION PRINCIPLES:
- Every student has unique potential and multiple viable career paths
- Career exploration is a process, not a one-time decision
- Skills can be developed; interests can evolve
- Success is possible in any field with the right approach
- Early exploration leads to better career decisions

Please provide comprehensive career pathway exploration following this JSON structure:

{format_instructions}

Focus on:
1. Specific career recommendations with clear rationale
2. Practical pathways from student's current position to career goals
3. Age-appropriate exploration activities and next steps
4. Realistic timelines and milestone planning
5. Encouragement balanced with honest assessment of requirements
6. Multiple options to reduce pressure and increase possibilities

Remember: This exploration should inspire the student while providing practical, actionable guidance for their career journey."""

    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic for career pathway exploration"""

        # Extract required data
        dbda_scores = validated_input["required_data"]["dbda_scores"]
        cii_results = validated_input["required_data"]["cii_results"]

        # Extract optional context
        optional_data = validated_input["optional_data"]
        previous_outputs = validated_input.get("previous_outputs", {})

        # Get previous agent results
        test_interpreter_result = previous_outputs.get("test_score_interpreter")
        stream_advisor_result = previous_outputs.get("academic_stream_advisor")

        # Prepare comprehensive inputs for career exploration
        student_profile = self._prepare_student_profile(optional_data)
        assessment_analysis = self._extract_assessment_analysis(
            test_interpreter_result, dbda_scores, cii_results
        )
        stream_recommendations = self._extract_stream_recommendations(
            stream_advisor_result
        )
        aptitude_insights = self._analyze_aptitude_insights(dbda_scores)
        interest_patterns = self._analyze_interest_patterns(cii_results)
        career_context = self._prepare_career_context(optional_data)
        exploration_framework = self._create_exploration_framework()

        # Add processing note
        self._add_processing_note("Starting comprehensive career pathway exploration")

        try:
            # Generate career exploration using LLM
            prompt_input = {
                "student_profile": student_profile,
                "assessment_analysis": assessment_analysis,
                "stream_recommendations": stream_recommendations,
                "aptitude_insights": aptitude_insights,
                "interest_patterns": interest_patterns,
                "career_context": career_context,
                "exploration_framework": exploration_framework,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            formatted_prompt = self.exploration_prompt.format(**prompt_input)

            # Get LLM response
            llm_response = self.llm_model.invoke(formatted_prompt)

            # Convert to dictionary and add metadata
            result = self._parse_llm_response(llm_response)

            # Add career exploration metadata
            result["exploration_metadata"] = {
                "explorer_role": "Career Guidance Specialist for Young Adults",
                "target_age_group": "School Students (14-18 years)",
                "exploration_date": datetime.now().isoformat(),
                "methodology": "Aptitude-Interest-Stream Integration Career Mapping",
                "based_on_assessments": [
                    "DBDA Aptitude Test",
                    "Career Interest Inventory (CII)",
                ],
                "education_system_context": "Indian Academic System",
                "career_fields_covered": len(self.stream_career_mapping),
            }

            # Add computational analysis
            result["computational_analysis"] = {
                "aptitude_career_matching": self._calculate_aptitude_career_scores(
                    dbda_scores
                ),
                "interest_career_alignment": self._calculate_interest_career_scores(
                    cii_results
                ),
                "stream_pathway_analysis": self._analyze_stream_pathways(
                    stream_recommendations, dbda_scores, cii_results
                ),
                "career_readiness_scores": self._calculate_career_readiness(
                    dbda_scores, cii_results, optional_data
                ),
                "top_career_recommendations": self._get_top_career_matches(
                    dbda_scores, cii_results, stream_recommendations
                ),
            }

            student_data = {
                "profile": self._prepare_student_profile(optional_data),
                "grade": optional_data.get("current_grade"),
                "academic_performance": optional_data.get("academic_performance"),
                "activities": optional_data.get("extracurricular_activities"),
                "aspirations": optional_data.get("career_aspirations"),
                "constraints": {
                    "geographical": optional_data.get("geographical_preferences"),
                    "financial": optional_data.get("financial_considerations"),
                    "family": optional_data.get("family_background"),
                },
            }

            assessment_data = {
                "dbda_scores": dbda_scores,
                "cii_results": cii_results,
                "aptitude_insights": aptitude_insights,
                "interest_patterns": interest_patterns,
            }

            result["practical_guidance"] = (
                self.practical_guidance_agent.generate_guidance(
                    student_profile=self._prepare_student_profile(optional_data),
                    career_recommendations=result["recommended_career_pathways"],
                    assessment_data=assessment_data,
                    context=student_data["constraints"],
                )
            )
            self._add_processing_note(
                "Dynamic practical guidance generated successfully"
            )

            career_readiness_result = self.career_readiness_agent.assess_readiness(
                student_data=student_data,
                career_pathways=result["recommended_career_pathways"],
                assessment_scores=assessment_data,
            )

            # Update the career_readiness_assessment section
            result["career_readiness_assessment"] = career_readiness_result
            self._add_processing_note("Dynamic career readiness assessment completed")

            self._add_processing_note(
                "Career pathway exploration completed successfully"
            )
            return result

        except Exception as e:
            self.logger.error(f"Error in career exploration: {str(e)}")
            self._add_processing_note(f"Career exploration error: {str(e)}")
            raise

    def _prepare_student_profile(self, optional_data: Dict[str, Any]) -> str:
        """Prepare comprehensive student profile for career exploration"""
        profile_parts = []

        # Basic information
        grade = optional_data.get("current_grade", "Not specified")
        profile_parts.append(f"Current Grade: {grade}")

        # Academic performance
        if optional_data.get("academic_performance"):
            profile_parts.append(
                f"Academic Performance: {optional_data['academic_performance']}"
            )

        # Extracurricular activities
        if optional_data.get("extracurricular_activities"):
            activities = optional_data["extracurricular_activities"]
            if isinstance(activities, list):
                profile_parts.append(
                    f"Extracurricular Activities: {', '.join(activities)}"
                )
            else:
                profile_parts.append(f"Extracurricular Activities: {activities}")

        # Career aspirations
        if optional_data.get("career_aspirations"):
            profile_parts.append(
                f"Current Career Interests: {optional_data['career_aspirations']}"
            )

        # Family background context
        if optional_data.get("family_background"):
            profile_parts.append(
                f"Family Context: {optional_data['family_background']}"
            )

        return (
            "\n".join(profile_parts)
            if profile_parts
            else "Basic student profile available for career exploration"
        )

    def _extract_assessment_analysis(
        self,
        test_interpreter_result,
        dbda_scores: Dict[str, Any],
        cii_results: Dict[str, Any],
    ) -> str:
        """Extract key insights from test interpretation for career exploration"""
        if (
            not test_interpreter_result
            or test_interpreter_result.status != ProcessingStatus.COMPLETED
        ):
            # Provide basic analysis if no interpreter results available
            analysis_parts = ["Assessment analysis based on raw scores:"]

            # Analyze DBDA scores
            top_aptitudes = sorted(
                dbda_scores.items(), key=lambda x: x[1], reverse=True
            )[:3]
            analysis_parts.append("Top Aptitude Areas:")
            for aptitude, score in top_aptitudes:
                analysis_parts.append(
                    f"- {aptitude.replace('_', ' ').title()}: {score}/10"
                )

            # Analyze CII results
            top_interests = sorted(
                cii_results.items(), key=lambda x: x[1], reverse=True
            )[:3]
            analysis_parts.append("Top Interest Areas:")
            for interest, score in top_interests:
                analysis_parts.append(
                    f"- {interest.replace('_', ' ').title()}: {score}/10"
                )

            return "\n".join(analysis_parts)

        output_data = test_interpreter_result.output_data
        analysis_parts = []

        # Executive summary
        if output_data.get("executive_summary"):
            analysis_parts.append(
                f"Assessment Overview: {output_data['executive_summary']}"
            )

        # Aptitude analysis
        if output_data.get("aptitude_analysis"):
            analysis_parts.append("Aptitude Analysis Summary:")
            aptitude_info = output_data["aptitude_analysis"]
            if isinstance(aptitude_info, dict):
                for key, value in aptitude_info.items():
                    if isinstance(value, str) and len(value) < 200:
                        analysis_parts.append(f"- {key}: {value}")

        # Interest analysis
        if output_data.get("interest_analysis"):
            analysis_parts.append("Interest Analysis Summary:")
            interest_info = output_data["interest_analysis"]
            if isinstance(interest_info, dict):
                for key, value in interest_info.items():
                    if isinstance(value, str) and len(value) < 200:
                        analysis_parts.append(f"- {key}: {value}")

        # Key recommendations from test interpretation
        if output_data.get("key_recommendations"):
            analysis_parts.append("Assessment-Based Recommendations:")
            recommendations = output_data["key_recommendations"]
            if isinstance(recommendations, list):
                for rec in recommendations[:3]:  # Top 3 recommendations
                    analysis_parts.append(f"- {rec}")

        return (
            "\n".join(analysis_parts)
            if analysis_parts
            else "Basic assessment analysis available"
        )

    def _extract_stream_recommendations(self, stream_advisor_result) -> str:
        """Extract stream recommendations for career pathway mapping"""
        if (
            not stream_advisor_result
            or stream_advisor_result.status != ProcessingStatus.COMPLETED
        ):
            return "No stream recommendations available from previous analysis"

        output_data = stream_advisor_result.output_data
        stream_parts = []

        # Executive summary from stream advisor
        if output_data.get("executive_summary"):
            stream_parts.append(
                f"Stream Advisor Summary: {output_data['executive_summary']}"
            )

        # Recommended streams
        if output_data.get("recommended_streams"):
            stream_parts.append("Recommended Academic Streams:")
            streams = output_data["recommended_streams"]
            if isinstance(streams, list):
                for i, stream in enumerate(streams[:3], 1):  # Top 3 streams
                    if isinstance(stream, dict):
                        stream_name = stream.get("stream_type", f"Stream {i}")
                        suitability = stream.get("suitability_score", "Not specified")
                        stream_parts.append(
                            f"{i}. {stream_name} (Suitability: {suitability})"
                        )

                        # Add supporting reasons if available
                        if stream.get("primary_strengths_supporting"):
                            stream_parts.append(
                                f"   Supporting Strengths: {', '.join(stream['primary_strengths_supporting'][:2])}"
                            )

        # Computational analysis if available
        if output_data.get("computational_analysis", {}).get(
            "top_3_recommended_streams"
        ):
            top_streams = output_data["computational_analysis"][
                "top_3_recommended_streams"
            ]
            stream_parts.append("Top Stream Matches:")
            for stream_info in top_streams:
                if isinstance(stream_info, dict):
                    stream_name = stream_info.get("stream", "Unknown")
                    score = stream_info.get("suitability_score", 0)
                    stream_parts.append(
                        f"- {stream_name}: {score:.2f} suitability score"
                    )

        return (
            "\n".join(stream_parts)
            if stream_parts
            else "Stream recommendations under analysis"
        )

    def _analyze_aptitude_insights(self, dbda_scores: Dict[str, Any]) -> str:
        """Analyze aptitude insights for career mapping"""
        if not dbda_scores:
            return "No aptitude scores available"

        insights_parts = ["Aptitude-Based Career Insights:"]

        # Identify top aptitudes
        valid_scores = {k: v for k, v in dbda_scores.items() if v is not None}
        top_aptitudes = sorted(valid_scores.items(), key=lambda x: x[1], reverse=True)[
            :4
        ]

        for aptitude, score in top_aptitudes:
            aptitude_clean = aptitude.replace("_", " ").title()
            insights_parts.append(f"\n{aptitude_clean} (Score: {score}/10):")

            # Map to career clusters
            if aptitude in self.aptitude_career_clusters:
                career_clusters = self.aptitude_career_clusters[aptitude][
                    :3
                ]  # Top 3 clusters
                insights_parts.append(
                    f"  Relevant Career Clusters: {', '.join(career_clusters)}"
                )

            # Add interpretation
            if score >= 8:
                insights_parts.append(
                    f"  Strong aptitude - excellent foundation for related careers"
                )
            elif score >= 6:
                insights_parts.append(
                    f"  Good aptitude - suitable for related career paths"
                )
            else:
                insights_parts.append(
                    f"  Developing aptitude - could be strengthened with focused effort"
                )

        return "\n".join(insights_parts)

    def _analyze_interest_patterns(self, cii_results: Dict[str, Any]) -> str:
        """Analyze interest patterns for career alignment"""
        if not cii_results:
            return "No interest data available"

        patterns_parts = ["Interest-Based Career Patterns:"]

        # Identify high interest areas
        high_interests = [
            (interest, score) for interest, score in cii_results.items() if score >= 6
        ]
        high_interests.sort(key=lambda x: x[1], reverse=True)

        if not high_interests:
            # If no high interests, show top 3 relative interests
            high_interests = sorted(
                cii_results.items(), key=lambda x: x[1], reverse=True
            )[:3]
            patterns_parts.append("Top Relative Interest Areas:")
        else:
            patterns_parts.append("High Interest Areas:")

        for interest, score in high_interests[:4]:  # Top 4 interests
            interest_clean = interest.replace("_", " ").title()
            patterns_parts.append(f"\n{interest_clean} (Score: {score}/10):")

            # Map to career areas
            if interest in self.interest_career_alignment:
                career_areas = self.interest_career_alignment[interest][
                    :3
                ]  # Top 3 areas
                patterns_parts.append(
                    f"  Aligned Career Areas: {', '.join(career_areas)}"
                )

            # Add motivation insight
            if score >= 7:
                patterns_parts.append(
                    f"  High intrinsic motivation for related activities"
                )
            elif score >= 5:
                patterns_parts.append(
                    f"  Good interest level - could develop into strong motivation"
                )
            else:
                patterns_parts.append(f"  Emerging interest - worth exploring further")

        return "\n".join(patterns_parts)

    def _prepare_career_context(self, optional_data: Dict[str, Any]) -> str:
        """Prepare contextual factors for career exploration"""
        context_parts = []

        # Geographic preferences
        if optional_data.get("geographical_preferences"):
            context_parts.append(
                f"Geographic Preferences: {optional_data['geographical_preferences']}"
            )

        # Financial considerations
        if optional_data.get("financial_considerations"):
            context_parts.append(
                f"Financial Context: {optional_data['financial_considerations']}"
            )

        # Family background and expectations
        if optional_data.get("family_background"):
            context_parts.append(
                f"Family Background: {optional_data['family_background']}"
            )

        # Current career interests/aspirations
        if optional_data.get("career_aspirations"):
            context_parts.append(
                f"Current Career Interests: {optional_data['career_aspirations']}"
            )

        return (
            "\n".join(context_parts)
            if context_parts
            else "No specific contextual constraints identified"
        )

    def _create_exploration_framework(self) -> str:
        """Create career exploration framework for the agent"""
        framework = """
Career Exploration Framework for School Students:

1. STREAM-CAREER PATHWAY MAPPING:
   - Science (PCM): Engineering, Technology, Research, Analytics
   - Science (PCB): Medicine, Healthcare, Biotechnology, Life Sciences  
   - Science (PCMB): Medical Engineering, Interdisciplinary Research
   - Commerce (Math): Finance, Business Analytics, Consulting, Economics
   - Commerce (No Math): Management, Marketing, HR, Entrepreneurship
   - Arts/Humanities: Civil Services, Law, Media, Social Work, Education

2. CAREER EXPLORATION CRITERIA:
   - Aptitude-Interest Alignment Score
   - Educational Pathway Clarity
   - Market Demand and Future Outlook
   - Entry Timeline and Requirements
   - Skill Development Feasibility

3. AGE-APPROPRIATE CONSIDERATIONS:
   - Allow for interest evolution over time
   - Focus on broad career families rather than narrow specializations
   - Emphasize skill development over final career decisions
   - Address common teenage concerns about future choices

4. INDIAN EDUCATION CONTEXT:
   - Entrance exam requirements and preparation
   - College admission processes and criteria
   - Traditional vs emerging career opportunities
   - Family expectations vs individual interests

5. CAREER READINESS FACTORS:
   - Academic foundation strength
   - Interest consistency and intensity
   - Skill development potential
   - Support system availability
"""
        return framework

    def _calculate_aptitude_career_scores(
        self, dbda_scores: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate career compatibility scores based on aptitudes"""
        career_scores = {}

        # Map aptitudes to career clusters and calculate scores
        for career_cluster in [
            "Engineering",
            "Medicine",
            "Business",
            "Arts",
            "Research",
            "Technology",
        ]:
            score = 0.0
            relevant_aptitudes = []

            if career_cluster == "Engineering":
                relevant_aptitudes = ["technical", "computational", "experimental"]
            elif career_cluster == "Medicine":
                relevant_aptitudes = ["medical", "experimental", "humanitarian"]
            elif career_cluster == "Business":
                relevant_aptitudes = ["administrative", "computational", "humanitarian"]
            elif career_cluster == "Arts":
                relevant_aptitudes = ["creative", "performing", "entertainment"]
            elif career_cluster == "Research":
                relevant_aptitudes = ["experimental", "computational", "nature"]
            elif career_cluster == "Technology":
                relevant_aptitudes = ["technical", "computational", "creative"]

            # Calculate weighted score
            for aptitude in relevant_aptitudes:
                if aptitude in dbda_scores:
                    score += dbda_scores[aptitude] / 10.0

            career_scores[career_cluster] = round(
                score / len(relevant_aptitudes) if relevant_aptitudes else 0, 3
            )

        return career_scores

    def _calculate_interest_career_scores(
        self, cii_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate career motivation scores based on interests"""
        career_scores = {}

        # Map interests to career areas
        for career_area in [
            "Healthcare",
            "Technology",
            "Business",
            "Creative",
            "Social Service",
            "Research",
        ]:
            score = 0.0
            relevant_interests = []

            if career_area == "Healthcare":
                relevant_interests = ["medical", "humanitarian", "experimental"]
            elif career_area == "Technology":
                relevant_interests = ["technical", "computational", "experimental"]
            elif career_area == "Business":
                relevant_interests = ["administrative", "clerical", "computational"]
            elif career_area == "Creative":
                relevant_interests = ["creative", "performing", "entertainment"]
            elif career_area == "Social Service":
                relevant_interests = ["humanitarian", "educational", "defense"]
            elif career_area == "Research":
                relevant_interests = ["experimental", "nature", "computational"]

            # Calculate weighted score
            for interest in relevant_interests:
                if interest in cii_results:
                    score += cii_results[interest] / 10.0

            career_scores[career_area] = round(
                score / len(relevant_interests) if relevant_interests else 0, 3
            )

        return career_scores

    def _analyze_stream_pathways(
        self,
        stream_recommendations: str,
        dbda_scores: Dict[str, Any],
        cii_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze career pathways from recommended streams"""
        analysis = {
            "stream_career_alignment": {},
            "pathway_feasibility": {},
            "skill_requirements": {},
        }

        # Extract stream names from recommendations (simplified parsing)
        recommended_streams = []
        if "Science (PCM)" in stream_recommendations:
            recommended_streams.append("Science (PCM)")
        if "Science (PCB)" in stream_recommendations:
            recommended_streams.append("Science (PCB)")
        if "Commerce" in stream_recommendations:
            recommended_streams.append("Commerce")
        if "Arts" in stream_recommendations or "Humanities" in stream_recommendations:
            recommended_streams.append("Arts/Humanities")

        # Analyze each recommended stream
        for stream in recommended_streams:
            if stream in self.stream_career_mapping:
                stream_info = self.stream_career_mapping[stream]
                analysis["stream_career_alignment"][stream] = stream_info[
                    "primary_careers"
                ][:5]
                analysis["pathway_feasibility"][stream] = (
                    self._assess_pathway_feasibility(stream, dbda_scores, cii_results)
                )

        return analysis

    def _assess_pathway_feasibility(
        self, stream: str, dbda_scores: Dict[str, Any], cii_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess feasibility of career pathways from a stream"""
        feasibility = {
            "high_feasibility": [],
            "moderate_feasibility": [],
            "requires_development": [],
        }

        # Simple feasibility assessment based on scores
        if stream == "Science (PCM)":
            if (
                dbda_scores.get("technical", 0) >= 7
                and dbda_scores.get("computational", 0) >= 6
            ):
                feasibility["high_feasibility"].append(
                    "Engineering and Technology careers"
                )
            elif dbda_scores.get("technical", 0) >= 5:
                feasibility["moderate_feasibility"].append(
                    "Engineering with focused preparation"
                )
            else:
                feasibility["requires_development"].append(
                    "Technical and mathematical skills"
                )

        elif stream == "Science (PCB)":
            if (
                dbda_scores.get("medical", 0) >= 7
                and cii_results.get("medical", 0) >= 7
            ):
                feasibility["high_feasibility"].append("Medical and Healthcare careers")
            elif dbda_scores.get("medical", 0) >= 5:
                feasibility["moderate_feasibility"].append(
                    "Healthcare with dedicated preparation"
                )
            else:
                feasibility["requires_development"].append(
                    "Medical aptitude and interest"
                )

        return feasibility

    def _calculate_career_readiness(
        self,
        dbda_scores: Dict[str, Any],
        cii_results: Dict[str, Any],
        optional_data: Dict[str, Any],
    ) -> Dict[str, float]:
        """Calculate readiness scores for different career paths"""
        readiness_scores = {}

        # Calculate readiness for major career paths
        career_paths = [
            "Engineering",
            "Medicine",
            "Business",
            "Arts",
            "Research",
            "Technology",
        ]

        for path in career_paths:
            base_score = 0.5  # Base readiness

            # Add aptitude component
            if path == "Engineering":
                aptitude_boost = (
                    dbda_scores.get("technical", 0)
                    + dbda_scores.get("computational", 0)
                ) / 20
            elif path == "Medicine":
                aptitude_boost = (
                    dbda_scores.get("medical", 0) + dbda_scores.get("humanitarian", 0)
                ) / 20
            elif path == "Business":
                aptitude_boost = (
                    dbda_scores.get("administrative", 0)
                    + dbda_scores.get("computational", 0)
                ) / 20
            else:
                aptitude_boost = 0.1

            # Add interest component
            if path == "Engineering":
                interest_boost = (
                    cii_results.get("technical", 0)
                    + cii_results.get("computational", 0)
                ) / 20
            elif path == "Medicine":
                interest_boost = (
                    cii_results.get("medical", 0) + cii_results.get("humanitarian", 0)
                ) / 20
            elif path == "Business":
                interest_boost = (
                    cii_results.get("administrative", 0)
                    + cii_results.get("clerical", 0)
                ) / 20
            else:
                interest_boost = 0.1

            # Calculate final readiness
            readiness_scores[path] = round(
                min(1.0, base_score + aptitude_boost + interest_boost), 3
            )

        return readiness_scores

    def _get_top_career_matches(
        self,
        dbda_scores: Dict[str, Any],
        cii_results: Dict[str, Any],
        stream_recommendations: str,
    ) -> List[Dict[str, Any]]:
        """Get top career matches based on all factors"""
        career_matches = []

        # Calculate combined scores for major careers
        major_careers = [
            "Software Engineer",
            "Doctor",
            "Business Analyst",
            "Teacher",
            "Researcher",
            "Designer",
            "Civil Servant",
            "Consultant",
        ]

        for career in major_careers:
            # Simple scoring logic (you can make this more sophisticated)
            aptitude_score = self._get_career_aptitude_score(career, dbda_scores)
            interest_score = self._get_career_interest_score(career, cii_results)
            combined_score = (aptitude_score * 0.6) + (interest_score * 0.4)

            career_matches.append(
                {
                    "career": career,
                    "combined_score": round(combined_score, 3),
                    "aptitude_score": round(aptitude_score, 3),
                    "interest_score": round(interest_score, 3),
                    "match_level": (
                        "High"
                        if combined_score >= 0.7
                        else "Moderate" if combined_score >= 0.5 else "Low"
                    ),
                }
            )

        # Sort by combined score and return top 5
        career_matches.sort(key=lambda x: x["combined_score"], reverse=True)
        return career_matches[:5]

    def _get_career_aptitude_score(
        self, career: str, dbda_scores: Dict[str, Any]
    ) -> float:
        """Get aptitude score for a specific career"""
        career_aptitude_mapping = {
            "Software Engineer": ["technical", "computational"],
            "Doctor": ["medical", "experimental"],
            "Business Analyst": ["administrative", "computational"],
            "Teacher": ["educational", "humanitarian"],
            "Researcher": ["experimental", "computational"],
            "Designer": ["creative", "performing"],
            "Civil Servant": ["administrative", "humanitarian"],
            "Consultant": ["administrative", "computational"],
        }

        relevant_aptitudes = career_aptitude_mapping.get(career, ["computational"])
        scores = [dbda_scores.get(apt, 5) for apt in relevant_aptitudes]
        return sum(scores) / (len(scores) * 10)

    def _get_career_interest_score(
        self, career: str, cii_results: Dict[str, Any]
    ) -> float:
        """Get interest score for a specific career"""
        career_interest_mapping = {
            "Software Engineer": ["technical", "computational"],
            "Doctor": ["medical", "humanitarian"],
            "Business Analyst": ["administrative", "computational"],
            "Teacher": ["educational", "humanitarian"],
            "Researcher": ["experimental", "computational"],
            "Designer": ["creative", "performing"],
            "Civil Servant": ["administrative", "humanitarian"],
            "Consultant": ["administrative", "computational"],
        }

        relevant_interests = career_interest_mapping.get(career, ["computational"])
        scores = [cii_results.get(interest, 5) for interest in relevant_interests]
        return sum(scores) / (len(scores) * 10)

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
