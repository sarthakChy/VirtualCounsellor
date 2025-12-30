from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from agentic_layer.base_agent import BaseAgent
from config.agent_config import AgentType, OpportunityMatchingOutput
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class OpportunityMatcherAgent(BaseAgent):
    """
    Opportunity Matcher Agent for College Student Fleet

    Role: Career Placement Specialist and Opportunity Curator
    Purpose: Matches student profile with specific job opportunities, internships, and programs

    Key Features:
    - Job role compatibility scoring
    - Company culture fit assessment
    - Application timeline and strategy optimization
    - Alternative pathway recommendations
    - Success probability estimation for different opportunities
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="opportunity_matcher",
            agent_name="Opportunity Matcher Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config,
        )

    def _define_required_inputs(self) -> List[str]:
        """Define required inputs for skill development strategy"""
        return []  # No direct user data required - gets data from previous agents

    def _define_optional_inputs(self) -> List[str]:
        """Define optional inputs that enhance opportunity matching"""
        return [
            "market_intelligence_output",  # Market trends for better matching
            "skill_development_output",  # Current skill development status
            "resume_data",  # Direct resume access for detailed matching
            "linkedin_profile",  # Professional network context
            "geographic_preferences",  # Location preferences for opportunities
            "company_preferences",  # Company size, culture, industry preferences
            "salary_expectations",  # Compensation expectations
            "work_mode_preferences",  # Remote, hybrid, onsite preferences
            "timeline_urgency",  # How quickly opportunities are needed
            "industry_focus",  # Specific industry targeting
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of opportunity matching output"""
        return {
            "matched_opportunities": "Curated list of suitable opportunities with compatibility scores",
            "compatibility_analysis": "Detailed analysis of profile-opportunity alignment",
            "application_strategy": "Customized approach for each opportunity type",
            "success_probability": "Estimated success rates and key success factors",
            "preparation_requirements": "Skills and preparations needed for target opportunities",
            "alternative_pathways": "Alternative routes and backup strategies",
            "networking_strategy": "Targeted networking for opportunity access",
        }

    def _initialize_agent(self):
        """Initialize opportunity matcher specific components"""
        self.output_parser = JsonOutputParser(pydantic_object=OpportunityMatchingOutput)

        # Main opportunity matching prompt
        self.matching_prompt = PromptTemplate(
            input_variables=[
                "profile_summary",
                "career_goals",
                "current_skills",
                "market_context",
                "preferences",
                "timeline_context",
                "geographic_focus",
                "analysis_date",
                "format_instructions",
            ],
            template=self._create_system_prompt(
                "Career Placement Specialist and Opportunity Curator",
                """
Context Information:
- Analysis Date: {analysis_date}
- Profile Summary: {profile_summary}
- Career Goals: {career_goals}
- Current Skills: {current_skills}
- Market Context: {market_context}
- Preferences: {preferences}
- Timeline Context: {timeline_context}
- Geographic Focus: {geographic_focus}

Your expertise includes:
- Job market analysis and opportunity identification
- Profile-opportunity compatibility assessment
- Application strategy optimization and customization
- Company culture and role fit evaluation
- Success probability modeling for different opportunity types
- Alternative pathway identification and risk assessment
- Networking strategy for opportunity access and referrals
- Interview preparation and application timing optimization

Opportunity Matching Framework:
1. Opportunity Identification: Source relevant opportunities across multiple channels
2. Compatibility Scoring: Assess alignment between profile and opportunity requirements
3. Fit Analysis: Evaluate cultural, role, and growth fit factors
4. Success Modeling: Calculate probability of success for each opportunity
5. Strategy Customization: Create tailored application approach for each opportunity
6. Timeline Optimization: Plan application sequence and timing
7. Alternative Planning: Identify backup opportunities and pivot strategies
8. Network Activation: Leverage connections for opportunity access

Focus Areas for College Students:
- Entry-level positions and graduate programs
- Internship opportunities for skill building and network development
- Startup vs established company trade-offs and considerations
- Remote work opportunities for geographic flexibility
- Growth potential and learning opportunities in each role
- Company culture fit for early career development
- Salary negotiation positioning for entry-level candidates
- Building long-term career foundation through strategic opportunity selection

Opportunity Categories:
- Full-time entry-level positions
- Internships and co-op programs
- Graduate trainee programs
- Freelance and project-based opportunities
- Startup opportunities with equity potential
- Research and academic opportunities
- International opportunities and exchanges

Success Factors Assessment:
- Technical skill alignment and gap analysis
- Soft skill requirements and cultural fit
- Network connections and referral potential
- Application timing and market conditions
- Competition level and differentiation strategies
- Interview preparation requirements and success factors

{format_instructions}
                """,
            )
            + "\n\nProvide comprehensive opportunity matching analysis in the specified JSON format.",
        )

        self.logger.info("Opportunity Matcher Agent initialized")

    @traceable(
        name="opportunity_matching_analysis",
        tags=["opportunity_matching", "comprehensive", "llm_chain"],
    )
    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core opportunity matching logic"""
        self._add_processing_note("Starting opportunity matching analysis")

        # Extract required inputs from previous agents
        profile_analysis = self._extract_agent_output(
            validated_input, "profile_analysis"
        )
        career_optimization = self._extract_agent_output(
            validated_input, "career_optimization_planner"
        )

        # Extract optional context
        market_context = self._extract_market_context(validated_input)
        preferences = self._extract_preferences(validated_input)
        timeline_context = self._extract_timeline_context(validated_input)
        geographic_focus = self._extract_geographic_focus(validated_input)

        # Create comprehensive context
        profile_summary = self._create_profile_summary(profile_analysis)
        career_goals = self._extract_career_goals(career_optimization)
        current_skills = self._extract_current_skills_summary(profile_analysis)

        self.logger.info("Matching opportunities to student profile and career goals")

        # Prepare prompt inputs
        prompt_inputs = {
            "profile_summary": profile_summary,
            "career_goals": career_goals,
            "current_skills": current_skills,
            "market_context": market_context,
            "preferences": preferences,
            "timeline_context": timeline_context,
            "geographic_focus": geographic_focus,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.matching_prompt.format(**prompt_inputs)
        response = self.llm_model.invoke(formatted_prompt)
        output_dict = self._parse_llm_response(response)

        output_dict["matching_metadata"] = {
            "analysis_date": prompt_inputs["analysis_date"],
            "opportunities_analyzed": len(output_dict.get("matched_opportunities", [])),
            "matching_criteria": self._get_matching_criteria(),
            "success_factors": self._get_key_success_factors(output_dict),
            "personalization_level": self._assess_personalization_level(
                validated_input
            ),
        }

        # Add implementation guidance
        output_dict["implementation_guidance"] = self._create_implementation_guidance(
            output_dict
        )

        self._add_processing_note(
            "Opportunity matching analysis completed successfully"
        )
        return output_dict

    @traceable(
        name="profile_opportunity_alignment",
        tags=["opportunity_matching", "compatibility", "llm_chain"],
    )
    def _extract_agent_output(
        self, validated_input: Dict[str, Any], agent_id: str
    ) -> Dict[str, Any]:
        """Extract output from specific previous agent"""
        previous_outputs = validated_input.get("previous_outputs", {})
        agent_output = previous_outputs.get(agent_id)

        if agent_output and hasattr(agent_output, "output_data"):
            return agent_output.output_data

        # Fallback to required data
        required_data = validated_input.get("required_data", {})
        return required_data.get(f"{agent_id}_output", {})

    @traceable(
        name="opportunity_compatibility_scoring",
        tags=["opportunity_matching", "scoring", "llm_chain"],
    )
    def _create_profile_summary(self, profile_analysis: Dict[str, Any]) -> str:
        """Create comprehensive profile summary for opportunity matching"""
        summary_parts = []

        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            if "profile_positioning" in comp_analysis:
                summary_parts.append(
                    f"Positioning: {comp_analysis['profile_positioning']}"
                )

            if "experience_level" in comp_analysis:
                summary_parts.append(
                    f"Experience Level: {comp_analysis['experience_level']}"
                )

            if "competitive_advantages" in comp_analysis:
                advantages = comp_analysis["competitive_advantages"]
                if isinstance(advantages, list):
                    summary_parts.append(f"Key Advantages: {', '.join(advantages[:3])}")

            if "primary_domain" in comp_analysis:
                summary_parts.append(f"Domain: {comp_analysis['primary_domain']}")

        return (
            "; ".join(summary_parts)
            if summary_parts
            else "College student with developing professional profile"
        )

    def _extract_career_goals(self, career_optimization: Dict[str, Any]) -> str:
        """Extract career goals from career optimization output"""
        if not career_optimization:
            return "General career development and entry-level opportunities"

        goal_parts = []

        if "career_goals" in career_optimization:
            career_goals = career_optimization["career_goals"]
            if isinstance(career_goals, list):
                for goal in career_goals[:3]:  # Top 3 goals
                    if isinstance(goal, dict) and "goal_title" in goal:
                        goal_parts.append(goal["goal_title"])

        if "career_strategy" in career_optimization:
            strategy = career_optimization["career_strategy"]
            if isinstance(strategy, dict) and "short_term_strategy" in strategy:
                goal_parts.append(f"Strategy: {strategy['short_term_strategy']}")

        return (
            "; ".join(goal_parts)
            if goal_parts
            else "Seeking entry-level opportunities with growth potential"
        )

    def _extract_current_skills_summary(self, profile_analysis: Dict[str, Any]) -> str:
        """Extract current skills summary for matching"""
        if not profile_analysis:
            return "Foundational skills with learning potential"

        skills = []

        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            if "technical_skills" in comp_analysis:
                tech_skills = comp_analysis["technical_skills"]
                if isinstance(tech_skills, dict):
                    strong_skills = [
                        skill
                        for skill, level in tech_skills.items()
                        if level in ["Advanced", "Expert", "Strong"]
                    ]
                    skills.extend(strong_skills[:5])

            if "profile_strengths" in comp_analysis:
                strengths = comp_analysis["profile_strengths"]
                if isinstance(strengths, list):
                    skills.extend(strengths[:3])

        return (
            ", ".join(skills)
            if skills
            else "Developing technical and professional skills"
        )

    @traceable(
        name="market_context_integration",
        tags=["opportunity_matching", "market_analysis", "llm_chain"],
    )
    def _extract_market_context(self, validated_input: Dict[str, Any]) -> str:
        """Extract market intelligence context"""
        market_output = validated_input.get("previous_outputs", {}).get(
            "market_intelligence"
        )

        if market_output and hasattr(market_output, "output_data"):
            market_data = market_output.output_data

            context_parts = []

            if "industry_trends" in market_data:
                trends = market_data["industry_trends"]
                if isinstance(trends, dict) and "growth_areas" in trends:
                    growth_areas = trends["growth_areas"]
                    if isinstance(growth_areas, list):
                        context_parts.append(
                            f"Growing Areas: {', '.join(growth_areas[:3])}"
                        )

            if "job_market_outlook" in market_data:
                outlook = market_data["job_market_outlook"]
                if isinstance(outlook, dict) and "entry_level_opportunities" in outlook:
                    context_parts.append(
                        f"Entry-level Outlook: {outlook['entry_level_opportunities']}"
                    )

            return (
                "; ".join(context_parts)
                if context_parts
                else "Positive market conditions for skilled graduates"
            )

        return "General technology and business market opportunities available"

    def _extract_preferences(self, validated_input: Dict[str, Any]) -> str:
        """Extract student preferences from optional inputs"""
        optional_data = validated_input.get("optional_data", {})

        preferences = []

        if "company_preferences" in optional_data:
            preferences.append(f"Company: {optional_data['company_preferences']}")

        if "work_mode_preferences" in optional_data:
            preferences.append(f"Work Mode: {optional_data['work_mode_preferences']}")

        if "salary_expectations" in optional_data:
            preferences.append(f"Salary: {optional_data['salary_expectations']}")

        if "industry_focus" in optional_data:
            preferences.append(f"Industry: {optional_data['industry_focus']}")

        return (
            "; ".join(preferences)
            if preferences
            else "Open to diverse opportunities with growth potential and good learning environment"
        )

    def _extract_timeline_context(self, validated_input: Dict[str, Any]) -> str:
        """Extract timeline context for opportunity matching"""
        optional_data = validated_input.get("optional_data", {})

        if "timeline_urgency" in optional_data:
            return str(optional_data["timeline_urgency"])

        # Infer from academic status if available
        if "academic_status" in optional_data:
            academic = optional_data["academic_status"]
            year = academic.get("current_year", "Unknown")

            if year == 4:
                return "Final year - immediate job search and placement urgency"
            elif year == 3:
                return "Pre-final year - internship focus with job search preparation"

        return "Flexible timeline with focus on best-fit opportunities"

    def _extract_geographic_focus(self, validated_input: Dict[str, Any]) -> str:
        """Extract geographic preferences"""
        optional_data = validated_input.get("optional_data", {})

        if "geographic_preferences" in optional_data:
            return str(optional_data["geographic_preferences"])

        return "India (major tech hubs) with openness to remote opportunities"

    def _get_matching_criteria(self) -> List[str]:
        """Get the criteria used for opportunity matching"""
        return [
            "Technical skill alignment",
            "Career goal compatibility",
            "Company culture fit",
            "Growth potential",
            "Learning opportunities",
            "Geographic accessibility",
            "Compensation alignment",
            "Network connection potential",
        ]

    def _get_key_success_factors(self, output_dict: Dict[str, Any]) -> List[str]:
        """Extract key success factors from analysis"""
        success_factors = [
            "Strong technical preparation",
            "Effective networking and referrals",
            "Customized application approach",
            "Interview preparation and practice",
            "Portfolio project demonstration",
        ]

        return success_factors

    def _assess_personalization_level(self, validated_input: Dict[str, Any]) -> str:
        """Assess how personalized the opportunity matching can be"""
        data_points = 0

        # Count available data sources
        if validated_input.get("previous_outputs", {}).get("profile_analysis"):
            data_points += 3
        if validated_input.get("previous_outputs", {}).get(
            "career_optimization_planner"
        ):
            data_points += 3
        if validated_input.get("previous_outputs", {}).get("market_intelligence"):
            data_points += 2

        optional_data_count = len(validated_input.get("optional_data", {}))
        data_points += optional_data_count

        if data_points >= 10:
            return "Highly personalized"
        elif data_points >= 6:
            return "Moderately personalized"
        else:
            return "Generally applicable"

    def _create_implementation_guidance(
        self, output_dict: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Create implementation guidance for opportunity pursuit"""
        return {
            "immediate_actions": [
                "Review and prioritize matched opportunities",
                "Customize resume and cover letter for top opportunities",
                "Research target companies thoroughly",
                "Prepare for technical and behavioral interviews",
            ],
            "weekly_tasks": [
                "Apply to 3-5 high-priority opportunities",
                "Reach out to network connections for referrals",
                "Practice interview questions and technical skills",
                "Follow up on submitted applications",
            ],
            "monthly_goals": [
                "Complete applications to all top-tier opportunities",
                "Attend networking events and company information sessions",
                "Build portfolio projects that demonstrate relevant skills",
                "Seek informational interviews with industry professionals",
            ],
        }

    def _calculate_confidence_score(
        self, validated_data: Dict[str, Any], output_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for opportunity matching"""
        base_confidence = 0.75  # Good confidence for opportunity matching

        # Boost confidence with quality inputs from previous agents
        if validated_data.get("previous_outputs", {}).get("profile_analysis"):
            base_confidence += 0.08

        if validated_data.get("previous_outputs", {}).get(
            "career_optimization_planner"
        ):
            base_confidence += 0.08

        if validated_data.get("previous_outputs", {}).get("market_intelligence"):
            base_confidence += 0.04

        # Check output completeness
        expected_components = [
            "matched_opportunities",
            "compatibility_analysis",
            "application_strategy",
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
