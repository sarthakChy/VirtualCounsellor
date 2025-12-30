from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class CareerReadinessOutput(BaseModel):
    """Output structure for career readiness assessment"""

    readiness_analysis: Dict[str, Any] = Field(
        description="Detailed readiness assessment"
    )
    development_areas: List[str] = Field(description="Areas needing development")
    strength_areas: List[str] = Field(description="Areas of strength to leverage")
    preparation_recommendations: List[str] = Field(
        description="Specific preparation steps"
    )
    timeline_considerations: Dict[str, str] = Field(
        description="Timeline factors for different careers"
    )


class CareerReadinessSubAgent:
    """Sub-agent for dynamic career readiness assessment"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=CareerReadinessOutput)

        self.prompt = PromptTemplate(
            input_variables=["student_data", "career_pathways", "assessment_scores"],
            template="""You are an Educational Psychologist specializing in career readiness assessment for school students.

STUDENT DATA:
{student_data}

CAREER PATHWAYS BEING CONSIDERED:
{career_pathways}

ASSESSMENT SCORES:
{assessment_scores}

Conduct a thorough career readiness assessment that:

1. READINESS ANALYSIS - Evaluate the student's preparation for each career path:
   - Academic foundation strength
   - Skill alignment with career requirements
   - Interest intensity and consistency
   - Emotional and psychological readiness
   - Support system availability

2. DEVELOPMENT AREAS - Identify specific areas needing growth:
   - Academic subjects requiring strengthening
   - Skills gaps that need addressing
   - Personality traits to develop
   - Knowledge areas to explore

3. STRENGTH AREAS - Highlight what the student can leverage:
   - Natural talents and abilities
   - Existing interests and passions
   - Developed skills and competencies
   - Supportive factors in their environment

4. PREPARATION RECOMMENDATIONS - Provide specific next steps:
   - Immediate actions they can take
   - Medium-term preparation strategies
   - Resources and tools to use
   - People to connect with

5. TIMELINE CONSIDERATIONS - Realistic timeframes for different careers:
   - How long until they can enter each field
   - Preparation time required
   - Key milestones and checkpoints
   - Flexibility and alternative pathways

Be honest about challenges while maintaining encouragement and optimism.

{format_instructions}""",
        )

    def assess_readiness(
        self, student_data: Dict, career_pathways: List[Dict], assessment_scores: Dict
    ) -> Dict[str, Any]:
        """Assess student's readiness for different career paths"""
        # Format career pathways for analysis
        pathway_summary = []
        for pathway in career_pathways[:5]:  # Top 5 pathways
            if isinstance(pathway, dict):
                pathway_summary.append(f"- {pathway.get('career_title', 'Unknown')}")

        prompt_input = {
            "student_data": json.dumps(student_data, indent=2),
            "career_pathways": "\n".join(pathway_summary),
            "assessment_scores": json.dumps(assessment_scores, indent=2),
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
