from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class ScholarshipDiscoveryOutput(BaseModel):
    """Output structure for scholarship discovery"""

    prioritized_scholarships: List[Dict[str, Any]] = Field(
        description="Scholarships ranked by suitability and probability"
    )
    application_schedule: Dict[str, List[str]] = Field(
        description="Timeline for scholarship applications"
    )
    eligibility_optimization: Dict[str, List[str]] = Field(
        description="Ways to improve eligibility"
    )
    total_potential_funding: str = Field(
        description="Estimated total funding potential"
    )
    success_strategies: List[str] = Field(
        description="Strategies to maximize scholarship success"
    )


class ScholarshipDiscoverySubAgent:
    """Sub-agent for dynamic scholarship discovery and matching"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(
            pydantic_object=ScholarshipDiscoveryOutput
        )

        # Comprehensive scholarship database for Indian students
        self.scholarship_categories = {
            "Merit_Based": {
                "National_Level": [
                    "Kishore Vaigyanik Protsahan Yojana (KVPY)",
                    "National Talent Search Examination (NTSE)",
                    "Indian National Mathematical Olympiad (INMO)",
                    "National Science Olympiad (NSO)",
                ],
                "Entrance_Exam_Based": [
                    "JEE Merit Scholarships",
                    "NEET Merit Scholarships",
                    "BITSAT Scholarships",
                    "VIT Merit Scholarships",
                ],
                "Corporate_Sponsored": [
                    "Tata Scholarships",
                    "Reliance Foundation Scholarships",
                    "Aditya Birla Scholarships",
                    "Bajaj Auto Scholarships",
                ],
            },
            "Need_Based": {
                "Government_Schemes": [
                    "Post Matric Scholarship Scheme",
                    "Pre Matric Scholarship Scheme",
                    "Central Sector Scholarship Scheme",
                    "Prime Minister's Special Scholarship Scheme",
                ],
                "Private_Foundations": [
                    "Azim Premji Foundation Scholarships",
                    "Narotam Sekhsaria Foundation",
                    "K.C. Mahindra Education Trust",
                    "Sitaram Jindal Foundation",
                ],
                "Educational_Loans": [
                    "Education Loan Subsidy Schemes",
                    "Interest Subsidy on Education Loans",
                    "Collateral-free Education Loans",
                ],
            },
            "Category_Specific": {
                "SC_ST": [
                    "National Fellowship for SC/ST Students",
                    "Post Matric Scholarship for SC/ST",
                    "Top Class Education for SC/ST",
                    "Rajiv Gandhi National Fellowship",
                ],
                "OBC": [
                    "Post Matric Scholarship for OBC",
                    "Central Sector Scholarship for OBC",
                    "Merit-cum-Means Scholarship for OBC",
                ],
                "Minority": [
                    "Maulana Azad National Fellowship",
                    "Begum Hazrat Mahal National Scholarship",
                    "Merit-cum-Means Scholarship for Minorities",
                ],
                "Girl_Child": [
                    "National Scheme of Incentive to Girls",
                    "Udaan Scholarship for Girl Students",
                    "INSPIRE Scholarship for Girls in Science",
                ],
            },
            "International": {
                "Study_Abroad": [
                    "Fulbright-Nehru Fellowships",
                    "Commonwealth Scholarships",
                    "Inlaks Scholarships",
                    "JN Tata Endowment Scholarships",
                ],
                "Exchange_Programs": [
                    "Indian Government Scholarships for Foreign Students",
                    "ICCR Scholarships",
                    "University-specific Exchange Programs",
                ],
            },
        }

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "academic_achievements",
                "financial_need",
                "career_pathway",
                "demographic_info",
            ],
            template="""You are a Scholarship Discovery Specialist with comprehensive knowledge of Indian scholarship ecosystem.

STUDENT PROFILE:
{student_profile}

ACADEMIC ACHIEVEMENTS:
{academic_achievements}

FINANCIAL NEED ASSESSMENT:
{financial_need}

CAREER PATHWAY:
{career_pathway}

DEMOGRAPHIC INFORMATION:
{demographic_info}

Conduct comprehensive scholarship discovery and matching:

1. ELIGIBILITY ANALYSIS:
   - Academic merit requirements matching
   - Financial need criteria assessment
   - Demographic eligibility (category, gender, region)
   - Course/stream specific scholarships
   - Timeline and age requirements

2. SCHOLARSHIP PRIORITIZATION:
   - High probability + High value scholarships first
   - Government vs private scholarship balance
   - Long-term vs one-time funding
   - Renewable vs non-renewable options
   - Application difficulty vs benefit ratio

3. APPLICATION STRATEGY:
   - Optimal application timing and sequence
   - Documentation requirements preparation
   - Essays and personal statements guidance
   - Interview preparation for merit scholarships
   - Portfolio requirements for specialized scholarships

4. FINANCIAL IMPACT ANALYSIS:
   - Total potential funding calculation
   - Scholarship stacking possibilities
   - Loan reduction potential
   - ROI of scholarship applications
   - Alternative funding source integration

5. SUCCESS OPTIMIZATION:
   - Profile strengthening recommendations
   - Community service and leadership development
   - Academic performance improvement areas
   - Extracurricular activity alignment
   - Networking and recommendation letter strategies

Focus on actionable, specific recommendations with realistic probability assessments.

{format_instructions}""",
        )

    def discover_scholarships(
        self,
        student_profile: str,
        academic_achievements: str,
        financial_need: str,
        career_pathway: str,
        demographic_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate personalized scholarship discovery analysis"""

        prompt_input = {
            "student_profile": student_profile,
            "academic_achievements": academic_achievements,
            "financial_need": financial_need,
            "career_pathway": career_pathway,
            "demographic_info": json.dumps(demographic_info, indent=2),
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add computational analysis
        result["scholarship_analytics"] = self._analyze_scholarship_landscape(
            result.get("prioritized_scholarships", []), demographic_info
        )

        return result

    def _analyze_scholarship_landscape(
        self, scholarships: List[Dict], demographic_info: Dict
    ) -> Dict[str, Any]:
        """Analyze scholarship opportunities quantitatively"""
        if not scholarships:
            return {"analysis": "No scholarships analyzed"}

        analytics = {
            "total_opportunities": len(scholarships),
            "funding_categories": {},
            "application_timeline": {},
            "eligibility_overlap": 0,
            "demographic_advantages": [],
        }

        # Analyze scholarship categories
        for scholarship in scholarships:
            if isinstance(scholarship, dict):
                category = scholarship.get("scholarship_type", "General")
                analytics["funding_categories"][category] = (
                    analytics["funding_categories"].get(category, 0) + 1
                )

        # Analyze demographic advantages
        demo_info = demographic_info or {}
        if demo_info.get("category") in ["SC", "ST", "OBC"]:
            analytics["demographic_advantages"].append("Reservation category benefits")
        if demo_info.get("gender") == "Female":
            analytics["demographic_advantages"].append(
                "Girl child specific scholarships"
            )
        if demo_info.get("rural_background"):
            analytics["demographic_advantages"].append("Rural area specific schemes")

        return analytics

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
