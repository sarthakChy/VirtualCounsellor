from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from agentic_layer.base_agent import BaseAgent
from config.agent_config import AgentType, CareerOptimizationOutput
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class CareerOptimizationPlannerAgent(BaseAgent):
    """
    Career Optimization Planner Agent for College Student Fleet

    Role: Career Coach and Strategic Planner
    Purpose: Develops comprehensive career strategy for maximizing opportunities in chosen field

    Key Features:
    - Short-term (6 months) and long-term (2-3 years) goal setting
    - Internship and job application strategy
    - Network building and professional relationship development
    - Personal branding and online presence optimization
    - Interview preparation and negotiation strategies
    """

    def __init__(self, llm_model=None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id="career_optimization_planner",
            agent_name="Career Optimization Planner Agent",
            agent_type=AgentType.VERTICAL_SPECIFIC,
            llm_model=llm_model,
            config=config,
        )

    def _define_required_inputs(self) -> List[str]:
        """Define required inputs for skill development strategy"""
        return []  # No direct user data required - gets data from previous agents

    def _define_optional_inputs(self) -> List[str]:
        """Define optional inputs that enhance career planning"""
        return [
            "resume_data",  # Current resume for context
            "linkedin_profile",  # Professional presence analysis
            "academic_status",  # Timeline and constraints context
            "career_preferences",  # Specific career goals/preferences
            "geographic_preferences",  # Location preferences
            "company_preferences",  # Target company types
            "work_life_balance_priorities",  # Personal priorities
            "salary_expectations",  # Financial goals
            "industry_connections",  # Existing professional network
        ]

    def _define_output_schema(self) -> Dict[str, Any]:
        """Define the structure of career optimization output"""
        return {
            "career_goals": "Structured career goals with timelines and success metrics",
            "career_strategy": "Overall strategic approach for career development",
            "networking_plan": "Professional networking and relationship building strategy",
            "job_search_strategy": "Job search, application, and interview strategy",
            "personal_branding": "Personal branding and online presence optimization",
            "action_planning": "Monthly action plans and implementation strategy",
            "success_tracking": "KPIs and methods for tracking progress",
        }

    def _initialize_agent(self):
        """Initialize career optimization planner specific components"""
        self.output_parser = JsonOutputParser(pydantic_object=CareerOptimizationOutput)

        # Main career optimization strategy prompt
        self.optimization_prompt = PromptTemplate(
            input_variables=[
                "profile_summary",
                "current_strengths",
                "skill_development_plan",
                "market_opportunities",
                "career_preferences",
                "timeline_constraints",
                "academic_context",
                "analysis_date",
                "format_instructions",
            ],
            template=self._create_system_prompt(
                "Career Coach and Strategic Planner",
                """
Context Information:
- Analysis Date: {analysis_date}
- Profile Summary: {profile_summary}
- Current Strengths: {current_strengths}
- Skill Development Plan: {skill_development_plan}
- Market Opportunities: {market_opportunities}
- Career Preferences: {career_preferences}
- Timeline Constraints: {timeline_constraints}
- Academic Context: {academic_context}

Your expertise includes:
- Strategic career planning with goal-setting methodologies
- Job market navigation and opportunity maximization
- Professional networking and relationship building
- Personal branding and thought leadership development
- Interview preparation and salary negotiation
- Career pivot and transition management
- Professional development and continuous learning strategies

Strategic Planning Framework:
1. Goal Architecture: Design SMART career goals with clear timelines
2. Strategy Development: Create multi-layered approach for career advancement
3. Market Positioning: Position student optimally in competitive job market
4. Network Development: Build strategic professional relationships
5. Brand Building: Establish strong personal and professional brand
6. Execution Planning: Create detailed action plans with milestones
7. Risk Management: Identify potential challenges and mitigation strategies
8. Success Tracking: Establish KPIs and progress monitoring systems

Focus Areas for College Students:
- Transition from academic to professional environment
- Building job-ready professional presence and network
- Optimizing internship and entry-level job search strategies
- Developing industry credibility and thought leadership
- Balancing multiple opportunities and making strategic choices
- Preparing for salary negotiations and career advancement
- Building resilience and adaptability for changing job markets

Career Optimization Priorities:
- Immediate job readiness and competitive positioning
- Long-term career trajectory and growth planning
- Professional network development and maintenance
- Personal brand establishment and thought leadership
- Interview success and negotiation preparation
- Continuous learning and skill evolution planning
- Industry relationship building and mentorship acquisition

Timeline Considerations:
- Academic calendar alignment with recruitment cycles
- Industry-specific hiring patterns and peak seasons
- Skill development timelines vs job application deadlines
- Network building progression and relationship development
- Personal branding evolution and content creation schedules
- Interview preparation and practice timeline requirements

CRITICAL: Ensure all JSON output is valid. Do not use comments like // in JSON. 
All property names must be in double quotes. All strings must be properly escaped.

{format_instructions}
                """,
            )
            + "\n\nProvide comprehensive career optimization strategy in the specified JSON format. Make sure the JSON is completely valid with no syntax errors.",
        )

        self.logger.info("Career Optimization Planner Agent initialized")

    @traceable(
        name="comprehensive_career_strategy",
        tags=["career_optimization_strategy", "comprehensive", "llm_chain"],
    )
    def _process_core_logic(self, validated_input: Dict[str, Any]) -> Dict[str, Any]:
        """Core career optimization planning logic"""
        self._add_processing_note("Starting career optimization strategy development")

        # Extract required inputs from previous agents
        profile_analysis = self._extract_agent_output(
            validated_input, "profile_analysis"
        )
        market_intelligence = self._extract_agent_output(
            validated_input, "market_intelligence"
        )
        skill_development = self._extract_agent_output(
            validated_input, "skill_development_strategist"
        )

        # Extract context information
        profile_summary = self._create_profile_summary(profile_analysis)
        current_strengths = self._extract_current_strengths(profile_analysis)
        skill_plan = self._extract_skill_development_summary(skill_development)
        market_opportunities = self._extract_market_opportunities(market_intelligence)
        career_preferences = self._extract_career_preferences(validated_input)
        timeline_constraints = self._extract_timeline_constraints(validated_input)
        academic_context = self._extract_academic_context(validated_input)

        self.logger.info("Developing comprehensive career optimization strategy")

        # Prepare prompt inputs
        prompt_inputs = {
            "profile_summary": profile_summary,
            "current_strengths": current_strengths,
            "skill_development_plan": skill_plan,
            "market_opportunities": market_opportunities,
            "career_preferences": career_preferences,
            "timeline_constraints": timeline_constraints,
            "academic_context": academic_context,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "format_instructions": self.output_parser.get_format_instructions(),
        }

        formatted_prompt = self.optimization_prompt.format(**prompt_inputs)
        response = self.llm_model.invoke(formatted_prompt)

        output_dict = self._parse_llm_response(response)

        # Add metadata
        output_dict["optimization_metadata"] = {
            "analysis_date": prompt_inputs["analysis_date"],
            "planning_horizon": "6 months to 3 years",
            "strategy_components": list(output_dict.keys()),
            "personalization_level": self._assess_personalization_level(
                validated_input
            ),
            "implementation_complexity": self._assess_implementation_complexity(
                output_dict
            ),
            "success_probability": self._estimate_success_probability(
                validated_input, output_dict
            ),
        }

        # Add implementation timeline
        output_dict["implementation_timeline"] = self._create_implementation_timeline(
            output_dict
        )

        self._add_processing_note("Career optimization strategy completed successfully")
        return output_dict

    @traceable(
        name="previous_agent_output_extraction",
        tags=["career_optimization_strategy", "previous_outputs", "llm_chain"],
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

    def _create_profile_summary(self, profile_analysis: Dict[str, Any]) -> str:
        """Create comprehensive profile summary for strategy context"""
        summary_parts = []

        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            # Extract key profile elements
            if "profile_positioning" in comp_analysis:
                summary_parts.append(
                    f"Profile Positioning: {comp_analysis['profile_positioning']}"
                )

            if "experience_level" in comp_analysis:
                summary_parts.append(
                    f"Experience Level: {comp_analysis['experience_level']}"
                )

            if "primary_domain" in comp_analysis:
                summary_parts.append(
                    f"Primary Domain: {comp_analysis['primary_domain']}"
                )

            if "competitive_advantages" in comp_analysis:
                advantages = comp_analysis["competitive_advantages"]
                if isinstance(advantages, list):
                    summary_parts.append(f"Key Advantages: {', '.join(advantages[:3])}")

        return (
            "; ".join(summary_parts)
            if summary_parts
            else "College student with developing professional profile"
        )

    def _extract_current_strengths(self, profile_analysis: Dict[str, Any]) -> str:
        """Extract current strengths for strategy building"""
        strengths = []

        if "comprehensive_analysis" in profile_analysis:
            comp_analysis = profile_analysis["comprehensive_analysis"]

            if "profile_strengths" in comp_analysis:
                profile_strengths = comp_analysis["profile_strengths"]
                if isinstance(profile_strengths, list):
                    strengths.extend(profile_strengths[:5])

            if "technical_skills" in comp_analysis:
                tech_skills = comp_analysis["technical_skills"]
                if isinstance(tech_skills, dict):
                    strong_skills = [
                        skill
                        for skill, level in tech_skills.items()
                        if level in ["Advanced", "Expert", "Strong"]
                    ]
                    strengths.extend(strong_skills[:3])

        return (
            ", ".join(strengths)
            if strengths
            else "Foundational skills and strong learning ability"
        )

    def _extract_skill_development_summary(
        self, skill_development: Dict[str, Any]
    ) -> str:
        """Extract skill development plan summary"""
        if not skill_development:
            return "General skill development recommended"

        summary_parts = []

        # Add null check for development_roadmap
        if (
            "development_roadmap" in skill_development
            and skill_development["development_roadmap"]
        ):
            roadmap = skill_development["development_roadmap"]
            if isinstance(roadmap, dict):
                if "immediate_actions" in roadmap and roadmap["immediate_actions"]:
                    immediate = roadmap["immediate_actions"]
                    if isinstance(immediate, list):
                        summary_parts.append(
                            f"Immediate Actions: {'; '.join(immediate[:3])}"
                        )

        return (
            "; ".join(summary_parts)
            if summary_parts
            else "Structured skill development plan in progress"
        )

    def _extract_market_opportunities(self, market_intelligence: Dict[str, Any]) -> str:
        """Extract key market opportunities"""
        if not market_intelligence:
            return "General technology and business opportunities available"

        opportunities = []

        if "job_market_outlook" in market_intelligence:
            outlook = market_intelligence["job_market_outlook"]
            if isinstance(outlook, dict) and "growth_areas" in outlook:
                growth_areas = outlook["growth_areas"]
                if isinstance(growth_areas, list):
                    opportunities.extend(growth_areas[:3])

        if "emerging_technologies" in market_intelligence:
            emerging = market_intelligence["emerging_technologies"]
            if isinstance(emerging, list):
                opportunities.extend([f"{tech} technology" for tech in emerging[:2]])

        return (
            ", ".join(opportunities)
            if opportunities
            else "Diverse opportunities in technology and business sectors"
        )

    def _extract_career_preferences(self, validated_input: Dict[str, Any]) -> str:
        """Extract career preferences from optional inputs"""
        optional_data = validated_input.get("optional_data", {})

        preferences = []

        if "career_preferences" in optional_data:
            preferences.append(str(optional_data["career_preferences"]))

        if "company_preferences" in optional_data:
            preferences.append(
                f"Company preference: {optional_data['company_preferences']}"
            )

        if "work_life_balance_priorities" in optional_data:
            preferences.append(
                f"Work-life balance: {optional_data['work_life_balance_priorities']}"
            )

        return (
            "; ".join(preferences)
            if preferences
            else "Open to diverse career opportunities with growth potential"
        )

    def _extract_timeline_constraints(self, validated_input: Dict[str, Any]) -> str:
        """Extract timeline constraints and graduation context"""
        optional_data = validated_input.get("optional_data", {})

        if "academic_status" in optional_data:
            academic = optional_data["academic_status"]
            current_year = academic.get("current_year", "Unknown")

            if current_year == 4:
                return (
                    "Final year - 6-12 months for job search preparation and placement"
                )
            elif current_year == 3:
                return (
                    "Pre-final year - 12-18 months for internships and skill building"
                )
            elif current_year in [1, 2]:
                return "Early college - 2-3 years for comprehensive career development"

        return "Flexible timeline with focus on steady career progression"

    def _extract_academic_context(self, validated_input: Dict[str, Any]) -> str:
        """Extract academic context for career planning"""
        optional_data = validated_input.get("optional_data", {})

        if "academic_status" in optional_data:
            academic = optional_data["academic_status"]
            context_parts = []

            if "gpa" in academic:
                context_parts.append(f"GPA: {academic['gpa']}")

            if "major_subjects" in academic:
                subjects = academic["major_subjects"]
                if isinstance(subjects, list):
                    context_parts.append(f"Major subjects: {', '.join(subjects[:3])}")

            return (
                "; ".join(context_parts)
                if context_parts
                else "College student in good academic standing"
            )

        return "College student with solid academic foundation"

    def _assess_personalization_level(self, validated_input: Dict[str, Any]) -> str:
        """Assess how personalized the strategy can be"""
        data_points = 0

        # Count available data sources
        if validated_input.get("previous_outputs", {}).get("profile_analysis"):
            data_points += 3
        if validated_input.get("previous_outputs", {}).get("market_intelligence"):
            data_points += 2
        if validated_input.get("previous_outputs", {}).get(
            "skill_development_strategist"
        ):
            data_points += 2

        optional_data_count = len(validated_input.get("optional_data", {}))
        data_points += optional_data_count

        if data_points >= 8:
            return "Highly personalized"
        elif data_points >= 5:
            return "Moderately personalized"
        else:
            return "Generally applicable"

    def _assess_implementation_complexity(self, output_dict: Dict[str, Any]) -> str:
        """Assess implementation complexity of the strategy"""
        complexity_factors = 0

        # Count career goals
        if "career_goals" in output_dict:
            career_goals = output_dict["career_goals"]
            if isinstance(career_goals, list):
                complexity_factors += len(career_goals)

        # Count monthly action items
        if "monthly_action_plan" in output_dict:
            monthly_plan = output_dict["monthly_action_plan"]
            if isinstance(monthly_plan, dict):
                complexity_factors += sum(
                    len(actions)
                    for actions in monthly_plan.values()
                    if isinstance(actions, list)
                )

        if complexity_factors >= 20:
            return "High complexity - requires dedicated effort and time management"
        elif complexity_factors >= 10:
            return "Moderate complexity - manageable with good planning"
        else:
            return "Low complexity - straightforward implementation"

    def _estimate_success_probability(
        self, validated_input: Dict[str, Any], output_dict: Dict[str, Any]
    ) -> float:
        """Estimate probability of strategy success"""
        base_probability = 0.7

        # Boost for strong profile analysis
        if validated_input.get("previous_outputs", {}).get("profile_analysis"):
            base_probability += 0.1

        # Boost for market alignment
        if validated_input.get("previous_outputs", {}).get("market_intelligence"):
            base_probability += 0.1

        # Boost for clear skill development plan
        if validated_input.get("previous_outputs", {}).get(
            "skill_development_strategist"
        ):
            base_probability += 0.05

        # Reduce for high complexity without sufficient support
        complexity = self._assess_implementation_complexity(output_dict)
        if "High complexity" in complexity:
            base_probability -= 0.05

        return min(0.9, base_probability)  # Cap at 90%

    def _create_implementation_timeline(
        self, output_dict: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Create implementation timeline from strategy components"""
        timeline = {
            "Week 1-2": [
                "Set up tracking systems and KPIs",
                "Begin personal branding optimization",
                "Start immediate skill development actions",
            ],
            "Month 1": [
                "Complete profile optimizations",
                "Begin networking outreach",
                "Start first set of career goals",
            ],
            "Month 2-3": [
                "Intensify networking efforts",
                "Begin job search preparation",
                "Complete initial skill certifications",
            ],
            "Month 4-6": [
                "Launch job search activities",
                "Leverage network for opportunities",
                "Complete major skill development milestones",
            ],
        }

        return timeline

    def _calculate_confidence_score(
        self, validated_data: Dict[str, Any], output_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for career optimization strategy"""
        base_confidence = 0.75  # Good confidence for strategic planning

        # Boost confidence with quality inputs from previous agents
        if validated_data.get("previous_outputs", {}).get("profile_analysis"):
            base_confidence += 0.08

        if validated_data.get("previous_outputs", {}).get("market_intelligence"):
            base_confidence += 0.07

        if validated_data.get("previous_outputs", {}).get(
            "skill_development_strategist"
        ):
            base_confidence += 0.05

        # Check strategy completeness
        expected_components = [
            "career_goals",
            "career_strategy",
            "networking_plan",
            "job_search_strategy",
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
