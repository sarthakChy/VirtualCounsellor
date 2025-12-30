from typing import Dict, List, Any, Optional
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class ExtractionResult(BaseModel):
    """Model for extraction results"""

    extracted_value: Any = Field(description="The extracted information")
    confidence_score: float = Field(description="Confidence in extraction (0-1)")
    source_context: str = Field(description="Which data sources were used")
    reasoning: str = Field(description="Brief explanation of extraction logic")


class SmartDataExtractionAgent:
    """
    Smart LLM-based data extraction agent that can extract any type of information
    from validated input data using natural language instructions.
    """

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=ExtractionResult)

        # Generic extraction prompt template
        self.extraction_prompt = PromptTemplate(
            input_variables=[
                "extraction_task",
                "available_data",
                "output_format",
                "format_instructions",
            ],
            template="""You are a smart data extraction agent. Your job is to analyze the provided data and extract specific information as requested.

EXTRACTION TASK: {extraction_task}

AVAILABLE DATA:
{available_data}

EXPECTED OUTPUT FORMAT: {output_format}

Instructions:
1. Carefully analyze ALL the provided data sources
2. Extract the most relevant and accurate information for the specified task
3. Provide a confidence score (0-1) based on data quality and completeness
4. Mention which data sources you used in your extraction
5. Provide brief reasoning for your extraction approach
6. If the requested information is not available, return appropriate defaults or "Unknown"
7. Be smart about inferring information from context when direct data isn't available

{format_instructions}

Return your response as valid JSON only.""",
        )

    def extract_information(
        self,
        extraction_task: str,
        validated_input: Dict[str, Any],
        output_format: str = "string",
        context: str = "",
    ) -> ExtractionResult:
        """
        Extract specific information using LLM intelligence

        Args:
            extraction_task: What to extract (e.g., "student's primary education field")
            validated_input: The complete validated input data
            output_format: Expected format (string, list, dict, etc.)
            context: Additional context for extraction
        """

        # Prepare data summary for LLM
        available_data = self._prepare_data_summary(validated_input)

        # Add context if provided
        full_task = f"{extraction_task}. {context}" if context else extraction_task

        # Format the prompt
        prompt_inputs = {
            "extraction_task": full_task,
            "available_data": available_data,
            "output_format": output_format,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.extraction_prompt.format(**prompt_inputs)

        # Get LLM response
        response = self.llm_model.invoke(formatted_prompt)

        # Parse response
        try:
            result_dict = self._parse_llm_response(response)
            return ExtractionResult(**result_dict)
        except Exception as e:
            # Fallback result
            return ExtractionResult(
                extracted_value="Unknown",
                confidence_score=0.0,
                source_context="Error in extraction",
                reasoning=f"Failed to extract: {str(e)}",
            )

    def _prepare_data_summary(self, validated_input: Dict[str, Any]) -> str:
        """Prepare a comprehensive but concise summary of available data"""
        data_summary = []

        # Resume data
        resume_data = validated_input.get("optional_data", {}).get("resume_data")
        if resume_data:
            content = resume_data.get("content", "")[:2000]  # Limit size
            data_summary.append(f"RESUME CONTENT:\n{content}")

            # Add metadata if available
            filename = resume_data.get("filename", "")
            if filename:
                data_summary.append(f"Resume file: {filename}")

        # Academic status
        academic_status = validated_input.get("optional_data", {}).get(
            "academic_status"
        )
        if academic_status:
            data_summary.append(
                f"ACADEMIC STATUS:\n{json.dumps(academic_status, indent=2)}"
            )

        # LinkedIn profile
        linkedin_profile = validated_input.get("optional_data", {}).get(
            "linkedin_profile"
        )
        if linkedin_profile:
            data_summary.append(
                f"LINKEDIN PROFILE:\n{json.dumps(linkedin_profile, indent=2)}"
            )

        # GitHub profile
        github_profile = validated_input.get("optional_data", {}).get("github_profile")
        if github_profile:
            data_summary.append(
                f"GITHUB PROFILE:\n{json.dumps(github_profile, indent=2)}"
            )

        # Previous analysis outputs
        previous_outputs = validated_input.get("previous_outputs", {})
        if previous_outputs:
            for agent_name, output in previous_outputs.items():
                if hasattr(output, "output_data"):
                    # Summarize key insights from previous agents
                    output_summary = self._summarize_previous_output(output.output_data)
                    data_summary.append(
                        f"PREVIOUS ANALYSIS ({agent_name.upper()}):\n{output_summary}"
                    )

        # Context data
        context_data = validated_input.get("context_data", {})
        if context_data:
            vertical_info = context_data.get("vertical_info", {})
            if vertical_info:
                data_summary.append(f"CONTEXT: {vertical_info.get('description', '')}")

        return "\n\n".join(data_summary)

    def _summarize_previous_output(self, output_data: Dict[str, Any]) -> str:
        """Summarize key insights from previous agent outputs"""
        summary_parts = []

        if "comprehensive_analysis" in output_data:
            comp_analysis = output_data["comprehensive_analysis"]

            # Key strengths
            strengths = comp_analysis.get("key_strengths", [])
            if strengths:
                summary_parts.append(f"Key Strengths: {', '.join(strengths[:3])}")

            # Profile positioning
            positioning = comp_analysis.get("profile_positioning", "")
            if positioning:
                summary_parts.append(f"Profile Focus: {positioning[:200]}")

            # Improvement areas
            improvements = comp_analysis.get("improvement_priorities", [])
            if improvements:
                summary_parts.append(
                    f"Improvement Areas: {', '.join(improvements[:2])}"
                )

        return (
            "; ".join(summary_parts) if summary_parts else json.dumps(output_data)[:300]
        )

    def _parse_llm_response(self, response) -> Dict[str, Any]:
        """Parse LLM response to extract JSON"""
        content = response.content.strip()

        # Clean markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try with output parser
            return self.output_parser.parse(content)
