from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class CollegeMatchingOutput(BaseModel):
    """Output structure for college matching"""

    matched_colleges: List[Dict[str, Any]] = Field(
        description="Colleges matched to student profile"
    )
    ranking_analysis: Dict[str, Any] = Field(
        description="Ranking-based analysis and recommendations"
    )
    geographic_distribution: Dict[str, List[str]] = Field(
        description="Region-wise college options"
    )
    admission_probability: Dict[str, str] = Field(
        description="Probability assessment for different colleges"
    )
    next_steps: List[str] = Field(
        description="Immediate actions for college applications"
    )


class CollegeMatchingSubAgent:
    """Sub-agent for dynamic college matching based on student profile and preferences"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=CollegeMatchingOutput)

        # College database categories for Indian institutions
        self.college_categories = {
            "Engineering": {
                "Tier1": [
                    "IIT Delhi",
                    "IIT Bombay",
                    "IIT Madras",
                    "IIT Kanpur",
                    "IIT Kharagpur",
                ],
                "Tier2": [
                    "NIT Trichy",
                    "NIT Warangal",
                    "NIT Surathkal",
                    "IIIT Hyderabad",
                    "DTU Delhi",
                ],
                "Private_Premium": [
                    "BITS Pilani",
                    "VIT Vellore",
                    "Manipal Institute",
                    "Thapar University",
                ],
                "Regional_Strong": [
                    "State Engineering Colleges",
                    "Regional Technical Universities",
                ],
            },
            "Medicine": {
                "Premier": [
                    "AIIMS Delhi",
                    "CMC Vellore",
                    "JIPMER Puducherry",
                    "KGMU Lucknow",
                ],
                "Government": [
                    "State Medical Colleges",
                    "Central Universities Medical",
                    "Military Medical",
                ],
                "Private_Established": [
                    "Kasturba Medical",
                    "JSS Medical",
                    "Amrita Medical",
                ],
                "Emerging": ["New Medical Colleges", "Private Medical Universities"],
            },
            "Business": {
                "Top_Tier": [
                    "IIM Ahmedabad",
                    "IIM Bangalore",
                    "IIM Calcutta",
                    "ISB Hyderabad",
                ],
                "Government": ["FMS Delhi", "JBIMS Mumbai", "DoMS IIT", "SJMSOM IIT"],
                "Private_Premium": ["XLRI Jamshedpur", "MDI Gurgaon", "SPJIMR Mumbai"],
                "Regional": ["Regional Management Institutes", "State Universities"],
            },
            "Liberal_Arts": {
                "Premium": [
                    "Ashoka University",
                    "O.P. Jindal",
                    "Christ University",
                    "Symbiosis",
                ],
                "Government": ["DU Colleges", "JNU", "BHU", "Central Universities"],
                "Specialized": ["NIFT", "NID", "Film Schools", "Mass Communication"],
            },
        }

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "career_goals",
                "academic_profile",
                "preferences",
                "constraints",
            ],
            template="""You are a College Matching Specialist with deep knowledge of Indian higher education institutions.

STUDENT PROFILE:
{student_profile}

CAREER GOALS:
{career_goals}

ACADEMIC PROFILE:
{academic_profile}

PREFERENCES:
{preferences}

CONSTRAINTS:
{constraints}

Perform comprehensive college matching analysis:

1. PROFILE-BASED MATCHING:
   - Analyze academic strength vs college requirements
   - Match career goals to program offerings
   - Consider entrance exam performance expectations
   - Factor in extracurricular achievements

2. STRATEGIC CATEGORIZATION:
   - Reach colleges (aspirational based on best-case performance)
   - Match colleges (realistic based on current trajectory) 
   - Safety colleges (high probability of admission)
   - Consider both merit and management quota options

3. RANKING ANALYSIS:
   - NIRF rankings relevance to student goals
   - Industry reputation and placement records
   - Alumni network strength in preferred sectors
   - Research opportunities and faculty quality

4. GEOGRAPHIC DISTRIBUTION:
   - Home state advantages and quotas
   - Metropolitan vs tier-2 city opportunities
   - Cost-of-living considerations
   - Cultural and linguistic comfort factors

5. ADMISSION PROBABILITY ASSESSMENT:
   - Historical cutoffs and trends
   - Competition level analysis
   - Quota and reservation benefits
   - Alternative admission pathways (management quota, NRI, etc.)

Focus on specific, actionable recommendations with realistic admission probabilities.

{format_instructions}""",
        )

    def match_colleges(
        self,
        student_profile: str,
        career_goals: str,
        academic_profile: str,
        preferences: str,
        constraints: str,
    ) -> Dict[str, Any]:
        """Generate personalized college matching analysis"""

        prompt_input = {
            "student_profile": student_profile,
            "career_goals": career_goals,
            "academic_profile": academic_profile,
            "preferences": preferences,
            "constraints": constraints,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add computational analysis
        result["computational_insights"] = self._analyze_college_metrics(
            result.get("matched_colleges", [])
        )

        return result

    def _analyze_college_metrics(self, matched_colleges: List[Dict]) -> Dict[str, Any]:
        """Analyze quantitative metrics of matched colleges"""
        if not matched_colleges:
            return {"analysis": "No colleges matched for analysis"}

        metrics = {
            "total_colleges_matched": len(matched_colleges),
            "category_distribution": {},
            "geographic_spread": {},
            "admission_difficulty_levels": {"High": 0, "Medium": 0, "Low": 0},
        }

        # Analyze college categories and difficulty
        for college in matched_colleges:
            if isinstance(college, dict):
                # Category analysis
                college_type = college.get("college_type", "Unknown")
                metrics["category_distribution"][college_type] = (
                    metrics["category_distribution"].get(college_type, 0) + 1
                )

                # Geographic analysis
                location = college.get("location", "Unknown")
                state = location.split(",")[-1].strip() if "," in location else location
                metrics["geographic_spread"][state] = (
                    metrics["geographic_spread"].get(state, 0) + 1
                )

        return metrics

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
