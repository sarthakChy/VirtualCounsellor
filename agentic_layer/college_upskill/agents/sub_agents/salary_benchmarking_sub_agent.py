from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json
import re


class SalaryBenchmarkOutput(BaseModel):
    """Output structure for salary benchmarking"""

    domain_salary_ranges: Dict[str, Dict[str, Any]] = Field(
        description="Salary ranges by domain and experience level"
    )
    geographic_variations: Dict[str, Dict[str, Any]] = Field(
        description="Salary variations by location"
    )
    growth_trajectories: Dict[str, List[Dict[str, Any]]] = Field(
        description="Career progression and salary growth"
    )
    total_compensation_analysis: Dict[str, Any] = Field(
        description="Beyond base salary compensation"
    )
    market_positioning: Dict[str, str] = Field(
        description="How domains compare in compensation"
    )


class SalaryBenchmarkingSubAgent:
    """Sub-agent for salary and compensation analysis across domains"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=SalaryBenchmarkOutput)

        # Salary benchmarking framework
        self.experience_levels = [
            "Entry Level (0-2 years)",
            "Mid Level (2-5 years)",
            "Senior Level (5-10 years)",
            "Expert Level (10+ years)",
        ]

        self.indian_markets = {
            "Tier 1": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune"],
            "Tier 2": [
                "Ahmedabad",
                "Kolkata",
                "Jaipur",
                "Chandigarh",
                "Kochi",
                "Indore",
            ],
            "Remote": ["Remote India", "Remote Global"],
        }

        self.prompt = PromptTemplate(
            input_variables=[
                "specific_domains",
                "intermediate_domains",
                "broad_categories",
                "student_level",
            ],
            template="""You are a Compensation Analyst specializing in salary benchmarking across career domains in the Indian market context.

TARGET DOMAINS FOR ANALYSIS:
Specific Domains: {specific_domains}
Intermediate Domains: {intermediate_domains}
Broad Market Categories: {broad_categories}
Student Context: {student_level}

SALARY BENCHMARKING FRAMEWORK:

1. DOMAIN SALARY RANGES:
For each specific domain, provide:
- Entry level (0-2 years): Base salary ranges in INR
- Mid level (2-5 years): Salary progression ranges
- Senior level (5-10 years): Advanced role compensation
- Leadership level (10+ years): Leadership/specialist premium

Include:
- Base salary ranges (median, 25th percentile, 75th percentile)
- Variable compensation (bonuses, stock options, incentives)
- Benefits and perks value estimation
- Contract/freelance rate equivalents

2. GEOGRAPHIC SALARY VARIATIONS:
Analyze compensation differences across:
- Tier 1 cities (Mumbai, Bangalore, Delhi, Chennai, Hyderabad, Pune)
- Tier 2 cities and regional markets
- Remote work compensation (India-based vs global remote)
- Cost of living adjustments and real purchasing power

3. CAREER GROWTH TRAJECTORIES:
For each domain, map:
- Typical career progression paths with salary milestones
- Time to reach different compensation levels
- Skills that accelerate salary growth
- Alternative high-paying career tracks within the domain
- Entrepreneurship and consulting income potential

4. TOTAL COMPENSATION ANALYSIS:
Beyond base salary, analyze:
- Health insurance and medical benefits value
- Learning and development allowances
- Work-life balance and flexibility value
- Stock options and equity participation
- Retirement and provident fund contributions
- Other perks (travel, accommodation, meals)

5. MARKET POSITIONING:
Compare domains on:
- Compensation competitiveness vs market average
- Growth potential and ceiling effects
- Risk vs reward profiles
- Industry stability and job security
- International opportunity and compensation

CRITICAL OUTPUT REQUIREMENTS:
- Generate ONLY valid JSON without any comments or explanations
- Do NOT use JavaScript-style comments (//) in the JSON
- Do NOT include placeholder text like "..." in the actual JSON structure
- All data must be complete and properly formatted
- If you need to indicate incomplete data, use proper JSON values like "data_pending" or empty arrays

Focus on actionable insights for college students understanding earning potential and making informed career investment decisions.

{format_instructions}

Return only valid JSON without any markdown formatting, comments, or explanations.""",
        )

    def analyze_compensation(
        self,
        specific_domains: List[str],
        intermediate_domains: List[str],
        broad_categories: List[str],
        student_context: str = "Final year college student",
    ) -> Dict[str, Any]:
        """Analyze compensation across the domain hierarchy"""

        prompt_input = {
            "specific_domains": ", ".join(specific_domains),
            "intermediate_domains": ", ".join(intermediate_domains),
            "broad_categories": ", ".join(broad_categories),
            "student_level": student_context,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add computational salary analysis
        result["salary_analytics"] = self._calculate_salary_metrics(result)

        # Add ROI analysis for career paths
        result["career_roi_analysis"] = self._calculate_career_roi(result)

        return result

    def _calculate_salary_metrics(self, salary_result: Dict) -> Dict[str, Any]:
        """Calculate quantitative salary metrics for comparison"""
        metrics = {
            "domain_ranking": {},
            "growth_potential": {},
            "geographic_premium": {},
        }

        domain_salaries = salary_result.get("domain_salary_ranges", {})

        # Rank domains by entry-level compensation
        entry_rankings = {}
        for domain, salary_info in domain_salaries.items():
            if (
                isinstance(salary_info, dict)
                and "Entry Level (0-2 years)" in salary_info
            ):
                entry_info = salary_info["Entry Level (0-2 years)"]
                if isinstance(entry_info, dict) and "median" in str(entry_info).lower():
                    # Extract approximate median value (simplified)
                    entry_rankings[domain] = 5.0  # Placeholder scoring system

        metrics["domain_ranking"] = dict(
            sorted(entry_rankings.items(), key=lambda x: x[1], reverse=True)
        )

        return metrics

    def _calculate_career_roi(self, salary_result: Dict) -> Dict[str, Any]:
        """Calculate return on investment for different career paths"""
        roi_analysis = {
            "investment_factors": {
                "education_time": "4-6 years typical degree completion",
                "skill_development": "1-3 years additional specialization",
                "networking_investment": "Ongoing relationship building",
            },
            "return_factors": {
                "salary_progression": "Compensation growth over 5-10 years",
                "job_security": "Market demand stability",
                "satisfaction_index": "Work-life balance and fulfillment",
            },
            "break_even_analysis": "Time to recover educational and opportunity costs",
        }

        return roi_analysis

    def _clean_json_comments(self, content: str) -> str:
        """Remove JavaScript-style comments from JSON content"""
        # Remove single-line comments
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

        # Remove multi-line comments
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

        # Remove trailing commas before closing brackets/braces
        content = re.sub(r",(\s*[}\]])", r"\1", content)

        # Clean up excessive whitespace
        content = re.sub(r"\n\s*\n", "\n", content)

        return content.strip()

    def _parse_llm_response(self, response) -> Dict[str, Any]:
        """Parse LLM response with error handling and comment removal"""
        content = response.content.strip()

        # Remove markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # Clean JavaScript-style comments and formatting issues
        content = self._clean_json_comments(content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as json_error:
            try:
                # Try with output parser as fallback
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
                # Log the cleaned content for debugging
                print(f"Cleaned content that failed to parse: {repr(content[:500])}")
                raise ValueError(
                    f"Failed to parse salary benchmarking response. "
                    f"JSON error: {json_error}. "
                    f"Parser error: {parser_error}. "
                    f"Content preview: {content[:200]}..."
                )
