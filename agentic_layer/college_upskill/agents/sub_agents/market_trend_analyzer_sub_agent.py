from typing import Dict, List, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json
from datetime import datetime


class MarketTrendOutput(BaseModel):
    """Output structure for market trend analysis"""

    domain_specific_trends: Dict[str, Dict[str, Any]] = Field(
        description="Trends for each specific domain"
    )
    cross_domain_opportunities: List[Dict[str, Any]] = Field(
        description="Opportunities spanning multiple domains"
    )
    emerging_intersections: List[Dict[str, Any]] = Field(
        description="New field intersections and hybrid roles"
    )
    market_timing_insights: Dict[str, Any] = Field(
        description="Timing analysis for market entry"
    )
    skill_evolution_patterns: Dict[str, List[str]] = Field(
        description="How skills are evolving in each domain"
    )


class MarketTrendAnalyzerSubAgent:
    """Sub-agent for analyzing market trends across the domain hierarchy"""

    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.output_parser = JsonOutputParser(pydantic_object=MarketTrendOutput)

        # Market trend knowledge base
        self.trend_indicators = {
            "growth_signals": [
                "job posting increases",
                "startup funding",
                "technology adoption",
                "regulatory changes",
            ],
            "decline_signals": [
                "automation threats",
                "outsourcing trends",
                "market saturation",
                "skill obsolescence",
            ],
            "stability_signals": [
                "consistent demand",
                "established workflows",
                "mature industry",
                "steady growth",
            ],
        }

        self.prompt = PromptTemplate(
            input_variables=[
                "specific_domains",
                "intermediate_domains",
                "broad_categories",
                "domain_hierarchy",
                "analysis_date",
            ],
            template="""You are a Market Trend Analyst specializing in career opportunity forecasting across domain hierarchies.

DOMAIN ANALYSIS TARGETS:
Specific Domains: {specific_domains}
Intermediate Domains: {intermediate_domains}  
Broad Market Categories: {broad_categories}
Domain Relationships: {domain_hierarchy}
Analysis Date: {analysis_date}

TREND ANALYSIS FRAMEWORK:

1. DOMAIN-SPECIFIC TREND ANALYSIS:
For each specific domain, analyze:
- Current market demand and growth trajectory
- Key drivers of change (technology, regulation, social trends)
- Skill demand evolution (what's growing, what's declining)
- Entry-level vs experienced role availability
- Geographic variation in opportunities
- Compensation trends and projections

2. CROSS-DOMAIN OPPORTUNITY IDENTIFICATION:
- Identify roles that span multiple specific domains
- Analyze intermediate domains as career bridges
- Find opportunities in domain intersections
- Evaluate transferable skill advantages

3. EMERGING INTERSECTION ANALYSIS:
- New hybrid roles combining domains (e.g., Health Data Science, EdTech Psychology)
- Technology-driven field convergence
- Interdisciplinary career opportunities
- Innovation-driven new role categories

4. MARKET TIMING INSIGHTS:
- Early vs mature market entry timing for each domain
- Skill development timing for maximum market advantage
- Geographic market timing differences
- Industry cycle considerations

5. SKILL EVOLUTION PATTERNS:
- Core skills becoming more/less valuable in each domain
- New skills emerging in traditional domains
- Technology impact on skill requirements
- Soft skill demand changes

Focus on actionable insights for a college student planning their career development across these interconnected domains.

{format_instructions}

Provide comprehensive multi-level trend analysis connecting specific domains to broader market realities.""",
        )

    def analyze_trends(
        self,
        specific_domains: List[str],
        intermediate_domains: List[str],
        broad_categories: List[str],
        domain_hierarchy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze market trends across the domain hierarchy"""

        prompt_input = {
            "specific_domains": ", ".join(specific_domains),
            "intermediate_domains": ", ".join(intermediate_domains),
            "broad_categories": ", ".join(broad_categories),
            "domain_hierarchy": json.dumps(domain_hierarchy, indent=2),
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.prompt.format(**prompt_input)
        llm_response = self.llm_model.invoke(formatted_prompt)
        result = self._parse_llm_response(llm_response)

        # Add computational trend scoring
        result["trend_scoring"] = self._calculate_trend_scores(result)

        # Add opportunity prioritization
        result["opportunity_prioritization"] = self._prioritize_opportunities(result)

        return result

    def _calculate_trend_scores(self, trend_result: Dict) -> Dict[str, float]:
        """Calculate quantitative trend scores for prioritization"""
        scores = {}

        domain_trends = trend_result.get("domain_specific_trends", {})
        for domain, trends in domain_trends.items():
            if isinstance(trends, dict):
                # Simple scoring based on growth indicators
                growth_score = 0.5  # Base score

                trend_text = str(trends).lower()
                for signal in self.trend_indicators["growth_signals"]:
                    if signal in trend_text:
                        growth_score += 0.1

                for signal in self.trend_indicators["decline_signals"]:
                    if signal in trend_text:
                        growth_score -= 0.15

                scores[domain] = max(0.1, min(1.0, growth_score))

        return scores

    def _prioritize_opportunities(self, trend_result: Dict) -> List[Dict[str, Any]]:
        """Prioritize opportunities based on trend analysis"""
        opportunities = []

        # Extract cross-domain opportunities
        cross_domain = trend_result.get("cross_domain_opportunities", [])
        for opp in cross_domain:
            if isinstance(opp, dict):
                opportunities.append(
                    {
                        "opportunity": opp,
                        "type": "cross_domain",
                        "priority_score": 0.8,  # High priority for cross-domain
                    }
                )

        # Extract emerging intersections
        emerging = trend_result.get("emerging_intersections", [])
        for opp in emerging:
            if isinstance(opp, dict):
                opportunities.append(
                    {
                        "opportunity": opp,
                        "type": "emerging",
                        "priority_score": 0.9,  # Highest priority for emerging
                    }
                )

        # Sort by priority score
        opportunities.sort(key=lambda x: x["priority_score"], reverse=True)

        return opportunities[:10]  # Top 10 opportunities

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
                    f"Failed to parse market trend analysis response. "
                    f"JSON error: {json_error}. "
                    f"Parser error: {parser_error}."
                )
