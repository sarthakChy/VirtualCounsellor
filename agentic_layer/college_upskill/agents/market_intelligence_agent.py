from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from agentic_layer.base_agent import BaseAgent
from config.agent_config import AgentType, MarketIntelligenceOutput
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agentic_layer.college_upskill.agents.sub_agents.domain_extraction_sub_agent import (
    DomainExtractionSubAgent,
)
from agentic_layer.college_upskill.agents.sub_agents.market_trend_analyzer_sub_agent import (
    MarketTrendAnalyzerSubAgent,
)
from agentic_layer.college_upskill.agents.sub_agents.salary_benchmarking_sub_agent import (
    SalaryBenchmarkingSubAgent,
)
from agentic_layer.college_upskill.agents.sub_agents.extraction_sub_agent import (
    SmartDataExtractionAgent,
)


class MarketIntelligenceAgent(BaseAgent):
    """
    Market Intelligence Agent for College Student Fleet

    Role: Industry Analyst and Trend Forecaster
    Purpose: Provides current job market analysis and emerging opportunities in student's domain

    Key Features:
    - Real-time job market trends analysis
    - Skill demand forecasting for next 2-3 years
    - Salary benchmarking for different career paths
    - Geographic opportunity mapping
    - Industry growth trajectory analysis
    - Dynamic domain extraction with LLM-based reasoning
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="market_intelligence",
            agent_name="Market Intelligence Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config,
        )

        self.domain_extraction_agent = DomainExtractionSubAgent(llm_model)
        self.trend_analyzer_agent = MarketTrendAnalyzerSubAgent(llm_model)
        self.salary_benchmarking_agent = SalaryBenchmarkingSubAgent(llm_model)
        self.extraction_agent = SmartDataExtractionAgent(llm_model)
        # Store domain analysis details for integration into final output
        self.domain_analysis_details = {}

    def _define_required_inputs(self) -> List[str]:
        """Define required inputs for market intelligence analysis"""
        return [
            # No strictly required inputs - can provide general market intelligence
            # But works better with profile context
        ]

    def _define_optional_inputs(self) -> List[str]:
        """Define optional inputs that enhance market analysis"""
        return [
            "resume_data",  # To understand student's domain/interests
            "linkedin_profile",  # For industry context
            "github_profile",  # For technical skill context
            "academic_status",  # For understanding student's field
            "profile_analysis_output",  # From previous agent for context
            "target_industries",  # Specific industries of interest
            "preferred_locations",  # Geographic preferences
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of market intelligence output"""
        return {
            "industry_trends": "Current trends and growth patterns",
            "skill_demand": "In-demand skills with priority levels",
            "salary_insights": "Compensation analysis and trends",
            "job_market_outlook": "Future opportunities and projections",
            "geographic_insights": "Location-based market data",
            "emerging_technologies": "New technologies and their impact",
            "market_recommendations": "Strategic advice for students",
            "domain_selection_reasoning": "Explanation of how target domains were identified",
        }

    def _initialize_agent(self):
        """Initialize agent-specific components"""
        # 3. SIMPLIFIED INITIALIZATION - SUB-AGENTS HANDLE THEIR OWN PROMPTS
        self.output_parser = JsonOutputParser(pydantic_object=MarketIntelligenceOutput)

        # Simple orchestration prompt instead of complex analysis prompt
        self.orchestration_prompt = PromptTemplate(
            input_variables=[
                "domain_extraction_result",
                "trend_analysis_result",
                "salary_analysis_result",
                "synthesis_context",
                "format_instructions",
            ],
            template="""You are a Market Intelligence Orchestrator synthesizing comprehensive career market analysis.

DOMAIN EXTRACTION RESULTS:
{domain_extraction_result}

TREND ANALYSIS RESULTS:
{trend_analysis_result}

SALARY ANALYSIS RESULTS:
{salary_analysis_result}

SYNTHESIS CONTEXT:
{synthesis_context}

Your role is to synthesize these specialized analyses into coherent market intelligence recommendations for a college student.

Create a comprehensive market intelligence report that:
1. Integrates domain-specific trends with broader market patterns
2. Connects salary insights to career development strategy
3. Provides actionable recommendations based on the multi-level domain analysis
4. Highlights cross-domain opportunities and emerging intersections
5. Gives clear next steps for market positioning and skill development

{format_instructions}

Focus on synthesis rather than re-analysis - the specialized sub-agents have provided the detailed analysis.""",
        )

        self.logger.info(
            "Market Intelligence Agent initialized with dynamic domain extraction"
        )

    @traceable(
        name="market_intelligence_analysis",
        tags=["market_intelligence", "comprehensive", "llm_chain"],
    )
    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core market intelligence analysis logic using sub-agents"""
        self._add_processing_note(
            "Starting market intelligence analysis with sub-agent architecture"
        )

        # Step 1: Extract student context for domain extraction
        education_field = self._extract_education_field(validated_input)
        skills = self._extract_skills_list(validated_input)
        experience = self._extract_experience_summary(validated_input)
        interests = self._extract_interests(validated_input)
        student_context = f"Education: {education_field}, Skills: {', '.join(skills[:5])}, Experience: {experience}"

        # Step 2: Use Domain Extraction Sub-Agent
        self._add_processing_note("Executing domain extraction sub-agent")
        domain_extraction_result = self.domain_extraction_agent.extract_domains(
            student_profile=student_context,
            education_field=education_field,
            skills=skills,
            experience=experience,
            interests=interests,
        )

        # Step 3: Use Market Trend Analyzer Sub-Agent
        self._add_processing_note("Executing market trend analysis sub-agent")
        trend_analysis_result = self.trend_analyzer_agent.analyze_trends(
            specific_domains=domain_extraction_result.get("specific_domains", []),
            intermediate_domains=domain_extraction_result.get(
                "intermediate_domains", []
            ),
            broad_categories=domain_extraction_result.get(
                "broad_market_categories", []
            ),
            domain_hierarchy=domain_extraction_result.get("domain_hierarchy", {}),
        )

        # Step 4: Use Salary Benchmarking Sub-Agent
        self._add_processing_note("Executing salary benchmarking sub-agent")
        salary_analysis_result = self.salary_benchmarking_agent.analyze_compensation(
            specific_domains=domain_extraction_result.get("specific_domains", []),
            intermediate_domains=domain_extraction_result.get(
                "intermediate_domains", []
            ),
            broad_categories=domain_extraction_result.get(
                "broad_market_categories", []
            ),
            student_context=self._extract_student_level(validated_input),
        )

        # Step 5: Synthesize results using orchestration prompt
        self._add_processing_note("Synthesizing sub-agent results")
        synthesis_context = self._build_synthesis_context(validated_input)

        prompt_inputs = {
            "domain_extraction_result": json.dumps(domain_extraction_result, indent=2),
            "trend_analysis_result": json.dumps(trend_analysis_result, indent=2),
            "salary_analysis_result": json.dumps(salary_analysis_result, indent=2),
            "synthesis_context": synthesis_context,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.orchestration_prompt.format(**prompt_inputs)
        response = self.llm_model.invoke(formatted_prompt)
        output_dict = self._parse_llm_response(response)

        # Step 6: Add comprehensive metadata from sub-agents
        output_dict["domain_selection_reasoning"] = {
            "extraction_method": "Multi-level LLM-based domain hierarchy",
            "specific_domains": domain_extraction_result.get("specific_domains", []),
            "intermediate_domains": domain_extraction_result.get(
                "intermediate_domains", []
            ),
            "broad_market_categories": domain_extraction_result.get(
                "broad_market_categories", []
            ),
            "domain_hierarchy": domain_extraction_result.get("domain_hierarchy", {}),
            "extraction_reasoning": domain_extraction_result.get(
                "extraction_reasoning", ""
            ),
            "semantic_analysis": domain_extraction_result.get("semantic_analysis", {}),
        }

        # Step 7: Add sub-agent analysis metadata
        output_dict["analysis_metadata"] = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "sub_agent_architecture": "Domain Extraction → Trend Analysis → Salary Benchmarking → Synthesis",
            "domain_extraction_confidence": self._calculate_domain_confidence(
                domain_extraction_result
            ),
            "trend_analysis_scope": len(
                trend_analysis_result.get("domain_specific_trends", {})
            ),
            "salary_analysis_coverage": len(
                salary_analysis_result.get("domain_salary_ranges", {})
            ),
            "geographic_scope": "India (Tier 1, Tier 2, Remote)",
            "synthesis_quality_score": self._assess_synthesis_quality(output_dict),
        }

        self._add_processing_note(
            "Market intelligence analysis completed with sub-agent integration"
        )
        return output_dict

    def _extract_education_field(self, validated_input: Dict[str, Any]) -> str:
        """Extract primary education field using smart extraction"""
        task = """Extract the student's primary education field or academic major. 
        Look for degree information, major subjects, field of study, or specialization. 
        Return a concise field name (e.g., 'Computer Science', 'Psychology', 'Mechanical Engineering', 'Business Administration')."""

        result = self.extraction_agent.extract_information(
            extraction_task=task,
            validated_input=validated_input,
            output_format="string",
            context="Focus on the main academic discipline or area of study",
        )

        return result.extracted_value

    def _extract_skills_list(self, validated_input: Dict[str, Any]) -> List[str]:
        """Extract skills list using smart extraction"""
        task = """Extract a comprehensive list of the student's technical skills, tools, programming languages, 
        software proficiencies, and relevant competencies. Include both hard skills (technical) and relevant 
        soft skills mentioned. Return as a list of individual skills."""

        result = self.extraction_agent.extract_information(
            extraction_task=task,
            validated_input=validated_input,
            output_format="list of strings",
            context="Include technical skills, software, programming languages, research tools, and key competencies",
        )

        if isinstance(result.extracted_value, list):
            return result.extracted_value
        elif isinstance(result.extracted_value, str):
            # Try to parse as comma-separated if returned as string
            return [
                skill.strip()
                for skill in result.extracted_value.split(",")
                if skill.strip()
            ]
        else:
            return []

    def _extract_experience_summary(self, validated_input: Dict[str, Any]) -> str:
        """Extract experience summary using smart extraction"""
        task = """Summarize the student's work experience, internships, research positions, projects, 
        and relevant extracurricular activities. Provide a concise but informative summary that captures 
        their professional journey and key experiences."""

        result = self.extraction_agent.extract_information(
            extraction_task=task,
            validated_input=validated_input,
            output_format="string",
            context="Focus on work experience, internships, research, projects, and leadership roles",
        )

        return result.extracted_value

    def _extract_interests(self, validated_input: Dict[str, Any]) -> str:
        """Extract interests and career aspirations using smart extraction"""
        task = """Extract the student's career interests, professional aspirations, areas of passion, 
        and fields they want to work in. Look for explicitly stated interests as well as implied interests 
        from their activities, projects, and experiences."""

        result = self.extraction_agent.extract_information(
            extraction_task=task,
            validated_input=validated_input,
            output_format="string",
            context="Look for career goals, professional interests, hobby interests that relate to career, and aspirational fields",
        )

        return result.extracted_value

    def _extract_student_level(self, validated_input: Dict[str, Any]) -> str:
        """Extract student academic level for salary context"""
        academic_status = validated_input.get("optional_data", {}).get(
            "academic_status"
        )
        if academic_status:
            year = academic_status.get("current_year", "Unknown")
            major = academic_status.get("major", "Unknown")
            return f"{year} year {major} student"

        return "College student seeking career guidance"

    def _build_synthesis_context(self, validated_input: Dict[str, Any]) -> str:
        """Build context for final synthesis"""
        context_parts = []

        # Geographic preferences
        preferred_locations = validated_input.get("optional_data", {}).get(
            "preferred_locations"
        )
        if preferred_locations:
            context_parts.append(f"Geographic preferences: {preferred_locations}")
        else:
            context_parts.append(
                "Geographic focus: Indian market with global remote opportunities"
            )

        # Career stage
        academic_status = validated_input.get("optional_data", {}).get(
            "academic_status"
        )
        if academic_status:
            year = academic_status.get("current_year", "Unknown")
            context_parts.append(
                f"Career stage: {year} year student preparing for job market entry"
            )

        # Previous analysis context
        previous_outputs = validated_input.get("previous_outputs", {})
        if previous_outputs.get("profile_analysis"):
            context_parts.append(
                "Profile analysis available from previous agent for integration"
            )

        return (
            "; ".join(context_parts)
            if context_parts
            else "General career guidance context"
        )

    def _calculate_domain_confidence(
        self, domain_extraction_result: Dict[str, Any]
    ) -> float:
        """Calculate confidence in domain extraction from sub-agent"""
        base_confidence = 0.8

        # Check completeness of domain hierarchy
        specific_domains = domain_extraction_result.get("specific_domains", [])
        intermediate_domains = domain_extraction_result.get("intermediate_domains", [])
        broad_categories = domain_extraction_result.get("broad_market_categories", [])

        if len(specific_domains) >= 3:
            base_confidence += 0.05
        if len(intermediate_domains) >= 3:
            base_confidence += 0.05
        if len(broad_categories) >= 2:
            base_confidence += 0.05

        # Check reasoning quality
        reasoning = domain_extraction_result.get("extraction_reasoning", "")
        if len(reasoning) > 100:
            base_confidence += 0.05

        return min(0.95, base_confidence)

    def _assess_synthesis_quality(self, output_dict: Dict[str, Any]) -> float:
        """Assess quality of final synthesis"""
        quality_score = 0.7

        # Check output completeness
        expected_keys = [
            "industry_trends",
            "skill_demand",
            "salary_insights",
            "job_market_outlook",
            "geographic_insights",
            "emerging_technologies",
        ]

        completed_keys = sum(
            1 for key in expected_keys if key in output_dict and output_dict[key]
        )
        quality_score += (completed_keys / len(expected_keys)) * 0.2

        # Check integration quality
        if output_dict.get("domain_selection_reasoning"):
            quality_score += 0.05

        if output_dict.get("market_recommendations"):
            quality_score += 0.05

        return min(0.95, quality_score)

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
