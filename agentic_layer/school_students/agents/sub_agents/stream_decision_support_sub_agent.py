from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class StreamDecisionSupportOutput(BaseModel):
    """Output structure for stream decision support"""

    personalized_decision_factors: List[str] = Field(
        description="Factors specific to this student's situation"
    )
    addressed_misconceptions: List[str] = Field(
        description="Misconceptions relevant to student's context"
    )
    tailored_success_strategies: List[str] = Field(
        description="Success strategies based on recommended streams"
    )
    specific_warning_signs: List[str] = Field(
        description="Contextual warning signs and concerns"
    )
    family_discussion_guide: List[str] = Field(
        description="Talking points for family discussions"
    )


class StreamDecisionSupportSubAgent:
    """Sub-agent for generating dynamic stream decision support"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(
            pydantic_object=StreamDecisionSupportOutput
        )

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "recommended_streams",
                "assessment_scores",
                "family_context",
                "academic_performance",
            ],
            template="""You are an experienced Academic Counselor specializing in Indian education system stream selection.

STUDENT PROFILE:
{student_profile}

RECOMMENDED STREAMS:
{recommended_streams}

ASSESSMENT SCORES:
{assessment_scores}

FAMILY CONTEXT:
{family_context}

ACADEMIC PERFORMANCE:
{academic_performance}

Provide highly personalized stream decision support that addresses:

1. PERSONALIZED DECISION FACTORS - Based on this specific student:
   - Their unique strengths and challenges
   - Family situation and expectations
   - Academic track record and capacity
   - Specific career interests mentioned
   - Financial and geographical constraints

2. ADDRESSED MISCONCEPTIONS - Target myths relevant to THIS student:
   - Family beliefs that may not apply to this student
   - Common misconceptions about their top recommended streams
   - Career myths related to their specific interests
   - Social pressures they might be facing

3. TAILORED SUCCESS STRATEGIES - Specific to recommended streams:
   - Concrete steps for their top stream choices
   - Subject-specific preparation advice
   - Skill development priorities based on their gaps
   - Timeline planning for their grade level

4. SPECIFIC WARNING SIGNS - Red flags for this particular case:
   - Misalignment between family expectations and aptitudes
   - Potential stress points in recommended streams
   - Academic challenges they might face
   - Decision paralysis or pressure indicators

5. FAMILY DISCUSSION GUIDE - Help navigate family conversations:
   - How to present assessment results to parents
   - Arguments for non-traditional stream choices if applicable
   - Compromise strategies if family-student misalignment exists
   - Questions for parents to consider

Make everything specific to this student's situation, not generic advice.

{format_instructions}""",
        )

    def generate_support(
        self,
        student_profile: str,
        recommended_streams: List[Dict],
        assessment_scores: Dict,
        family_context: Dict,
        academic_performance: str,
    ) -> Dict[str, Any]:
        """Generate personalized stream decision support"""
        # Format recommended streams for context
        streams_summary = []
        for i, stream in enumerate(recommended_streams[:3], 1):
            if isinstance(stream, dict):
                streams_summary.append(
                    f"{i}. {stream.get('stream_type', 'Unknown')} - Suitability: {stream.get('suitability_score', 0):.2f}"
                )

        prompt_input = {
            "student_profile": student_profile,
            "recommended_streams": "\n".join(streams_summary),
            "assessment_scores": json.dumps(assessment_scores, indent=2),
            "family_context": json.dumps(family_context, indent=2),
            "academic_performance": academic_performance,
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
