from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json


class FinancialAidPlanningOutput(BaseModel):
    """Output structure for financial aid planning"""

    comprehensive_cost_analysis: Dict[str, Any] = Field(
        description="Detailed cost breakdown and projections"
    )
    funding_strategy: Dict[str, List[str]] = Field(
        description="Multi-source funding approach"
    )
    loan_optimization: Dict[str, Any] = Field(
        description="Education loan strategy and optimization"
    )
    roi_analysis: Dict[str, Any] = Field(
        description="Return on investment analysis for education"
    )
    preparation_checklist: List[str] = Field(description="Financial preparation steps")


class FinancialAidPlanningSubAgent:
    """Sub-agent for comprehensive financial aid planning and optimization"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(
            pydantic_object=FinancialAidPlanningOutput
        )

        # Financial benchmarks for Indian higher education
        self.cost_benchmarks = {
            "Engineering": {
                "IIT": {"tuition": 200000, "hostel": 50000, "misc": 30000},
                "NIT": {"tuition": 150000, "hostel": 40000, "misc": 25000},
                "Private_Tier1": {"tuition": 400000, "hostel": 80000, "misc": 50000},
                "Private_Tier2": {"tuition": 200000, "hostel": 60000, "misc": 40000},
            },
            "Medicine": {
                "Government": {"tuition": 100000, "hostel": 50000, "misc": 30000},
                "Private": {"tuition": 1500000, "hostel": 100000, "misc": 80000},
                "Deemed": {"tuition": 800000, "hostel": 80000, "misc": 60000},
            },
            "Business": {
                "IIM": {"tuition": 2300000, "hostel": 200000, "misc": 100000},
                "Government": {"tuition": 100000, "hostel": 50000, "misc": 30000},
                "Private_Premium": {
                    "tuition": 1800000,
                    "hostel": 150000,
                    "misc": 80000,
                },
            },
            "Liberal_Arts": {
                "Premium_Private": {"tuition": 500000, "hostel": 100000, "misc": 50000},
                "Government": {"tuition": 50000, "hostel": 40000, "misc": 20000},
                "Regular_Private": {"tuition": 200000, "hostel": 60000, "misc": 30000},
            },
        }

        # Education loan parameters
        self.loan_parameters = {
            "collateral_free_limit": 750000,
            "interest_rates": {
                "government_bank": 8.5,
                "private_bank": 10.5,
                "nbfc": 12.0,
            },
            "moratorium_period": "course_duration + 1 year",
            "repayment_period": "5-15 years",
            "processing_fees": "0.5-2% of loan amount",
        }

        self.prompt = PromptTemplate(
            input_variables=[
                "student_profile",
                "college_costs",
                "family_income",
                "scholarship_potential",
                "loan_preferences",
            ],
            template="""You are a Financial Aid Planning Specialist helping Indian families optimize education funding strategies.

STUDENT PROFILE:
{student_profile}

COLLEGE COST ANALYSIS:
{college_costs}

FAMILY INCOME CONTEXT:
{family_income}

SCHOLARSHIP FUNDING POTENTIAL:
{scholarship_potential}

EDUCATION LOAN PREFERENCES:
{loan_preferences}

Create comprehensive financial aid planning:

1. COMPREHENSIVE COST ANALYSIS:
   - Year-wise cost breakdown (tuition, living, miscellaneous)
   - Inflation adjustments for multi-year programs
   - Hidden costs and unexpected expenses
   - Regional cost variations
   - Total education investment calculation

2. MULTI-SOURCE FUNDING STRATEGY:
   - Family contribution optimization
   - Scholarship stacking strategy
   - Education loan utilization
   - Part-time work opportunities
   - Emergency funding reserves

3. EDUCATION LOAN OPTIMIZATION:
   - Loan amount vs family contribution balance
   - Bank comparison and selection criteria
   - Interest rate optimization strategies
   - Collateral vs non-collateral options
   - Repayment planning and strategies

4. ROI ANALYSIS:
   - Expected career earnings vs education cost
   - Break-even analysis timelines
   - Alternative pathway cost-benefit comparison
   - Long-term financial impact assessment
   - Risk mitigation strategies

5. IMPLEMENTATION ROADMAP:
   - Financial documentation preparation
   - Application timeline coordination
   - Contingency planning for funding gaps
   - Regular review and adjustment mechanisms
   - Family financial counseling recommendations

Consider Indian banking regulations, tax implications, and family financial dynamics.

{format_instructions}""",
        )

    def create_financial_plan(
        self,
        student_profile: str,
        college_costs: Dict[str, float],
        family_income: str,
        scholarship_potential: str,
        loan_preferences: str,
    ) -> Dict[str, Any]:
        """Generate comprehensive financial aid planning"""

        prompt_input = {
            "student_profile": student_profile,
            "college_costs": json.dumps(college_costs, indent=2),
            "family_income": family_income,
            "scholarship_potential": scholarship_potential,
            "loan_preferences": loan_preferences,
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add computational financial analysis
        result["financial_analytics"] = self._calculate_financial_metrics(
            college_costs, family_income, scholarship_potential
        )

        return result

    def _calculate_financial_metrics(
        self,
        college_costs: Dict[str, float],
        family_income: str,
        scholarship_potential: str,
    ) -> Dict[str, Any]:
        """Calculate financial metrics and ratios"""

        # Extract cost information
        total_annual_cost = college_costs.get("total_annual", 300000)

        # Estimate family income bracket
        income_brackets = {
            "Lower Income": 400000,
            "Middle Income": 800000,
            "Higher Income": 1500000,
        }
        estimated_income = income_brackets.get(family_income, 800000)

        # Calculate financial ratios
        cost_to_income_ratio = (
            total_annual_cost * 4
        ) / estimated_income  # 4-year program

        # Extract scholarship potential
        try:
            scholarship_amount = (
                float(scholarship_potential.replace("₹", "").replace(",", ""))
                if "₹" in str(scholarship_potential)
                else 50000
            )
        except:
            scholarship_amount = 50000

        net_annual_cost = max(0, total_annual_cost - scholarship_amount)
        loan_requirement = max(
            0, (net_annual_cost * 4) - (estimated_income * 0.2)
        )  # Assuming 20% family contribution

        return {
            "financial_ratios": {
                "cost_to_income_ratio": round(cost_to_income_ratio, 2),
                "affordability_index": (
                    "High"
                    if cost_to_income_ratio < 2
                    else "Medium" if cost_to_income_ratio < 4 else "Low"
                ),
            },
            "funding_breakdown": {
                "total_program_cost": total_annual_cost * 4,
                "scholarship_savings": scholarship_amount * 4,
                "net_cost": net_annual_cost * 4,
                "estimated_loan_requirement": max(0, loan_requirement),
            },
            "repayment_projections": {
                "estimated_monthly_emi": (
                    round(loan_requirement * 0.012, 0) if loan_requirement > 0 else 0
                ),  # Rough EMI calculation
                "repayment_period": (
                    "10-15 years" if loan_requirement > 500000 else "5-10 years"
                ),
            },
        }

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
