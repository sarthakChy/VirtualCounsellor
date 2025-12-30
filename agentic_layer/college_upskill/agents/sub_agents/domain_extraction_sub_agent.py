from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class DomainExtractionOutput(BaseModel):
    """Output structure for domain extraction"""

    specific_domains: List[str] = Field(
        description="Specific domains from student profile"
    )
    intermediate_domains: List[str] = Field(
        description="Bridge domains connecting to market categories"
    )
    broad_market_categories: List[str] = Field(
        description="Broad market categories for trend analysis"
    )
    domain_hierarchy: Dict[str, Dict[str, List[str]]] = Field(
        description="Mapping between domain levels"
    )
    extraction_reasoning: str = Field(description="Reasoning behind domain selection")


class DomainExtractionSubAgent:
    """Sub-agent for dynamic domain extraction with three-level hierarchy"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=DomainExtractionOutput)

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "education_field",
                "skills",
                "experience",
                "interests",
            ],
            template="""You are a Career Domain Mapping Specialist. Extract career domains using a three-level hierarchy approach.

STUDENT PROFILE:
Education Field: {education_field}
Skills: {skills}
Experience: {experience}  
Interests: {interests}
Full Profile: {student_profile}

DOMAIN EXTRACTION FRAMEWORK:

Level 1 - SPECIFIC DOMAINS (Student's actual field):
- Extract 3-5 specific sub-domains within the student's field of study/work
- Be precise and field-specific (e.g., "Clinical Psychology" not just "Psychology")
- Consider specializations, research areas, or application domains

Level 2 - INTERMEDIATE DOMAINS (Bridge categories):
- Identify 3-5 broader professional categories that connect the specific domains to market opportunities
- These bridge the gap between academic/specific areas and market sectors
- Consider career paths, industry applications, and cross-functional opportunities

Level 3 - BROAD MARKET CATEGORIES (Market analysis targets):
- Map to 3-4 major market sectors for trend analysis
- Use standard industry categories (Healthcare, Technology, Finance, Education, etc.)
- These will be used for salary data, job market trends, and growth projections

MAPPING RULES:
1. Skills-based mapping: Technical skills can bridge to different markets
2. Interest-based mapping: Personal interests can open new sector opportunities  
3. Experience-based mapping: Work experience creates pathways to related industries
4. Academic-based mapping: Field of study has natural market connections

EXAMPLES:
Psychology Student:
- Specific: ["Clinical Psychology", "Research Psychology", "Mental Health Advocacy"]
- Intermediate: ["Healthcare Services", "Research & Academia", "Health Technology"]
- Broad: ["Healthcare", "Education", "Technology"]

Engineering Student:
- Specific: ["Software Development", "System Design", "Product Engineering"]
- Intermediate: ["Technology Services", "Product Development", "Technical Consulting"]
- Broad: ["Technology", "Manufacturing", "Finance"]

{format_instructions}

Focus on the student's actual background while identifying realistic market connections.""",
        )

    def extract_domains(
        self,
        student_profile: str,
        education_field: str,
        skills: List[str],
        experience: str,
        interests: str,
    ) -> Dict[str, Any]:
        """Extract three-level domain hierarchy from student profile"""

        prompt_input = {
            "student_profile": student_profile,
            "education_field": education_field,
            "skills": ", ".join(skills) if skills else "Not specified",
            "experience": experience,
            "interests": interests,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add semantic analysis
        result["semantic_analysis"] = self._analyze_domain_semantics(result)

        return result

    def _analyze_domain_semantics(self, extraction_result: Dict) -> Dict[str, Any]:
        """Analyze semantic relationships between domains"""
        specific = extraction_result.get("specific_domains", [])
        intermediate = extraction_result.get("intermediate_domains", [])
        broad = extraction_result.get("broad_market_categories", [])

        return {
            "domain_count": {
                "specific": len(specific),
                "intermediate": len(intermediate),
                "broad": len(broad),
            },
            "coverage_analysis": {
                "field_specificity": len(specific) >= 3,
                "market_bridge_strength": len(intermediate) >= 3,
                "market_breadth": len(broad) >= 2,
            },
        }

    def _parse_llm_response(self, response) -> Dict[str, Any]:
        """Parse LLM response with error handling"""
        content = response.content.strip()

        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as json_error:
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
                raise ValueError(
                    f"Failed to parse domain extraction response. "
                    f"JSON error: {json_error}. "
                    f"Parser error: {parser_error}."
                )
