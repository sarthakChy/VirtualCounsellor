from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from agentic_layer.base_agent import BaseAgent
from agentic_layer.school_students.agents.sub_agents.stream_decision_support_sub_agent import (
    StreamDecisionSupportSubAgent,
)
from agentic_layer.school_students.agents.sub_agents.parental_alignment_sub_agent import (
    ParentalAlignmentSubAgent,
)
from config.agent_config import AgentType, ProcessingStatus


class StreamType(Enum):
    """Academic stream types in Indian education system"""

    SCIENCE_PCM = "Science (Physics, Chemistry, Mathematics)"
    SCIENCE_PCB = "Science (Physics, Chemistry, Biology)"
    SCIENCE_PCMB = "Science (Physics, Chemistry, Mathematics, Biology)"
    COMMERCE_MATH = "Commerce with Mathematics"
    COMMERCE_NO_MATH = "Commerce without Mathematics"
    ARTS_HUMANITIES = "Arts/Humanities"
    VOCATIONAL = "Vocational/Technical"


class StreamRecommendation(BaseModel):
    """Individual stream recommendation with details"""

    stream_type: str = Field(description="Type of academic stream")
    suitability_score: float = Field(description="Suitability score 0.0-1.0")
    primary_strengths_supporting: List[str] = Field(
        description="Key strengths that support this stream"
    )
    interest_alignment: List[str] = Field(
        description="How interests align with this stream"
    )
    career_pathways: List[str] = Field(
        description="Major career pathways from this stream"
    )
    subject_requirements: List[str] = Field(
        description="Specific subjects required/recommended"
    )
    challenges_to_consider: List[str] = Field(
        description="Potential challenges in this stream"
    )
    success_predictors: List[str] = Field(
        description="Factors that predict success in this stream"
    )


class StreamAdvisorOutput(BaseModel):
    """Structured output for academic stream advice"""

    executive_summary: str = Field(
        description="Brief overview of stream recommendations"
    )
    recommended_streams: List[StreamRecommendation] = Field(
        description="Ranked stream recommendations"
    )
    stream_comparison_matrix: Dict[str, Any] = Field(
        description="Comparative analysis of suitable streams"
    )
    subject_wise_guidance: Dict[str, Any] = Field(
        description="Guidance for specific subjects within streams"
    )
    parental_discussion_points: List[str] = Field(
        description="Key points to discuss with parents"
    )
    decision_timeline: Dict[str, Any] = Field(
        description="Timeline for stream selection decision"
    )
    backup_options: List[str] = Field(
        description="Alternative options if primary choices don't work"
    )
    next_steps: List[str] = Field(description="Immediate action items for the student")


class AcademicStreamAdvisorAgent(BaseAgent):
    """
    Academic Counselor and Stream Specialist Agent for recommending optimal academic streams
    (Science/Commerce/Arts) based on test results and interests for Indian school students.
    Specializes in mapping aptitude-interest combinations to academic pathways.
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="academic_stream_advisor",
            agent_name="Academic Stream Advisor Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config or {},
        )
        self.decision_support_agent = StreamDecisionSupportSubAgent(llm_model)
        self.parental_alignment_agent = ParentalAlignmentSubAgent(llm_model)

        # Agent expertise areas
        self.expertise_areas = [
            "Academic stream selection for Indian education system",
            "Aptitude-stream mapping and career pathway analysis",
            "Subject combination optimization",
            "Performance prediction and success factors",
            "Parent-student counseling for stream decisions",
            "Alternative pathway identification",
        ]

        # Stream-subject mapping for Indian education system
        self.stream_subjects = {
            "Science (PCM)": {
                "core_subjects": ["Physics", "Chemistry", "Mathematics"],
                "optional_subjects": ["Computer Science", "Electronics", "Statistics"],
                "career_focus": "Engineering, Technology, Physical Sciences, Mathematics",
            },
            "Science (PCB)": {
                "core_subjects": ["Physics", "Chemistry", "Biology"],
                "optional_subjects": ["Mathematics", "Psychology", "Biotechnology"],
                "career_focus": "Medicine, Life Sciences, Healthcare, Research",
            },
            "Science (PCMB)": {
                "core_subjects": ["Physics", "Chemistry", "Mathematics", "Biology"],
                "optional_subjects": ["Computer Science", "Psychology"],
                "career_focus": "Medical Engineering, Biotechnology, Research, Flexible career options",
            },
            "Commerce (Math)": {
                "core_subjects": [
                    "Accountancy",
                    "Business Studies",
                    "Economics",
                    "Mathematics",
                ],
                "optional_subjects": [
                    "Computer Science",
                    "Statistics",
                    "Entrepreneurship",
                ],
                "career_focus": "Business, Finance, Economics, Data Analysis",
            },
            "Commerce (No Math)": {
                "core_subjects": ["Accountancy", "Business Studies", "Economics"],
                "optional_subjects": ["Psychology", "Legal Studies", "Marketing"],
                "career_focus": "Business Management, Marketing, Law, Social Sciences",
            },
            "Arts/Humanities": {
                "core_subjects": [
                    "History",
                    "Geography",
                    "Political Science",
                    "Economics",
                ],
                "optional_subjects": [
                    "Psychology",
                    "Sociology",
                    "Literature",
                    "Philosophy",
                ],
                "career_focus": "Civil Services, Law, Journalism, Social Work, Education",
            },
        }

        # Aptitude-stream compatibility matrix
        self.aptitude_stream_mapping = {
            "computational": {
                "Science (PCM)": 0.9,
                "Science (PCMB)": 0.8,
                "Commerce (Math)": 0.8,
            },
            "experimental": {
                "Science (PCB)": 0.9,
                "Science (PCMB)": 0.9,
                "Science (PCM)": 0.7,
            },
            "technical": {
                "Science (PCM)": 0.9,
                "Science (PCMB)": 0.7,
                "Vocational": 0.8,
            },
            "medical": {"Science (PCB)": 0.95, "Science (PCMB)": 0.9},
            "administrative": {
                "Commerce (Math)": 0.8,
                "Commerce (No Math)": 0.8,
                "Arts/Humanities": 0.6,
            },
            "humanitarian": {
                "Arts/Humanities": 0.9,
                "Commerce (No Math)": 0.6,
                "Science (PCB)": 0.5,
            },
            "educational": {
                "Arts/Humanities": 0.8,
                "Science (PCB)": 0.6,
                "Commerce (No Math)": 0.5,
            },
            "creative": {
                "Arts/Humanities": 0.8,
                "Commerce (No Math)": 0.5,
                "Vocational": 0.7,
            },
            "nature": {
                "Science (PCB)": 0.8,
                "Science (PCMB)": 0.7,
                "Arts/Humanities": 0.6,
            },
        }

    def _define_required_inputs(self) -> List[str]:
        """Required inputs for stream advisory"""
        return ["dbda_scores", "cii_results"]

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that enhance stream recommendations"""
        return [
            "current_grade",
            "academic_performance",
            "subject_preferences",
            "family_preferences",
            "career_aspirations",
            "geographical_constraints",
            "financial_considerations",
            "previous_agent_outputs",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of stream advisory output"""
        return {
            "executive_summary": "str",
            "recommended_streams": "list",
            "stream_comparison_matrix": "dict",
            "subject_wise_guidance": "dict",
            "parental_discussion_points": "list",
            "decision_timeline": "dict",
            "backup_options": "list",
            "next_steps": "list",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.output_parser = JsonOutputParser(pydantic_object=StreamAdvisorOutput)

        # Create the main stream advisory prompt
        self.advisory_prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "test_interpretation",
                "aptitude_strengths",
                "interest_patterns",
                "stream_options",
                "contextual_factors",
            ],
            template=self._create_advisory_template(),
        )

    def _create_advisory_template(self) -> str:
        """Create the comprehensive stream advisory prompt template"""
        return """You are an expert Academic Counselor and Stream Specialist with extensive experience in the Indian education system. You help Grade 9-12 students select optimal academic streams based on their aptitudes, interests, and circumstances.

STUDENT PROFILE:
{student_profile}

PSYCHOLOGICAL ASSESSMENT INTERPRETATION:
{test_interpretation}

IDENTIFIED APTITUDE STRENGTHS:
{aptitude_strengths}

INTEREST PATTERNS:
{interest_patterns}

AVAILABLE STREAM OPTIONS:
{stream_options}

CONTEXTUAL FACTORS:
{contextual_factors}

STREAM RECOMMENDATION GUIDELINES:
1. Prioritize aptitude-interest alignment for long-term satisfaction and success
2. Consider practical factors (family preferences, financial constraints, geographic limitations)
3. Evaluate career pathway diversity and future opportunities
4. Assess academic workload and student's capacity to handle different streams
5. Provide both primary and backup recommendations
6. Address common myths and misconceptions about streams
7. Consider emerging career fields and changing job market trends
8. Balance passion with practicality in recommendations

INDIAN ACADEMIC STREAM CONTEXT:
- Science streams lead to engineering, medicine, research careers
- Commerce streams open business, finance, economics pathways  
- Arts/Humanities enable civil services, law, social work, education
- Stream choice significantly impacts college admission and career options
- Many students face family pressure for Science stream regardless of aptitude
- Inter-stream mobility is possible but requires additional effort

IMPORTANT CONSIDERATIONS:
- Emphasize that all streams have high-potential career pathways
- Consider the student's stress tolerance and academic pressure handling
- Factor in the competitive landscape of different streams
- Discuss the importance of subject interest over social prestige

Please provide a comprehensive stream recommendation following this JSON structure:

{format_instructions}

Focus on:
1. Clear rationale for each stream recommendation based on test results
2. Honest assessment of challenges and requirements for each stream
3. Practical next steps for stream selection and preparation
4. Points to help students and parents make informed decisions
5. Alternative pathways if primary choices face obstacles
6. Timeline for decision-making aligned with academic calendar

Remember: This recommendation will significantly impact the student's academic journey. Provide balanced, evidence-based advice that considers both potential and practical constraints."""

    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic for academic stream advisory"""

        # Extract required data
        dbda_scores = validated_input["required_data"]["dbda_scores"]
        cii_results = validated_input["required_data"]["cii_results"]

        # Extract optional context
        optional_data = validated_input["optional_data"]
        previous_outputs = validated_input.get("previous_outputs", {})

        # Get test score interpretation from previous agent if available
        test_interpreter_result = previous_outputs.get("test_score_interpreter")

        # Prepare student profile
        student_profile = self._prepare_student_profile(optional_data)

        # Extract and format test interpretation
        test_interpretation = self._extract_test_interpretation(test_interpreter_result)

        # Identify aptitude strengths from scores
        aptitude_strengths = self._identify_aptitude_strengths(dbda_scores)

        # Extract interest patterns
        interest_patterns = self._extract_interest_patterns(cii_results)

        # Prepare stream options with details
        stream_options = self._format_stream_options()

        # Prepare contextual factors
        contextual_factors = self._prepare_contextual_factors(optional_data)

        # Add processing note
        self._add_processing_note(
            "Starting academic stream analysis and recommendation"
        )

        try:
            # Generate stream recommendations using LLM
            prompt_input = {
                "student_profile": student_profile,
                "test_interpretation": test_interpretation,
                "aptitude_strengths": aptitude_strengths,
                "interest_patterns": interest_patterns,
                "stream_options": stream_options,
                "contextual_factors": contextual_factors,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            formatted_prompt = self.advisory_prompt.format(**prompt_input)

            # Get LLM response
            llm_response = self.llm_model.invoke(formatted_prompt)

            # Convert to dictionary and add metadata
            result = self._parse_llm_response(llm_response)

            # Add advisory metadata
            result["advisory_metadata"] = {
                "advisor_role": "Academic Counselor and Stream Specialist",
                "education_system": "Indian Academic System (Grades 9-12)",
                "recommendation_date": datetime.now().isoformat(),
                "based_on_assessments": [
                    "DBDA Aptitude Test",
                    "Career Interest Inventory (CII)",
                ],
                "methodology": "Aptitude-Interest-Context Integration Analysis",
                "streams_considered": list(self.stream_subjects.keys()),
            }

            # Add computational analysis
            result["computational_analysis"] = {
                "aptitude_stream_compatibility": self._calculate_stream_compatibility(
                    dbda_scores
                ),
                "interest_stream_alignment": self._calculate_interest_alignment(
                    cii_results
                ),
                "combined_suitability_scores": self._calculate_combined_suitability(
                    dbda_scores, cii_results
                ),
                "top_3_recommended_streams": self._get_top_stream_recommendations(
                    dbda_scores, cii_results
                ),
            }

            family_context = {
                "family_preferences": optional_data.get("family_preferences"),
                "financial_considerations": optional_data.get(
                    "financial_considerations"
                ),
                "family_background": optional_data.get("family_background"),
            }

            decision_support_result = self.decision_support_agent.generate_support(
                student_profile=student_profile,
                recommended_streams=result["recommended_streams"],
                assessment_scores={"dbda": dbda_scores, "cii": cii_results},
                family_context=family_context,
                academic_performance=optional_data.get(
                    "academic_performance", "Not specified"
                ),
            )

            # Replace the hardcoded practical_guidance
            result["practical_guidance"] = decision_support_result
            self._add_processing_note("Dynamic decision support generated successfully")

            student_preferences = {
                "career_aspirations": optional_data.get("career_aspirations"),
                "subject_preferences": optional_data.get("subject_preferences"),
                "assessment_based_strengths": self._get_top_aptitudes_and_interests(
                    dbda_scores, cii_results
                ),
            }

            family_expectations = {
                "family_preferences": optional_data.get("family_preferences"),
                "family_background": optional_data.get("family_background"),
                "cultural_context": optional_data.get(
                    "geographical_constraints"
                ),  # Can indicate cultural region
            }

            alignment_result = self.parental_alignment_agent.assess_alignment(
                student_preferences=student_preferences,
                family_expectations=family_expectations,
                assessment_results={"dbda": dbda_scores, "cii": cii_results},
                recommended_streams=result["recommended_streams"],
            )

            # Enhance parental_discussion_points with dynamic analysis
            result["parental_alignment_analysis"] = alignment_result
            # Replace the original parental_discussion_points with more targeted content
            result["parental_discussion_points"] = alignment_result.get(
                "discussion_strategies", []
            )

            self._add_processing_note("Dynamic parental alignment analysis completed")

            self._add_processing_note("Stream advisory analysis completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Error in stream advisory: {str(e)}")
            self._add_processing_note(f"Stream advisory error: {str(e)}")
            raise

    def _get_top_aptitudes_and_interests(
        self, dbda_scores: Dict[str, Any], cii_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract top aptitudes and interests for analysis"""
        valid_scores = {k: v for k, v in dbda_scores.items() if v is not None}
        top_aptitudes = sorted(valid_scores.items(), key=lambda x: x[1], reverse=True)[
            :3
        ]
        top_interests = (
            sorted(cii_results.items(), key=lambda x: x[1], reverse=True)[:3]
            if cii_results
            else []
        )

        return {
            "top_aptitudes": [
                {"domain": apt, "score": score} for apt, score in top_aptitudes
            ],
            "top_interests": [
                {"domain": interest, "score": score}
                for interest, score in top_interests
            ],
        }

    def _prepare_student_profile(self, optional_data: Dict[str, Any]) -> str:
        """Prepare comprehensive student profile"""
        profile_parts = []

        # Basic information
        grade = optional_data.get("current_grade", "Not specified")
        profile_parts.append(f"Current Grade: {grade}")

        # Academic performance
        if optional_data.get("academic_performance"):
            profile_parts.append(
                f"Academic Performance: {optional_data['academic_performance']}"
            )

        # Subject preferences
        if optional_data.get("subject_preferences"):
            subjects = optional_data["subject_preferences"]
            if isinstance(subjects, list):
                profile_parts.append(f"Preferred Subjects: {', '.join(subjects)}")
            else:
                profile_parts.append(f"Subject Preferences: {subjects}")

        # Career aspirations
        if optional_data.get("career_aspirations"):
            profile_parts.append(
                f"Career Aspirations: {optional_data['career_aspirations']}"
            )

        return (
            "\n".join(profile_parts)
            if profile_parts
            else "Basic student profile available"
        )

    def _extract_test_interpretation(self, interpreter_result) -> str:
        """Extract key insights from test score interpreter agent"""
        if (
            not interpreter_result
            or interpreter_result.status != ProcessingStatus.COMPLETED
        ):
            return "Test interpretation not available from previous agent"

        output_data = interpreter_result.output_data
        interpretation_parts = []

        # Executive summary
        if output_data.get("executive_summary"):
            interpretation_parts.append(
                f"Assessment Overview: {output_data['executive_summary']}"
            )

        # Key aptitude insights
        if output_data.get("aptitude_analysis"):
            aptitude_info = output_data["aptitude_analysis"]
            if isinstance(aptitude_info, dict):
                interpretation_parts.append("Key Aptitude Insights:")
                for key, value in aptitude_info.items():
                    if isinstance(value, str):
                        interpretation_parts.append(f"- {key}: {value}")

        # Interest analysis
        if output_data.get("interest_analysis"):
            interest_info = output_data["interest_analysis"]
            if isinstance(interest_info, dict):
                interpretation_parts.append("Interest Analysis:")
                for key, value in interest_info.items():
                    if isinstance(value, str):
                        interpretation_parts.append(f"- {key}: {value}")

        # Aptitude-interest alignment
        if output_data.get("aptitude_interest_alignment"):
            alignment_info = output_data["aptitude_interest_alignment"]
            interpretation_parts.append(
                f"Aptitude-Interest Alignment: {alignment_info}"
            )

        return (
            "\n".join(interpretation_parts)
            if interpretation_parts
            else "Limited test interpretation available"
        )

    def _identify_aptitude_strengths(self, dbda_scores: Dict[str, Any]) -> str:
        """Identify and format aptitude strengths"""
        if not dbda_scores:
            return "No DBDA aptitude scores available"

        # Sort scores and identify strengths (score >= 7 considered strength)
        strengths = [
            (domain, score)
            for domain, score in dbda_scores.items()
            if score is not None and score >= 7
        ]
        strengths.sort(key=lambda x: x[1], reverse=True)

        if not strengths:
            # If no clear strengths, identify relative strengths
            sorted_scores = sorted(
                dbda_scores.items(), key=lambda x: x[1], reverse=True
            )
            top_3 = sorted_scores[:3]
            strength_lines = [
                f"Relative Strength - {domain.replace('_', ' ').title()}: {score}/10"
                for domain, score in top_3
            ]
        else:
            strength_lines = [
                f"{domain.replace('_', ' ').title()}: {score}/10 (Strong)"
                for domain, score in strengths
            ]

        return "Identified Aptitude Strengths:\n" + "\n".join(
            f"- {line}" for line in strength_lines
        )

    def _extract_interest_patterns(self, cii_results: Dict[str, Any]) -> str:
        """Extract and format interest patterns"""
        if not cii_results:
            return "No CII interest data available"

        # Sort interests and identify high interests (score >= 6 considered interest)
        interests = [
            (domain, score) for domain, score in cii_results.items() if score >= 6
        ]
        interests.sort(key=lambda x: x[1], reverse=True)

        if not interests:
            # If no clear interests, identify relative interests
            sorted_interests = sorted(
                cii_results.items(), key=lambda x: x[1], reverse=True
            )
            top_3 = sorted_interests[:3]
            interest_lines = [
                f"Moderate Interest - {domain.replace('_', ' ').title()}: {score}/10"
                for domain, score in top_3
            ]
        else:
            interest_lines = [
                f"{domain.replace('_', ' ').title()}: {score}/10 (High Interest)"
                for domain, score in interests
            ]

        return "Identified Interest Patterns:\n" + "\n".join(
            f"- {line}" for line in interest_lines
        )

    def _format_stream_options(self) -> str:
        """Format available stream options with details"""
        stream_lines = ["Available Academic Streams in Indian Education System:"]

        for stream, details in self.stream_subjects.items():
            stream_lines.append(f"\n{stream}:")
            stream_lines.append(
                f"  Core Subjects: {', '.join(details['core_subjects'])}"
            )
            stream_lines.append(
                f"  Optional Subjects: {', '.join(details['optional_subjects'])}"
            )
            stream_lines.append(f"  Career Focus: {details['career_focus']}")

        return "\n".join(stream_lines)

    def _prepare_contextual_factors(self, optional_data: Dict[str, Any]) -> str:
        """Prepare contextual factors that influence stream selection"""
        factors = []

        # Family preferences
        if optional_data.get("family_preferences"):
            factors.append(f"Family Preferences: {optional_data['family_preferences']}")

        # Financial considerations
        if optional_data.get("financial_considerations"):
            factors.append(
                f"Financial Considerations: {optional_data['financial_considerations']}"
            )

        # Geographic constraints
        if optional_data.get("geographical_constraints"):
            factors.append(
                f"Geographic Constraints: {optional_data['geographical_constraints']}"
            )

        # Academic performance context
        if optional_data.get("academic_performance"):
            factors.append(
                f"Current Academic Performance: {optional_data['academic_performance']}"
            )

        return (
            "\n".join(factors)
            if factors
            else "No specific contextual constraints mentioned"
        )

    def _calculate_stream_compatibility(
        self, dbda_scores: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate compatibility scores for each stream based on aptitudes"""
        stream_scores = {}

        for stream in self.stream_subjects.keys():
            score = 0.0
            count = 0

            for aptitude, aptitude_score in dbda_scores.items():
                if aptitude in self.aptitude_stream_mapping:
                    stream_mapping = self.aptitude_stream_mapping[aptitude]
                    if stream in stream_mapping:
                        # Normalize aptitude score (0-1) and multiply by stream compatibility
                        normalized_aptitude = aptitude_score / 10.0
                        score += normalized_aptitude * stream_mapping[stream]
                        count += 1

            stream_scores[stream] = round(score / max(count, 1), 3)

        return stream_scores

    def _calculate_interest_alignment(
        self, cii_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate how well interests align with each stream"""
        # This is a simplified mapping - you might want to expand this
        stream_interest_scores = {}

        interest_stream_mapping = {
            "technical": ["Science (PCM)", "Science (PCMB)"],
            "medical": ["Science (PCB)", "Science (PCMB)"],
            "experimental": ["Science (PCB)", "Science (PCM)", "Science (PCMB)"],
            "computational": ["Science (PCM)", "Commerce (Math)"],
            "administrative": ["Commerce (Math)", "Commerce (No Math)"],
            "humanitarian": ["Arts/Humanities", "Commerce (No Math)"],
            "creative": ["Arts/Humanities"],
            "educational": ["Arts/Humanities"],
        }

        for stream in self.stream_subjects.keys():
            score = 0.0
            count = 0

            for interest, interest_score in cii_results.items():
                if interest in interest_stream_mapping:
                    if stream in interest_stream_mapping[interest]:
                        score += interest_score / 10.0
                        count += 1

            stream_interest_scores[stream] = round(score / max(count, 1), 3)

        return stream_interest_scores

    def _calculate_combined_suitability(
        self, dbda_scores: Dict[str, Any], cii_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate combined aptitude-interest suitability scores"""
        aptitude_scores = self._calculate_stream_compatibility(dbda_scores)
        interest_scores = self._calculate_interest_alignment(cii_results)

        combined_scores = {}
        for stream in self.stream_subjects.keys():
            # Weight aptitude slightly higher than interest (60:40 ratio)
            combined = (aptitude_scores.get(stream, 0) * 0.6) + (
                interest_scores.get(stream, 0) * 0.4
            )
            combined_scores[stream] = round(combined, 3)

        return combined_scores

    def _get_top_stream_recommendations(
        self, dbda_scores: Dict[str, Any], cii_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get top 3 stream recommendations with scores"""
        combined_scores = self._calculate_combined_suitability(dbda_scores, cii_results)

        # Sort by combined score
        sorted_streams = sorted(
            combined_scores.items(), key=lambda x: x[1], reverse=True
        )

        top_3 = []
        for i, (stream, score) in enumerate(sorted_streams[:3]):
            top_3.append(
                {
                    "rank": i + 1,
                    "stream": stream,
                    "suitability_score": score,
                    "score_interpretation": self._interpret_suitability_score(score),
                }
            )

        return top_3

    def _interpret_suitability_score(self, score: float) -> str:
        """Interpret suitability score levels"""
        if score >= 0.8:
            return "Highly Suitable"
        elif score >= 0.6:
            return "Well Suited"
        elif score >= 0.4:
            return "Moderately Suitable"
        elif score >= 0.2:
            return "Limited Suitability"
        else:
            return "Not Recommended"

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
