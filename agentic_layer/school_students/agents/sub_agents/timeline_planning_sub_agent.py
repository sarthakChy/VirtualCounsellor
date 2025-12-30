from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class TimelinePlanningOutput(BaseModel):
    """Output structure for timeline planning"""

    immediate_action_plan: List[str] = Field(
        description="Specific actions for next 1-3 months"
    )
    monthly_review_schedule: Dict[str, List[str]] = Field(
        description="Monthly review and adjustment points"
    )
    critical_deadlines: List[Dict[str, str]] = Field(
        description="Key deadlines and their importance"
    )
    milestone_tracking: Dict[str, List[str]] = Field(
        description="How to track progress on key milestones"
    )
    contingency_planning: List[str] = Field(
        description="Backup plans for potential issues"
    )


class TimelinePlanningSubAgent:
    """Sub-agent for dynamic timeline planning based on student's specific situation"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=TimelinePlanningOutput)

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "current_grade",
                "career_goals",
                "entrance_exams",
                "constraints",
            ],
            template="""You are an Educational Timeline Specialist creating personalized academic schedules for Indian school students.

STUDENT PROFILE:
{student_profile}

CURRENT GRADE: {current_grade}

CAREER GOALS:
{career_goals}

RELEVANT ENTRANCE EXAMS:
{entrance_exams}

CONSTRAINTS & CONTEXT:
{constraints}

Create a highly personalized timeline that considers:

1. IMMEDIATE ACTION PLAN (Next 1-3 months):
   - Specific, actionable steps based on current grade and time of year
   - Academic calendar considerations (term exams, holidays, etc.)
   - Preparation milestones for upcoming entrance exams
   - Skill development activities they can start now

2. MONTHLY REVIEW SCHEDULE:
   - Grade-specific review points
   - Performance tracking mechanisms
   - Adjustment triggers and decision points
   - Family involvement checkpoints

3. CRITICAL DEADLINES:
   - Entrance exam registration and preparation milestones
   - Stream selection deadlines (for applicable grades)
   - College application deadlines
   - Scholarship and financial aid deadlines

4. MILESTONE TRACKING:
   - Specific metrics for tracking progress
   - Early warning indicators
   - Celebration points for achievements
   - Course correction mechanisms

5. CONTINGENCY PLANNING:
   - Backup plans for different scenarios
   - Alternative pathways if primary plans change
   - Resource constraints adaptations
   - Emergency adjustment strategies

Make everything specific to this student's grade, career goals, and personal situation.

{format_instructions}""",
        )

    def generate_timeline(
        self,
        student_profile: str,
        current_grade: str,
        career_goals: str,
        entrance_exams: List[str],
        constraints: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate personalized timeline planning"""

        prompt_input = {
            "student_profile": student_profile,
            "current_grade": current_grade,
            "career_goals": career_goals,
            "entrance_exams": (
                ", ".join(entrance_exams) if entrance_exams else "To be determined"
            ),
            "constraints": json.dumps(constraints, indent=2),
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
