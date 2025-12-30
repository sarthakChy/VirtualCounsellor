from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class ResourcePlanningOutput(BaseModel):
    """Output structure for resource planning"""

    financial_planning: Dict[str, Any] = Field(
        description="Detailed financial requirements and options"
    )
    study_resources: Dict[str, List[str]] = Field(
        description="Specific study materials and tools needed"
    )
    support_system_requirements: List[str] = Field(
        description="Human resources and mentorship needs"
    )
    technology_requirements: List[str] = Field(
        description="Digital tools and technology needs"
    )
    alternative_resource_options: Dict[str, List[str]] = Field(
        description="Budget-friendly alternatives"
    )


class ResourcePlanningSubAgent:
    """Sub-agent for dynamic resource planning based on student's financial and geographical constraints"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=ResourcePlanningOutput)

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "career_pathway",
                "financial_context",
                "location_context",
                "grade_timeline",
            ],
            template="""You are a Resource Planning Specialist helping Indian students optimize their educational resource allocation.

STUDENT PROFILE:
{student_profile}

CAREER PATHWAY:
{career_pathway}

FINANCIAL CONTEXT:
{financial_context}

LOCATION CONTEXT:
{location_context}

GRADE & TIMELINE:
{grade_timeline}

Create a comprehensive resource plan that:

1. FINANCIAL PLANNING:
   - Detailed cost breakdown for their specific pathway
   - Prioritized spending recommendations
   - Cost-saving strategies without compromising quality
   - Scholarship and financial aid opportunities
   - Payment timeline planning

2. STUDY RESOURCES:
   - Grade-appropriate and pathway-specific materials
   - Digital vs physical resource recommendations
   - Free and paid resource options
   - Quality vs cost analysis
   - Resource sharing opportunities

3. SUPPORT SYSTEM REQUIREMENTS:
   - Types of mentors and counselors needed
   - Peer study groups and communities
   - Professional guidance requirements
   - Family involvement optimization
   - Online vs offline support preferences

4. TECHNOLOGY REQUIREMENTS:
   - Essential digital tools for their pathway
   - Hardware requirements (if any)
   - Internet and connectivity needs
   - Educational apps and software
   - Budget-conscious technology choices

5. ALTERNATIVE RESOURCE OPTIONS:
   - Low-cost alternatives for expensive resources
   - Free online alternatives to paid coaching
   - Community resources and libraries
   - Government schemes and programs
   - Creative resource optimization

Consider their specific financial situation, location constraints, and career goals to make practical recommendations.

{format_instructions}""",
        )

    def generate_resource_plan(
        self,
        student_profile: str,
        career_pathway: str,
        financial_context: str,
        location_context: str,
        grade_timeline: str,
    ) -> Dict[str, Any]:
        """Generate personalized resource planning"""

        prompt_input = {
            "student_profile": student_profile,
            "career_pathway": career_pathway,
            "financial_context": financial_context,
            "location_context": location_context,
            "grade_timeline": grade_timeline,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        return self._parse_llm_response(llm_response)

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
