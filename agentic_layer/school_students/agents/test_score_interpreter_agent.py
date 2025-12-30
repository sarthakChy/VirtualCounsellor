from typing import Dict, List, Any, Optional
from enum import Enum
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from agentic_layer.base_agent import BaseAgent
from config.agent_config import AgentType


class ScoreLevel(Enum):
    """Standard interpretation levels for assessment scores"""

    VERY_LOW = "Very Low"
    LOW = "Low"
    BELOW_AVERAGE = "Below Average"
    AVERAGE = "Average"
    ABOVE_AVERAGE = "Above Average"
    HIGH = "High"
    VERY_HIGH = "Very High"


class TestScoreInterpretationOutput(BaseModel):
    """Structured output for test score interpretation"""

    executive_summary: str = Field(
        description="Brief overview of student's overall profile"
    )
    aptitude_analysis: Dict[str, Any] = Field(
        description="DBDA aptitude test interpretation"
    )
    interest_analysis: Dict[str, Any] = Field(
        description="CII interest inventory interpretation"
    )
    aptitude_interest_alignment: Dict[str, Any] = Field(
        description="How aptitudes align with interests"
    )
    psychological_insights: Dict[str, Any] = Field(
        description="Age-appropriate psychological insights"
    )
    developmental_considerations: List[str] = Field(
        description="Adolescent development factors"
    )
    confidence_indicators: Dict[str, Any] = Field(
        description="Reliability of assessment results"
    )
    key_recommendations: List[str] = Field(
        description="Primary recommendations for next steps"
    )


class TestScoreInterpreterAgent(BaseAgent):
    """
    Expert Educational Psychologist Agent for interpreting DBDA and CII assessments
    for school students (grades 9-12). Specializes in adolescent psychological assessment
    and career development with age-appropriate guidance.
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="test_score_interpreter",
            agent_name="Test Score Interpreter Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config or {},
        )

        # Agent expertise areas
        self.expertise_areas = [
            "Adolescent psychological assessment (ages 14-18)",
            "DBDA aptitude test interpretation",
            "Career Interest Inventory (CII) analysis",
            "Aptitude-interest correlation analysis",
            "Age-appropriate career guidance",
            "Test reliability assessment for teenagers",
        ]

        # CII interest areas for interpretation (corrected based on actual CII domains)
        self.cii_domains = {
            "administrative": "Office management, coordination, organizational tasks and clerical work",
            "entertainment": "Performance, media, creative presentation and entertainment industry",
            "defense": "Security, protection, law enforcement and military activities",
            "sports": "Physical activities, athletics, fitness and sports-related careers",
            "creative": "Artistic creation, design, innovative thinking and creative expression",
            "performing": "Stage performance, public speaking, dramatic expression and presentation",
            "medical": "Healthcare, healing, biological sciences and medical professions",
            "technical": "Engineering, technology, mechanical problem-solving and technical skills",
            "experimental": "Research, testing, scientific methodology and laboratory work",
            "computational": "Mathematics, data analysis, logical reasoning and computer science",
            "humanitarian": "Social service, helping others, community work and welfare",
            "educational": "Teaching, training, knowledge transmission and academic work",
            "nature": "Environmental work, biology, outdoor activities and natural sciences",
            "clerical": "Data entry, record-keeping, administrative support and office tasks",
        }

        # DBDA aptitude areas for interpretation (keeping existing mapping)
        self.dbda_domains = {
            "administrative": "Office management, coordination, organizational tasks",
            "entertainment": "Performance, media, creative presentation",
            "defense": "Security, protection, law enforcement activities",
            "sports": "Physical activities, athletics, fitness-related careers",
            "creative": "Artistic creation, design, innovative thinking",
            "performing": "Stage performance, public speaking, dramatic expression",
            "medical": "Healthcare, healing, biological sciences",
            "technical": "Engineering, technology, mechanical problem-solving",
            "experimental": "Research, testing, scientific methodology",
            "computational": "Mathematics, data analysis, logical reasoning",
            "humanitarian": "Social service, helping others, community work",
            "educational": "Teaching, training, knowledge transmission",
            "nature": "Environmental work, biology, outdoor activities",
            "clerical": "Data entry, record-keeping, administrative support",
        }

    def _define_required_inputs(self) -> List[str]:
        """Required inputs for test score interpretation"""
        return ["dbda_scores", "cii_results"]

    def _define_optional_inputs(self) -> List[str]:
        """Optional inputs that enhance interpretation"""
        return [
            "student_name",
            "age",
            "current_grade",
            "academic_performance",
            "extracurricular_activities",
            "family_background",
            "test_taking_conditions",
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of interpretation output"""
        return {
            "executive_summary": "str",
            "aptitude_analysis": "dict",
            "interest_analysis": "dict",
            "aptitude_interest_alignment": "dict",
            "psychological_insights": "dict",
            "developmental_considerations": "list",
            "confidence_indicators": "dict",
            "key_recommendations": "list",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.output_parser = JsonOutputParser(
            pydantic_object=TestScoreInterpretationOutput
        )

        # Create the main interpretation prompt
        self.interpretation_prompt = PromptTemplate(
            input_variables=[
                "student_info",
                "dbda_scores",
                "cii_scores",
                "cii_domains",
                "dbda_domains",
                "optional_context",
            ],
            template=self._create_interpretation_template(),
        )

    def _create_interpretation_template(self) -> str:
        """Create the comprehensive interpretation prompt template"""
        return """You are an expert Educational Psychologist specializing in adolescent career assessment. You are interpreting standardized test results for a school student to provide age-appropriate, encouraging, and actionable career guidance.

STUDENT INFORMATION:
{student_info}

ASSESSMENT RESULTS:

DBDA APTITUDE TEST SCORES (Sten Scale 1-10):
{dbda_scores}

CAREER INTEREST INVENTORY (CII) SCORES (Sten Scale 1-10):
{cii_scores}  

ASSESSMENT DOMAIN INTERPRETATIONS:

CII Interest Areas:
{cii_domains}

DBDA Aptitude Areas:
{dbda_domains}

ADDITIONAL CONTEXT:
{optional_context}

INTERPRETATION GUIDELINES:
- Both DBDA and CII use Sten scores (1-10 scale) - treat them consistently
- Use age-appropriate language for 14-18 year olds
- Be encouraging while being realistic about strengths and areas for development
- Consider adolescent developmental factors (identity formation, future anxiety, peer influence)
- Focus on growth potential rather than fixed abilities
- Provide specific, actionable recommendations
- Address test reliability concerns common in teenage assessments
- Use positive framing while acknowledging areas for improvement

STEN SCORE INTERPRETATION GUIDE:
- Sten Scores 1-3: Below Average (need support/development)
- Sten Scores 4-6: Average (typical development)  
- Sten Scores 7-8: Above Average (strength areas)
- Sten Scores 9-10: High/Very High (exceptional strength)

Please provide a comprehensive interpretation following this JSON structure:

{format_instructions}

Focus on:
1. Identifying clear strengths and natural talents from DBDA
2. Recognizing interest patterns and motivational drivers from CII
3. Assessing how aptitudes align with interests for career fit
4. Providing developmental insights appropriate for teenagers
5. Offering specific next steps and recommendations
6. Addressing any concerning patterns or inconsistencies with care

Remember: This student is at a crucial stage of identity and career development. Your interpretation should inspire confidence while providing realistic guidance for their educational and career journey."""

    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core processing logic for test score interpretation"""

        # Extract required data
        dbda_scores = validated_input["required_data"]["dbda_scores"]
        cii_results = validated_input["required_data"]["cii_results"]

        # Extract optional context
        optional_data = validated_input["optional_data"]

        # Prepare student information summary
        student_info = self._prepare_student_info(optional_data)

        # Format scores for interpretation (both are now sten scores)
        dbda_formatted = self._format_sten_scores(dbda_scores, "DBDA Aptitude Areas")
        cii_formatted = self._format_sten_scores(
            cii_results, "Career Interest Inventory (CII)"
        )

        # Prepare domain descriptions
        cii_domains_text = self._format_domains(self.cii_domains)
        dbda_domains_text = self._format_domains(self.dbda_domains)

        # Prepare optional context
        optional_context = self._prepare_optional_context(optional_data)

        # Add processing note
        self._add_processing_note("Starting comprehensive test score interpretation")

        try:
            # Generate interpretation using LLM
            prompt_input = {
                "student_info": student_info,
                "dbda_scores": dbda_formatted,
                "cii_scores": cii_formatted,
                "cii_domains": cii_domains_text,
                "dbda_domains": dbda_domains_text,
                "optional_context": optional_context,
                "format_instructions": self.output_parser.get_format_instructions(),
            }

            formatted_prompt = self.interpretation_prompt.format(**prompt_input)

            # Get LLM response
            llm_response = self.llm_model.invoke(formatted_prompt)

            # Convert to dictionary and add metadata
            result = self._parse_llm_response(llm_response)

            # Add interpretation metadata
            result["interpretation_metadata"] = {
                "interpreter_role": "Educational Psychologist and Aptitude Specialist",
                "assessment_types": [
                    "DBDA Aptitude Test",
                    "Career Interest Inventory (CII)",
                ],
                "interpretation_date": validated_input.get("session_metadata", {}).get(
                    "timestamp", "unknown"
                ),
                "age_group_focus": "School Students (14-18 years)",
                "interpretation_approach": "Holistic developmental assessment",
                "scoring_system": "Both DBDA and CII use Sten scores (1-10)",
                "reliability_factors": self._assess_test_reliability(
                    dbda_scores, cii_results, optional_data
                ),
            }

            # Add score summaries for quick reference
            result["score_summaries"] = {
                "dbda_top_aptitudes": self._identify_top_scores(
                    dbda_scores, self.dbda_domains
                ),
                "cii_top_interests": self._identify_top_scores(
                    cii_results, self.cii_domains
                ),
                "aptitude_interest_patterns": self._identify_aptitude_interest_patterns(
                    dbda_scores, cii_results
                ),
            }

            self._add_processing_note("Test interpretation completed successfully")
            return result

        except Exception as e:
            self.logger.error(f"Error in test interpretation: {str(e)}")
            self._add_processing_note(f"Interpretation error: {str(e)}")
            raise

    def _prepare_student_info(self, optional_data: Dict[str, Any]) -> str:
        """Prepare student information summary"""
        info_parts = []

        name = optional_data.get("student_name", "Student")
        age = optional_data.get("age")
        grade = optional_data.get("current_grade")

        info_parts.append(f"Name: {name}")

        if age:
            info_parts.append(f"Age: {age} years")

        if grade:
            info_parts.append(f"Current Grade: {grade}")

        if optional_data.get("academic_performance"):
            info_parts.append(
                f"Academic Performance: {optional_data['academic_performance']}"
            )

        if optional_data.get("extracurricular_activities"):
            activities = optional_data["extracurricular_activities"]
            if isinstance(activities, list):
                info_parts.append(f"Activities: {', '.join(activities)}")
            else:
                info_parts.append(f"Activities: {activities}")

        return (
            "\n".join(info_parts) if info_parts else "Basic student profile available"
        )

    def _format_domains(self, domains: Dict[str, str]) -> str:
        """Format domain descriptions"""
        formatted_lines = []
        for domain, description in domains.items():
            formatted_lines.append(
                f"- {domain.replace('_', ' ').title()}: {description}"
            )
        return "\n".join(formatted_lines)

    def _prepare_optional_context(self, optional_data: Dict[str, Any]) -> str:
        """Prepare optional context information"""
        context_parts = []

        if optional_data.get("family_background"):
            context_parts.append(
                f"Family Background: {optional_data['family_background']}"
            )

        if optional_data.get("test_taking_conditions"):
            context_parts.append(
                f"Test Conditions: {optional_data['test_taking_conditions']}"
            )

        return (
            "\n".join(context_parts)
            if context_parts
            else "No additional context provided"
        )

    def _format_sten_scores(self, scores: Dict[str, Any], assessment_name: str) -> str:
        """Format sten scores for interpretation (unified for both DBDA and CII)"""
        if not scores:
            return f"No {assessment_name} scores available"

        formatted_lines = [f"{assessment_name} (Sten Scores 1-10):"]

        for domain, score in scores.items():
            if score is None:
                formatted_lines.append(
                    f"- {domain.replace('_', ' ').title()}: Not Available"
                )
            else:
                level = self._categorize_sten_score(score)
                formatted_lines.append(
                    f"- {domain.replace('_', ' ').title()}: {score}/10 ({level})"
                )

        return "\n".join(formatted_lines)

    def _categorize_sten_score(self, score: int) -> str:
        """Categorize sten scores into interpretive levels (unified for both assessments)"""
        if score is None:
            return "Not Available"

        if score <= 3:
            return "Below Average"
        elif score <= 4:
            return "Low Average"
        elif score <= 6:
            return "Average"
        elif score <= 7:
            return "Above Average"
        elif score <= 8:
            return "High"
        elif score <= 10:
            return "Very High"
        else:
            return "Very High"

    def _identify_top_scores(
        self, scores: Dict[str, Any], domain_descriptions: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Identify top scoring areas"""
        if not scores:
            return []

        # Filter out None values before sorting
        valid_scores = {k: v for k, v in scores.items() if v is not None}

        if not valid_scores:
            return []

        # Sort by score and get top 3
        sorted_scores = sorted(valid_scores.items(), key=lambda x: x[1], reverse=True)[
            :3
        ]

        top_areas = []
        for domain, score in sorted_scores:
            top_areas.append(
                {
                    "domain": domain.replace("_", " ").title(),
                    "score": score,
                    "description": domain_descriptions.get(
                        domain, "Description not available"
                    ),
                    "level": self._categorize_sten_score(score),
                }
            )

        return top_areas

    def _assess_test_reliability(
        self,
        dbda_scores: Dict[str, Any],
        cii_scores: Dict[str, Any],
        optional_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Assess reliability factors for the assessments"""
        reliability_factors = {
            "overall_reliability": "Good",
            "factors_affecting_reliability": [],
            "interpretation_confidence": "High",
        }

        # Filter out None values for reliability assessment
        valid_dbda_scores = [
            score for score in dbda_scores.values() if score is not None
        ]
        valid_cii_scores = [score for score in cii_scores.values() if score is not None]

        # Check for missing data
        missing_dbda = sum(1 for score in dbda_scores.values() if score is None)
        missing_cii = sum(1 for score in cii_scores.values() if score is None)

        if missing_dbda > 0:
            reliability_factors["factors_affecting_reliability"].append(
                f"Missing {missing_dbda} DBDA score(s)"
            )

        if missing_cii > 0:
            reliability_factors["factors_affecting_reliability"].append(
                f"Missing {missing_cii} CII score(s)"
            )

        # Check for extreme response patterns in valid scores only
        if valid_dbda_scores and any(
            score <= 1 or score >= 10 for score in valid_dbda_scores
        ):
            reliability_factors["factors_affecting_reliability"].append(
                "Extreme response pattern detected in DBDA"
            )

        if valid_cii_scores and any(
            score <= 1 or score >= 10 for score in valid_cii_scores
        ):
            reliability_factors["factors_affecting_reliability"].append(
                "Extreme response pattern detected in CII"
            )

        # Check age-related factors
        age = optional_data.get("age", 16)
        if age < 15:
            reliability_factors["factors_affecting_reliability"].append(
                "Younger age may affect test stability"
            )
            reliability_factors["interpretation_confidence"] = "Moderate"

        # Check for very flat profiles (little differentiation) - only with valid scores
        if valid_dbda_scores and len(valid_dbda_scores) > 1:
            dbda_range = max(valid_dbda_scores) - min(valid_dbda_scores)
            if dbda_range <= 2:
                reliability_factors["factors_affecting_reliability"].append(
                    "Low differentiation in DBDA scores"
                )

        if valid_cii_scores and len(valid_cii_scores) > 1:
            cii_range = max(valid_cii_scores) - min(valid_cii_scores)
            if cii_range <= 2:
                reliability_factors["factors_affecting_reliability"].append(
                    "Low differentiation in CII scores"
                )

        # Adjust overall reliability based on factors
        if len(reliability_factors["factors_affecting_reliability"]) >= 2:
            reliability_factors["overall_reliability"] = "Moderate"
            reliability_factors["interpretation_confidence"] = "Moderate"

        return reliability_factors

    def _identify_aptitude_interest_patterns(
        self, dbda_scores: Dict[str, Any], cii_scores: Dict[str, Any]
    ) -> List[str]:
        """Identify patterns between aptitudes and interests (updated for actual DBDA field names)"""
        patterns = []

        # Helper function to safely get score with None check
        def safe_get_score(scores_dict, key, default=0):
            score = scores_dict.get(key, default)
            return score if score is not None else default

        # Check for creative/artistic patterns (VA = Visual Arts, CA = Creative Arts)
        if (
            safe_get_score(dbda_scores, "VA") >= 7
            or safe_get_score(dbda_scores, "CA") >= 7
        ) and (
            safe_get_score(cii_scores, "creative") >= 6
            or safe_get_score(cii_scores, "performing") >= 6
        ):
            patterns.append("Strong creative/artistic aptitude and interest alignment")

        # Check for analytical/computational patterns (RA = Reasoning/Analytical, MA = Mathematical)
        if (
            safe_get_score(dbda_scores, "RA") >= 7
            or safe_get_score(dbda_scores, "MA") >= 7
        ) and (
            safe_get_score(cii_scores, "computational") >= 6
            or safe_get_score(cii_scores, "experimental") >= 6
        ):
            patterns.append(
                "Strong analytical and computational aptitude-interest convergence"
            )

        # Check for social/helping patterns (SA = Social Aptitude)
        if (safe_get_score(dbda_scores, "SA") >= 7) and (
            safe_get_score(cii_scores, "humanitarian") >= 6
            or safe_get_score(cii_scores, "educational") >= 6
        ):
            patterns.append(
                "Excellent social aptitude matching helping/educational interests"
            )

        # Check for clerical/administrative patterns (CL = Clerical)
        if (safe_get_score(dbda_scores, "CL") >= 7) and (
            safe_get_score(cii_scores, "administrative") >= 6
            or safe_get_score(cii_scores, "clerical") >= 6
        ):
            patterns.append(
                "Strong clerical aptitude with administrative interest alignment"
            )

        # Check for nature/outdoor patterns (NA = Nature Aptitude)
        if (safe_get_score(dbda_scores, "NA") >= 7) and (
            safe_get_score(cii_scores, "nature") >= 6
            or safe_get_score(cii_scores, "sports") >= 6
        ):
            patterns.append(
                "Nature aptitude aligns with outdoor and environmental interests"
            )

        # Check for technical/practical patterns (PM = Practical/Mechanical - if available)
        if (safe_get_score(dbda_scores, "PM") >= 7) and (
            safe_get_score(cii_scores, "technical") >= 6
            or safe_get_score(cii_scores, "sports") >= 6
        ):
            patterns.append("Practical/mechanical aptitude matches technical interests")

        # Check for medical/healthcare patterns (MA could relate to medical sciences)
        if (
            safe_get_score(dbda_scores, "MA") >= 7
            or safe_get_score(dbda_scores, "RA") >= 7
        ) and (safe_get_score(cii_scores, "medical") >= 6):
            patterns.append(
                "Mathematical/analytical aptitude supports medical interest"
            )

        # Check for entertainment/performance patterns (VA, CA could support entertainment)
        if (
            safe_get_score(dbda_scores, "VA") >= 7
            or safe_get_score(dbda_scores, "CA") >= 7
        ) and (
            safe_get_score(cii_scores, "entertainment") >= 6
            or safe_get_score(cii_scores, "performing") >= 6
        ):
            patterns.append(
                "Creative aptitudes strongly support entertainment and performance interests"
            )

        return (
            patterns
            if patterns
            else ["Aptitude-interest patterns require individual analysis"]
        )

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
