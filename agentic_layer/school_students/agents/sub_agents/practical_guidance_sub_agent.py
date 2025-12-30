from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class PracticalGuidanceOutput(BaseModel):
    """Output structure for practical guidance"""

    exploration_timeline: Dict[str, List[str]] = Field(
        description="Personalized timeline for career exploration"
    )
    skill_development_priorities: List[str] = Field(
        description="Specific skills to develop based on student profile"
    )
    networking_opportunities: List[str] = Field(
        description="Relevant networking suggestions"
    )
    career_myths_addressed: List[str] = Field(
        description="Specific myths relevant to student's situation"
    )
    success_strategies: List[str] = Field(description="Tailored success strategies")


class PracticalGuidanceSubAgent:
    """Sub-agent for generating dynamic practical guidance"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=PracticalGuidanceOutput)

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "career_recommendations",
                "assessment_data",
                "context",
            ],
            template="""You are a Career Guidance Counselor specializing in practical, actionable advice for Indian school students. 

STUDENT PROFILE:
{student_profile}

TOP CAREER RECOMMENDATIONS:
{career_recommendations}

ASSESSMENT DATA:
{assessment_data}

CONTEXT:
{context}

Provide highly personalized, practical guidance that:

1. EXPLORATION TIMELINE - Create specific timelines based on:
   - Student's current grade and academic calendar
   - Specific career paths they're considering
   - Entrance exam schedules and preparation time
   - College application deadlines

2. SKILL DEVELOPMENT PRIORITIES - Identify specific skills based on:
   - Gap analysis between current abilities and career requirements
   - Student's learning preferences and available resources
   - Industry-specific skill demands
   - Both technical and soft skills needed

3. NETWORKING OPPORTUNITIES - Suggest relevant networking based on:
   - Student's location and available resources
   - Specific industries they're interested in
   - Their comfort level with networking
   - Age-appropriate networking activities

4. CAREER MYTHS - Address specific myths relevant to:
   - The career fields they're considering
   - Common misconceptions in their family/social context
   - Gender or social stereotypes they might face
   - Economic concerns about their chosen fields

5. SUCCESS STRATEGIES - Provide tailored strategies based on:
   - Their personality and learning style
   - Specific challenges in their target careers
   - Their strengths and how to leverage them
   - Current trends in their fields of interest

Make everything specific, actionable, and relevant to this individual student's situation.

{format_instructions}""",
        )

    def generate_guidance(
        self,
        student_profile: str,
        career_recommendations: List[Dict],
        assessment_data: Dict,
        context: Dict,
    ) -> Dict[str, Any]:
        """Generate personalized practical guidance"""
        # Format career recommendations for context
        career_summary = []
        for career in career_recommendations[:3]:  # Top 3 careers
            if isinstance(career, dict):
                career_summary.append(
                    f"- {career.get('career_title', 'Unknown')}: {career.get('suitability_score', 0):.2f} suitability"
                )

        prompt_input = {
            "student_profile": student_profile,
            "career_recommendations": "\n".join(career_summary),
            "assessment_data": json.dumps(assessment_data, indent=2),
            "context": json.dumps(context, indent=2),
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
