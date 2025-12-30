from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from agentic_layer.base_agent import BaseAgent
from config.agent_config import AgentType, SkillDevelopmentOutput
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class SkillDevelopmentStrategistAgent(BaseAgent):
    """
    Skill Development Strategist Agent for College Student Fleet

    Role: Learning and Development Specialist
    Purpose: Creates comprehensive upskilling roadmap based on career goals and current skill gaps

    Key Features:
    - Prioritized skill development pathway
    - Learning resource recommendations (courses, certifications, projects)
    - Timeline estimation for skill acquisition
    - Portfolio project suggestions
    - Skill validation and demonstration strategies
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="skill_development_strategist",
            agent_name="Skill Development Strategist Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config,
        )

    def _define_required_inputs(self) -> List[str]:
        """Define required inputs for skill development strategy"""
        return []  # No direct user data required - gets data from previous agents

    def _define_optional_inputs(self) -> List[str]:
        """Define optional inputs that enhance skill development planning"""
        return [
            "resume_data",  # To understand current experience
            "github_profile",  # To assess technical project experience
            "academic_status",  # To understand academic background
            "career_preferences",  # Specific career goals or preferences
            "learning_preferences",  # Preferred learning methods/timeline
            "budget_constraints",  # Available budget for learning resources
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of skill development strategy output"""
        return {
            "skill_gap_analysis": "Detailed analysis of current vs required skills",
            "development_roadmap": "Structured learning plan with timelines",
            "immediate_actions": "Quick wins and immediate steps",
            "long_term_strategy": "Strategic skill building approach",
            "portfolio_projects": "Hands-on projects for skill demonstration",
            "certification_recommendations": "Relevant certifications to pursue",
            "networking_opportunities": "Skill-focused networking suggestions",
        }

    def _initialize_agent(self):
        """Initialize skill development strategist specific components"""
        self.output_parser = JsonOutputParser(pydantic_object=SkillDevelopmentOutput)

        # Main skill development analysis prompt
        self.strategy_prompt = PromptTemplate(
            input_variables=[
                "profile_summary",
                "current_skills",
                "market_demands",
                "career_goals",
                "learning_preferences",
                "timeline_constraints",
                "analysis_date",
                "format_instructions",
            ],
            template=self._create_system_prompt(
                "Learning and Development Specialist",
                """
Context Information:
- Analysis Date: {analysis_date}
- Profile Summary: {profile_summary}
- Current Skills: {current_skills}
- Market Demands: {market_demands}
- Career Goals: {career_goals}
- Learning Preferences: {learning_preferences}
- Timeline Constraints: {timeline_constraints}

Your expertise includes:
- Skill gap analysis and prioritization methodologies
- Learning pathway design with optimal sequencing
- Resource curation across multiple learning platforms
- Project-based learning and portfolio development
- Certification strategy and ROI analysis
- Skill validation and demonstration techniques
- Timeline optimization for efficient skill acquisition

Analysis Framework:
1. Current State Assessment: Analyze existing skill profile comprehensively
2. Market Alignment: Compare current skills with market requirements
3. Gap Prioritization: Identify and prioritize skill gaps by impact and urgency
4. Learning Path Design: Create structured, sequential learning roadmap
5. Resource Mapping: Recommend specific courses, tutorials, and practice platforms
6. Project Integration: Design hands-on projects for skill application
7. Validation Strategy: Plan for skill demonstration and certification
8. Timeline Optimization: Balance speed with depth for effective learning

Focus Areas for College Students:
- Building job-ready skills with practical application
- Balancing academic workload with skill development
- Cost-effective learning resource selection
- Portfolio projects that demonstrate competency
- Industry-relevant certifications vs generic ones
- Networking opportunities through learning communities
- Preparing for technical interviews and assessments

Learning Methodology Considerations:
- Theory vs hands-on practice balance
- Individual learning vs collaborative opportunities
- Formal courses vs self-directed learning
- Short-term bootcamps vs long-term skill building
- Free resources vs paid premium content

{format_instructions}
                """,
            )
            + "\n\nProvide comprehensive skill development strategy in the specified JSON format.",
        )

        self.logger.info("Skill Development Strategist Agent initialized")

    @traceable(
        name="skill_development_strategy",
        tags=["skill_development", "comprehensive", "llm_chain"],
    )
    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core skill development strategy logic"""
        self._add_processing_note("Starting skill development strategy analysis")

        # Extract required inputs
        profile_analysis = self._extract_profile_analysis(validated_input)
        market_intelligence = self._extract_market_intelligence(validated_input)

        # Extract optional context
        current_skills = self._extract_current_skills(validated_input, profile_analysis)
        career_goals = self._extract_career_goals(validated_input, profile_analysis)
        learning_preferences = self._extract_learning_preferences(validated_input)
        timeline_constraints = self._extract_timeline_constraints(validated_input)

        self.logger.info(
            f"Analyzing skill development strategy for {len(current_skills)} current skills"
        )

        # Prepare prompt inputs
        prompt_inputs = {
            "profile_summary": self._create_profile_summary(profile_analysis),
            "current_skills": self._format_current_skills(current_skills),
            "market_demands": self._format_market_demands(market_intelligence),
            "career_goals": career_goals,
            "learning_preferences": learning_preferences,
            "timeline_constraints": timeline_constraints,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.strategy_prompt.format(**prompt_inputs)
        response = self.llm_model.invoke(formatted_prompt)

        output_dict = self._parse_llm_response(response)

        output_dict["strategy_metadata"] = {
            "analysis_date": prompt_inputs["analysis_date"],
            "current_skills_analyzed": len(current_skills),
            "market_trends_considered": len(
                market_intelligence.get("skill_demand", {})
            ),
            "learning_timeline": timeline_constraints,
            "confidence_factors": self._assess_strategy_confidence(validated_input),
        }

        self._add_processing_note(
            "Skill development strategy analysis completed successfully"
        )
        return output_dict

    def _extract_profile_analysis(
        self, validated_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract profile analysis from previous agent output"""
        previous_outputs = validated_input.get("previous_outputs", {})
        profile_output = previous_outputs.get("profile_analysis")

        if profile_output and hasattr(profile_output, "output_data"):
            return profile_output.output_data

        # Fallback to required data if previous output structure is different
        required_data = validated_input.get("required_data", {})
        return required_data.get("profile_analysis_output", {})

    def _extract_market_intelligence(
        self, validated_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract market intelligence from previous agent output"""
        previous_outputs = validated_input.get("previous_outputs", {})
        market_output = previous_outputs.get("market_intelligence")

        if market_output and hasattr(market_output, "output_data"):
            return market_output.output_data

        # Fallback to required data
        required_data = validated_input.get("required_data", {})
        return required_data.get("market_intelligence_output", {})

    @traceable(
        name="skill_gap_analysis",
        tags=["skill_development", "gap_analysis", "llm_chain"],
    )
    def _extract_current_skills(
        self, validated_input: Dict[str, Any], profile_analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """Extract current skills from profile analysis and other sources"""
        skills = {}

        # From profile analysis
        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            # Handle technical_skills - could be dict or list
            if "technical_skills" in comp_analysis:
                tech_skills = comp_analysis["technical_skills"]
                if isinstance(tech_skills, dict):
                    skills.update(tech_skills)
                elif isinstance(tech_skills, list):
                    # Convert list to dict with default proficiency
                    for skill in tech_skills:
                        skills[skill] = "Intermediate"

            # Handle soft_skills - could be dict or list
            if "soft_skills" in comp_analysis:
                soft_skills = comp_analysis["soft_skills"]
                if isinstance(soft_skills, dict):
                    skills.update(soft_skills)
                elif isinstance(soft_skills, list):
                    # Convert list to dict with default proficiency
                    for skill in soft_skills:
                        skills[skill] = "Intermediate"

        # From individual analyses in profile
        individual_analyses = profile_analysis.get("individual_analyses", {})

        # From resume analysis
        resume_analysis = individual_analyses.get("resume", {})
        if "technical_skills" in resume_analysis:
            tech_skills = resume_analysis["technical_skills"]
            if isinstance(tech_skills, dict):
                skills.update(tech_skills)
            elif isinstance(tech_skills, list):
                # Convert list to dict with default proficiency
                for skill in tech_skills:
                    skills[skill] = "Intermediate"

        # From GitHub analysis
        github_analysis = individual_analyses.get("github", {})
        if "programming_languages" in github_analysis:
            prog_langs = github_analysis["programming_languages"]
            if isinstance(prog_langs, list):
                for lang in prog_langs:
                    skills[lang] = "Intermediate"  # Default assumption
            elif isinstance(prog_langs, dict):
                skills.update(prog_langs)

        return skills

    def _extract_career_goals(
        self, validated_input: Dict[str, Any], profile_analysis: Dict[str, Any]
    ) -> str:
        """Extract career goals from available data"""
        # Check if explicitly provided
        career_prefs = validated_input.get("optional_data", {}).get(
            "career_preferences"
        )
        if career_prefs:
            return str(career_prefs)

        # Infer from profile analysis
        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]
            if "career_direction" in comp_analysis:
                return comp_analysis["career_direction"]
            if "recommended_roles" in comp_analysis:
                roles = comp_analysis["recommended_roles"]
                if isinstance(roles, list) and roles:
                    return f"Target roles: {', '.join(roles[:3])}"

        return "General career development and skill enhancement for better job opportunities"

    def _extract_learning_preferences(self, validated_input: Dict[str, Any]) -> str:
        """Extract learning preferences"""
        learning_prefs = validated_input.get("optional_data", {}).get(
            "learning_preferences"
        )
        if learning_prefs:
            return str(learning_prefs)

        # Default preferences for college students
        return "Flexible online learning, hands-on projects, cost-effective resources, peer collaboration"

    def _extract_timeline_constraints(self, validated_input: Dict[str, Any]) -> str:
        """Extract timeline constraints"""
        # Check academic status for timeline context
        academic_status = validated_input.get("optional_data", {}).get(
            "academic_status"
        )
        if academic_status:
            current_year = academic_status.get("current_year", "Unknown")
            if current_year in [3, 4]:
                return f"Final year student - 6-12 months for intensive skill building before job search"
            elif current_year in [1, 2]:
                return f"Early college years - 2-3 years for comprehensive skill development"

        return "Flexible timeline with focus on steady progress and job readiness"

    def _create_profile_summary(self, profile_analysis: Dict[str, Any]) -> str:
        """Create a concise profile summary for context"""
        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            summary_parts = []

            if "profile_strengths" in comp_analysis:
                strengths = comp_analysis["profile_strengths"]
                if isinstance(strengths, list):
                    summary_parts.append(f"Key Strengths: {', '.join(strengths[:3])}")

            if "experience_level" in comp_analysis:
                summary_parts.append(
                    f"Experience Level: {comp_analysis['experience_level']}"
                )

            if "primary_domain" in comp_analysis:
                summary_parts.append(
                    f"Primary Domain: {comp_analysis['primary_domain']}"
                )

            return (
                "; ".join(summary_parts)
                if summary_parts
                else "College student seeking skill development"
            )

        return "Profile analysis available with comprehensive recommendations"

    def _format_current_skills(self, skills: Dict[str, str]) -> str:
        """Format current skills for prompt"""
        if not skills:
            return "Limited technical skills identified, focus on foundational skill building"

        skill_lines = []
        for skill, level in skills.items():
            skill_lines.append(f"- {skill}: {level}")

        return "\n".join(skill_lines)

    @traceable(
        name="market_demand_analysis",
        tags=["skill_development", "market_alignment", "llm_chain"],
    )
    def _format_market_demands(self, market_intelligence: Dict[str, Any]) -> str:
        """Format market demands from market intelligence"""
        if not market_intelligence:
            return "General market trends favor technical skills, communication, and adaptability"

        demand_parts = []

        if "skill_demand" in market_intelligence:
            skill_demand = market_intelligence["skill_demand"]
            if isinstance(skill_demand, dict):
                high_demand = [
                    skill
                    for skill, demand in skill_demand.items()
                    if "high" in str(demand).lower()
                ]
                if high_demand:
                    demand_parts.append(
                        f"High Demand Skills: {', '.join(high_demand[:5])}"
                    )

        if "industry_trends" in market_intelligence:
            trends = market_intelligence["industry_trends"]
            if isinstance(trends, dict) and "emerging_areas" in trends:
                emerging = trends["emerging_areas"]
                if isinstance(emerging, list):
                    demand_parts.append(f"Emerging Areas: {', '.join(emerging[:3])}")

        return (
            "; ".join(demand_parts)
            if demand_parts
            else "Focus on modern technical skills and soft skills"
        )

    def _assess_strategy_confidence(
        self, validated_input: Dict[str, Any]
    ) -> Dict[str, float]:
        """Assess confidence in different aspects of strategy"""
        confidence_factors = {
            "skill_gap_analysis": 0.8,  # Based on solid profile and market data
            "resource_recommendations": 0.9,  # Strong knowledge of learning resources
            "timeline_estimates": 0.7,  # Variable based on individual learning pace
            "project_suggestions": 0.85,  # Good understanding of skill-building projects
            "certification_strategy": 0.8,  # Well-defined certification landscape
        }

        # Adjust based on data quality
        if validated_input.get("previous_outputs", {}).get("profile_analysis"):
            for key in confidence_factors:
                confidence_factors[key] += 0.05

        if validated_input.get("previous_outputs", {}).get("market_intelligence"):
            for key in confidence_factors:
                confidence_factors[key] += 0.05

        return confidence_factors

    def _calculate_confidence_score(
        self, validated_data: Dict[str, Any], output_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for skill development strategy"""
        base_confidence = 0.7  # Good confidence for strategic planning

        # Boost confidence with quality inputs
        if validated_data.get("previous_outputs", {}).get("profile_analysis"):
            base_confidence += 0.1

        if validated_data.get("previous_outputs", {}).get("market_intelligence"):
            base_confidence += 0.1

        # Check strategy completeness
        expected_components = [
            "skill_gap_analysis",
            "development_roadmap",
            "immediate_actions",
        ]
        completed_components = sum(
            1
            for comp in expected_components
            if comp in output_data and output_data[comp]
        )
        completeness_boost = (completed_components / len(expected_components)) * 0.1

        return min(0.95, base_confidence + completeness_boost)

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
