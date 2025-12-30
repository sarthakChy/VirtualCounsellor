from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class ParentalAlignmentOutput(BaseModel):
    """Output structure for parental alignment guidance"""

    alignment_assessment: Dict[str, str] = Field(
        description="Assessment of parent-student alignment"
    )
    discussion_strategies: List[str] = Field(
        description="Strategies for family discussions"
    )
    compromise_solutions: List[str] = Field(
        description="Potential compromise approaches"
    )
    parent_education_points: List[str] = Field(
        description="Key points to educate parents about"
    )
    potential_conflicts: List[str] = Field(
        description="Potential areas of conflict and how to address them"
    )


class ParentalAlignmentSubAgent:
    """Sub-agent for handling parent-student alignment in stream selection"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=ParentalAlignmentOutput)

        self.prompt = PromptTemplate(
            input_variables=[
                "student_preferences",
                "family_expectations",
                "assessment_results",
                "recommended_streams",
            ],
            template="""You are a Family Counselor specializing in parent-student alignment for academic decisions in Indian families.

STUDENT'S ASSESSMENT-BASED PREFERENCES:
{student_preferences}

FAMILY EXPECTATIONS AND BACKGROUND:
{family_expectations}

OBJECTIVE ASSESSMENT RESULTS:
{assessment_results}

RECOMMENDED STREAMS:
{recommended_streams}

Analyze the alignment between family expectations and student's assessed capabilities/interests:

1. ALIGNMENT ASSESSMENT - Evaluate the degree of alignment:
   - Areas where family expectations match student's strengths
   - Significant misalignments and their implications
   - Underlying reasons for family preferences
   - Student's emotional response to family expectations

2. DISCUSSION STRATEGIES - Specific approaches for this family:
   - How to present assessment results effectively
   - Language and framing that resonates with these parents
   - Timing and setting for important conversations
   - Who should be involved in discussions

3. COMPROMISE SOLUTIONS - Practical middle-ground approaches:
   - Ways to honor both student potential and family concerns
   - Alternative pathways that satisfy both parties
   - Phased approaches to decision-making
   - Backup plans that address family security concerns

4. PARENT EDUCATION POINTS - What these specific parents need to understand:
   - Modern career landscape and opportunities
   - How their child's specific strengths translate to success
   - Risks of forcing unsuitable academic paths
   - Long-term benefits of aptitude-aligned choices

5. POTENTIAL CONFLICTS - Anticipate and prepare for:
   - Specific arguments parents might raise
   - Emotional responses from both sides
   - Cultural and generational differences
   - External pressures (relatives, society) affecting decisions

Focus on this specific family's dynamics, cultural context, and the unique challenges they face.

{format_instructions}""",
        )

    def assess_alignment(
        self,
        student_preferences: Dict,
        family_expectations: Dict,
        assessment_results: Dict,
        recommended_streams: List[Dict],
    ) -> Dict[str, Any]:
        """Assess parent-student alignment and provide guidance"""
        # Format the data for analysis
        prompt_input = {
            "student_preferences": json.dumps(student_preferences, indent=2),
            "family_expectations": json.dumps(family_expectations, indent=2),
            "assessment_results": json.dumps(assessment_results, indent=2),
            "recommended_streams": json.dumps(
                [
                    {
                        "stream": stream.get("stream_type", "Unknown"),
                        "score": stream.get("suitability_score", 0),
                        "reasoning": stream.get("primary_strengths_supporting", [])[:2],
                    }
                    for stream in recommended_streams[:3]
                ],
                indent=2,
            ),
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
