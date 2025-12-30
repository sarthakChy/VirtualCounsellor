import json
from typing import Dict, List, Any
from agentic_layer.base_agent import BaseAgent
from agentic_layer.base_fleet_manager import BaseFleetManager
from config.agent_config import AgentDependency, AgentResult, ProcessingStatus
from config.llm_config import llm_manager
from agentic_layer.college_upskill.agents.profile_analysis_agent import (
    ProfileAnalysisAgent,
)
from agentic_layer.college_upskill.agents.market_intelligence_agent import (
    MarketIntelligenceAgent,
)
from agentic_layer.college_upskill.agents.skill_development_strategist_agent import (
    SkillDevelopmentStrategistAgent,
)
from agentic_layer.college_upskill.agents.career_optimization_planner_agent import (
    CareerOptimizationPlannerAgent,
)
from agentic_layer.college_upskill.agents.opportunity_matcher_agent import (
    OpportunityMatcherAgent,
)


class CollegeStudentFleetManager(BaseFleetManager):
    """
    Fleet manager for college students seeking upskilling and career optimization

    Manages agents: profile_analysis, market_intelligence, skill_development_strategist,
                   career_optimization_planner, opportunity_matcher
    """

    def __init__(self, llm_model=None):
        if llm_model is None:
            llm_model = llm_manager.get_llm()

        super().__init__(
            fleet_id="college_upskilling_fleet",
            fleet_name="College Student Career Optimization Fleet",
            llm_model=llm_model,
        )

    def _initialize_fleet(self):
        """Initialize college student specific agents and dependencies"""
        self.logger.info("Initializing College Student Fleet")

        # Define agent execution order and dependencies
        self.execution_order = [
            "profile_analysis",  # Analyze resume/LinkedIn/GitHub first
            "market_intelligence",  # Get market data
            "skill_development_strategist",  # Identify skill gaps and development plan
            "career_optimization_planner",  # Create career strategy
            "opportunity_matcher",  # Match with specific opportunities
        ]

        # Define dependencies
        self.agent_dependencies = {
            "profile_analysis": AgentDependency("profile_analysis", depends_on=[]),
            "market_intelligence": AgentDependency(
                "market_intelligence", depends_on=[]
            ),
            "skill_development_strategist": AgentDependency(
                "skill_development_strategist",
                depends_on=["profile_analysis", "market_intelligence"],
                required_outputs=["current_skills", "market_trends"],
            ),
            "career_optimization_planner": AgentDependency(
                "career_optimization_planner",
                depends_on=[
                    "profile_analysis",
                    "market_intelligence",
                    "skill_development_strategist",
                ],
                required_outputs=["profile_summary", "skill_gaps", "development_plan"],
            ),
            "opportunity_matcher": AgentDependency(
                "opportunity_matcher",
                depends_on=["profile_analysis", "career_optimization_planner"],
                required_outputs=["profile_summary", "career_goals"],
            ),
        }

        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize actual agent instances"""
        try:
            # Initialize Profile Analysis Agent
            profile_agent = ProfileAnalysisAgent(llm_model=self.llm_model)
            self.add_agent(
                profile_agent, self.agent_dependencies.get("profile_analysis")
            )
            self.logger.info(f"Initialized agent: {profile_agent.agent_name}")

            market_agent = MarketIntelligenceAgent(llm_model=self.llm_model)
            self.add_agent(
                market_agent, self.agent_dependencies.get("market_intelligence")
            )
            self.logger.info(f"Initialized agent: {market_agent.agent_name}")

            skill_agent = SkillDevelopmentStrategistAgent(llm_model=self.llm_model)
            self.add_agent(
                skill_agent, self.agent_dependencies.get("skill_development_strategist")
            )
            self.logger.info(f"Initialized agent: {skill_agent.agent_name}")

            career_agent = CareerOptimizationPlannerAgent(llm_model=self.llm_model)
            self.add_agent(
                career_agent, self.agent_dependencies.get("career_optimization_planner")
            )
            self.logger.info(f"Initialized agent: {career_agent.agent_name}")

            opportunity_agent = OpportunityMatcherAgent(llm_model=self.llm_model)
            self.add_agent(
                opportunity_agent, self.agent_dependencies.get("opportunity_matcher")
            )
            self.logger.info(f"Initialized agent: {opportunity_agent.agent_name}")

            self.logger.info("All agents initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {e}")

    def _validate_fleet_input(
        self, user_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """Validate input data for college student fleet"""
        required_fields = ["resume_data"]  # Resume is mandatory
        optional_fields = [
            "github_profile",
            "linkedin_profile",
            "academic_status",
            "internship_experience",
            "project_experience",
        ]

        missing_required = []

        # Check required fields
        for field in required_fields:
            if field not in user_data or user_data[field] is None:
                missing_required.append(field)
            elif (
                isinstance(user_data[field], (dict, list))
                and len(user_data[field]) == 0
            ):
                missing_required.append(field)

        # Log available optional data
        available_optional = [
            field
            for field in optional_fields
            if field in user_data and user_data[field] is not None
        ]

        self.logger.info(f"Available optional data: {available_optional}")

        is_valid = len(missing_required) == 0
        return is_valid, missing_required

    def _create_execution_plan(self, user_data: Dict[str, Any]) -> List[str]:
        """Create execution plan based on available data"""
        plan = []

        # Always start with profile analysis if we have resume
        if user_data.get("resume_data"):
            plan.append("profile_analysis")

        # Market intelligence can run independently
        plan.append("market_intelligence")

        # Skill development strategist needs profile analysis
        if "profile_analysis" in plan:
            plan.append("skill_development_strategist")

        # Career optimization planner needs previous agents
        if "profile_analysis" in plan and "skill_development_strategist" in plan:
            plan.append("career_optimization_planner")

        # Opportunity matcher needs profile and career planning
        if "profile_analysis" in plan and "career_optimization_planner" in plan:
            plan.append("opportunity_matcher")

        self.logger.info(f"Created execution plan with {len(plan)} agents: {plan}")
        return plan

    def _generate_fleet_recommendations(
        self, agent_results: Dict[str, AgentResult]
    ) -> List[str]:
        """Generate overall recommendations from agent results"""
        recommendations = []

        # Add recommendations based on successful agent outputs
        if (
            "profile_analysis" in agent_results
            and agent_results["profile_analysis"].status == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Update your professional profiles based on the analysis"
            )
            recommendations.append(
                "Focus on highlighting your strongest skills and experiences"
            )

        if (
            "market_intelligence" in agent_results
            and agent_results["market_intelligence"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Stay updated with the latest industry trends and requirements"
            )
            recommendations.append(
                "Consider emerging technologies and skills in your field"
            )

        if (
            "skill_development_strategist" in agent_results
            and agent_results["skill_development_strategist"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append("Follow the recommended skill development roadmap")
            recommendations.append(
                "Prioritize high-impact skills for your target roles"
            )

        if (
            "career_optimization_planner" in agent_results
            and agent_results["career_optimization_planner"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Implement your personalized career optimization strategy step by step"
            )
            recommendations.append(
                "Begin executing your networking and job search plan immediately"
            )
            recommendations.append(
                "Set up tracking systems to monitor progress on career goals"
            )
            recommendations.append(
                "Start building your personal brand as outlined in the strategy"
            )

        if (
            "opportunity_matcher" in agent_results
            and agent_results["opportunity_matcher"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Apply to matched opportunities that align with your profile"
            )
            recommendations.append(
                "Customize your applications based on opportunity requirements"
            )

        # Add general recommendations
        recommendations.extend(
            [
                "Build a strong professional network in your target industry",
                "Create a portfolio showcasing your best work and projects",
                "Practice interview skills and prepare for technical assessments",
                "Consider gaining practical experience through internships or projects",
            ]
        )

        return recommendations

    def get_fleet_info(self) -> Dict[str, Any]:
        """Get information about this fleet"""
        return {
            "fleet_id": self.fleet_id,
            "fleet_name": self.fleet_name,
            "agent_count": len(self.execution_order),
            "agents": self.execution_order,
            "required_inputs": ["resume_data"],
            "optional_inputs": [
                "github_profile",
                "linkedin_profile",
                "academic_status",
                "internship_experience",
                "project_experience",
            ],
            "execution_strategy": self.execution_strategy.value,
            "dependencies": {
                agent_id: dep.depends_on
                for agent_id, dep in self.agent_dependencies.items()
            },
            "execution_history_count": len(self.execution_history),
        }

    def register_agent(self, agent: BaseAgent):
        """Register a real agent implementation"""
        if agent.agent_id in self.execution_order:
            self.add_agent(agent, self.agent_dependencies.get(agent.agent_id))
            self.logger.info(f"Registered real agent: {agent.agent_name}")
        else:
            self.logger.warning(f"Agent {agent.agent_id} not in execution order")

    def can_execute(
        self, user_data: Dict[str, Any]
    ) -> tuple[bool, List[str], Dict[str, Any]]:
        """Check if fleet can execute with given data"""
        is_valid, missing_data = self._validate_fleet_input(user_data)

        execution_info = {
            "can_execute": is_valid,
            "missing_data": missing_data,
            "execution_plan": (
                self._create_execution_plan(user_data) if is_valid else []
            ),
            "estimated_agents": (
                len(self._create_execution_plan(user_data)) if is_valid else 0
            ),
            "estimated_time_minutes": (
                len(self._create_execution_plan(user_data)) * 2 if is_valid else 0
            ),
        }

        return is_valid, missing_data, execution_info
