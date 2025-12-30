from typing import Dict, List, Any
from agentic_layer.base_agent import BaseAgent
from agentic_layer.base_fleet_manager import BaseFleetManager
from config.agent_config import AgentDependency, AgentResult, ProcessingStatus
from config.llm_config import llm_manager
from agentic_layer.school_students.agents.test_score_interpreter_agent import (
    TestScoreInterpreterAgent,
)
from agentic_layer.school_students.agents.academic_stream_advisor_agent import (
    AcademicStreamAdvisorAgent,
)
from agentic_layer.school_students.agents.career_pathway_explorer_agent import (
    CareerPathwayExplorerAgent,
)
from agentic_layer.school_students.agents.educational_roadmap_planner_agent import (
    EducationalRoadmapPlannerAgent,
)
from agentic_layer.school_students.agents.college_and_scholarship_navigator_agent import (
    CollegeScholarshipNavigatorAgent,
)


class SchoolStudentFleetManager(BaseFleetManager):
    """
    Fleet manager for school students (grades 9-12) seeking career exploration and academic guidance

    Manages agents: test_score_interpreter, academic_stream_advisor, career_pathway_explorer,
                   educational_roadmap_planner, college_scholarship_navigator
    """

    def __init__(self, llm_model=None):
        if llm_model is None:
            llm_model = llm_manager.get_llm()

        super().__init__(
            fleet_id="school_students_fleet",
            fleet_name="School Students Career Exploration Fleet",
            llm_model=llm_model,
        )

    def _initialize_fleet(self):
        self.logger.info("Initializing School Student Fleet")

        # Define agent execution order and dependencies
        self.execution_order = [
            "test_score_interpreter",  # Interpret DBDA, CII
            "academic_stream_advisor",  # Recommend streams based on test interpretation
            "career_pathway_explorer",  # Explore career options from stream choices
            "educational_roadmap_planner",  # Create detailed educational pathway
            "college_scholarship_navigator",  # Map colleges and financial aid opportunities
        ]

        # Define dependencies
        self.agent_dependencies = {
            "test_score_interpreter": AgentDependency(
                "test_score_interpreter", depends_on=[]
            ),
            "academic_stream_advisor": AgentDependency(
                "academic_stream_advisor",
                depends_on=["test_score_interpreter"],
                required_outputs=[
                    "aptitude_analysis",
                    "interest_mapping",
                    "personality_insights",
                ],
            ),
            "career_pathway_explorer": AgentDependency(
                "career_pathway_explorer",
                depends_on=["test_score_interpreter", "academic_stream_advisor"],
                required_outputs=["recommended_streams", "cognitive_strengths"],
            ),
            "educational_roadmap_planner": AgentDependency(
                "educational_roadmap_planner",
                depends_on=["academic_stream_advisor", "career_pathway_explorer"],
                required_outputs=[
                    "recommended_streams",
                    "recommended_career_pathways",
                ],  # Map the actual output keys
            ),
            "college_scholarship_navigator": AgentDependency(
                "college_scholarship_navigator",
                depends_on=["career_pathway_explorer", "educational_roadmap_planner"],
                required_outputs=[
                    "career_goals",
                    "educational_pathway",
                    "academic_timeline",
                ],
            ),
        }

        self._initialize_agents()

    def _initialize_agents(self):
        try:
            # Initialize Test Score Interpreter Agent
            test_interpreter_agent = TestScoreInterpreterAgent(llm_model=self.llm_model)
            self.add_agent(
                test_interpreter_agent,
                self.agent_dependencies.get("test_score_interpreter"),
            )
            self.logger.info(f"Initialized agent: {test_interpreter_agent.agent_name}")

            # Initialize Academic Stream Advisor Agent
            stream_advisor_agent = AcademicStreamAdvisorAgent(llm_model=self.llm_model)
            self.add_agent(
                stream_advisor_agent,
                self.agent_dependencies.get("academic_stream_advisor"),
            )
            self.logger.info(f"Initialized agent: {stream_advisor_agent.agent_name}")

            # Initialize Career Pathway Explorer Agent
            career_explorer_agent = CareerPathwayExplorerAgent(llm_model=self.llm_model)
            self.add_agent(
                career_explorer_agent,
                self.agent_dependencies.get("career_pathway_explorer"),
            )
            self.logger.info(f"Initialized agent: {career_explorer_agent.agent_name}")

            # Initialize Educational Roadmap Planner Agent
            roadmap_planner_agent = EducationalRoadmapPlannerAgent(
                llm_model=self.llm_model
            )
            self.add_agent(
                roadmap_planner_agent,
                self.agent_dependencies.get("educational_roadmap_planner"),
            )
            self.logger.info(f"Initialized agent: {roadmap_planner_agent.agent_name}")

            # Initialize College Scholarship Navigator Agent
            college_navigator_agent = CollegeScholarshipNavigatorAgent(
                llm_model=self.llm_model
            )
            self.add_agent(
                college_navigator_agent,
                self.agent_dependencies.get("college_scholarship_navigator"),
            )
            self.logger.info(f"Initialized agent: {college_navigator_agent.agent_name}")

            self.logger.info("All school student agents initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize school student agents: {e}")

    def _validate_fleet_input(
        self, user_data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        required_fields = [
            "dbda_scores",
            "cii_results",
        ]  # All assessment data mandatory
        optional_fields = [
            "demographic_info",
            "current_grade",
            "academic_performance",
            "extracurricular_activities",
            "family_preferences",
            "geographical_preferences",
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

        # Validate assessment data structure
        if "dbda_scores" in user_data and user_data["dbda_scores"]:
            if not isinstance(user_data["dbda_scores"], dict):
                missing_required.append("dbda_scores (invalid format)")

        if "cii_results" in user_data and user_data["cii_results"]:
            if not isinstance(user_data["cii_results"], dict):
                missing_required.append("cii_results (invalid format)")

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
        plan = []

        # Always start with test score interpretation if we have assessment data
        if user_data.get("dbda_scores") and user_data.get("cii_results"):
            plan.append("test_score_interpreter")

        # Academic stream advisor needs test interpretation
        if "test_score_interpreter" in plan:
            plan.append("academic_stream_advisor")

        # Career pathway explorer needs both previous agents
        if "test_score_interpreter" in plan and "academic_stream_advisor" in plan:
            plan.append("career_pathway_explorer")

        # Educational roadmap planner needs stream and career guidance
        if "academic_stream_advisor" in plan and "career_pathway_explorer" in plan:
            plan.append("educational_roadmap_planner")

        # College scholarship navigator needs career and educational planning
        if "career_pathway_explorer" in plan and "educational_roadmap_planner" in plan:
            plan.append("college_scholarship_navigator")

        self.logger.info(f"Created execution plan with {len(plan)} agents: {plan}")
        return plan

    def _generate_fleet_recommendations(
        self, agent_results: Dict[str, AgentResult]
    ) -> List[str]:
        """Generate overall recommendations from agent results"""
        recommendations = []

        # Add recommendations based on successful agent outputs
        if (
            "test_score_interpreter" in agent_results
            and agent_results["test_score_interpreter"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Discuss your assessment results with parents and school counselors"
            )
            recommendations.append(
                "Focus on developing your identified cognitive strengths"
            )
            recommendations.append(
                "Explore activities that align with your interest areas"
            )

        if (
            "academic_stream_advisor" in agent_results
            and agent_results["academic_stream_advisor"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Carefully consider the recommended academic streams"
            )
            recommendations.append(
                "Research subject requirements and career implications for each stream"
            )
            recommendations.append(
                "Talk to current students and professionals in fields that interest you"
            )

        if (
            "career_pathway_explorer" in agent_results
            and agent_results["career_pathway_explorer"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Explore the suggested career paths through internships or job shadowing"
            )
            recommendations.append(
                "Build relevant skills and knowledge in your areas of interest"
            )
            recommendations.append("Connect with professionals in your target fields")

        if (
            "educational_roadmap_planner" in agent_results
            and agent_results["educational_roadmap_planner"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append("Follow the grade-wise milestone plan consistently")
            recommendations.append(
                "Start preparation for relevant entrance exams early"
            )
            recommendations.append("Balance academics with extracurricular activities")
            recommendations.append(
                "Regularly review and adjust your educational timeline"
            )

        if (
            "college_scholarship_navigator" in agent_results
            and agent_results["college_scholarship_navigator"].status
            == ProcessingStatus.COMPLETED
        ):
            recommendations.append(
                "Research and shortlist colleges that match your goals and budget"
            )
            recommendations.append(
                "Apply for relevant scholarships and financial aid programs"
            )
            recommendations.append(
                "Visit college campuses and attend career counseling sessions"
            )
            recommendations.append(
                "Maintain good academic performance for scholarship eligibility"
            )

        # Add general recommendations for school students
        recommendations.extend(
            [
                "Maintain open communication with parents about career aspirations",
                "Seek guidance from teachers and school counselors regularly",
                "Participate in career-oriented workshops and competitions",
                "Develop both academic and soft skills consistently",
                "Stay informed about changing career landscapes and new opportunities",
                "Build a strong foundation in core subjects while exploring interests",
            ]
        )

        return recommendations

    def _assess_readiness_for_career_guidance(
        self, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        readiness_score = 0.7  # Base readiness for having assessment data
        readiness_factors = []

        # Check for additional readiness indicators
        if user_data.get("current_grade"):
            grade = user_data.get("current_grade", "")
            if "11" in str(grade) or "12" in str(grade):
                readiness_score += 0.2
                readiness_factors.append("Senior grade level indicates high readiness")
            elif "9" in str(grade) or "10" in str(grade):
                readiness_score += 0.1
                readiness_factors.append(
                    "Junior grade level allows for exploratory guidance"
                )

        if user_data.get("academic_performance"):
            readiness_score += 0.1
            readiness_factors.append(
                "Academic performance data available for informed guidance"
            )

        if user_data.get("extracurricular_activities"):
            readiness_factors.append("Extracurricular involvement shows engagement")

        return {
            "readiness_score": min(1.0, readiness_score),
            "readiness_factors": readiness_factors,
            "guidance_approach": self._determine_guidance_approach(
                readiness_score, user_data
            ),
        }

    def _determine_guidance_approach(
        self, readiness_score: float, user_data: Dict[str, Any]
    ) -> str:
        current_grade = user_data.get("current_grade", "")

        if readiness_score >= 0.9:
            return "comprehensive_career_planning"
        elif readiness_score >= 0.8:
            return "focused_stream_and_career_guidance"
        elif "9" in str(current_grade) or "10" in str(current_grade):
            return "exploratory_guidance_with_foundation_building"
        else:
            return "assessment_based_exploration"

    def get_fleet_info(self) -> Dict[str, Any]:
        return {
            "fleet_id": self.fleet_id,
            "fleet_name": self.fleet_name,
            "target_audience": "School students in grades 9-12",
            "agent_count": len(self.execution_order),
            "agents": self.execution_order,
            "required_inputs": ["dbda_scores", "cii_results"],
            "optional_inputs": [
                "demographic_info",
                "current_grade",
                "academic_performance",
                "extracurricular_activities",
                "family_preferences",
                "geographical_preferences",
            ],
            "assessment_requirements": {
                "dbda_scores": "Aptitude test scores in various cognitive domains",
                "cii_results": "Career Interest Inventory results showing interest patterns",
            },
            "execution_strategy": self.execution_strategy.value,
            "dependencies": {
                agent_id: dep.depends_on
                for agent_id, dep in self.agent_dependencies.items()
            },
            "execution_history_count": len(self.execution_history),
            "age_group_focus": "14-18 years (grades 9-12)",
            "guidance_types": [
                "stream_selection",
                "career_exploration",
                "educational_planning",
                "college_preparation",
            ],
        }

    def register_agent(self, agent: BaseAgent):
        if agent.agent_id in self.execution_order:
            self.add_agent(agent, self.agent_dependencies.get(agent.agent_id))
            self.logger.info(f"Registered real agent: {agent.agent_name}")
        else:
            self.logger.warning(f"Agent {agent.agent_id} not in execution order")

    def can_execute(
        self, user_data: Dict[str, Any]
    ) -> tuple[bool, List[str], Dict[str, Any]]:
        is_valid, missing_data = self._validate_fleet_input(user_data)
        readiness_assessment = self._assess_readiness_for_career_guidance(user_data)

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
            "readiness_assessment": readiness_assessment,
            "guidance_focus": (
                self._determine_primary_guidance_focus(user_data) if is_valid else None
            ),
        }

        return is_valid, missing_data, execution_info

    def _determine_primary_guidance_focus(
        self, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        current_grade = user_data.get("current_grade", "")
        focus_areas = []

        if "9" in str(current_grade):
            focus_areas = [
                "foundation_building",
                "interest_exploration",
                "early_stream_awareness",
            ]
        elif "10" in str(current_grade):
            focus_areas = [
                "stream_selection_preparation",
                "career_awareness",
                "skill_development",
            ]
        elif "11" in str(current_grade):
            focus_areas = [
                "stream_optimization",
                "career_planning",
                "entrance_exam_preparation",
            ]
        elif "12" in str(current_grade):
            focus_areas = [
                "college_selection",
                "career_finalization",
                "transition_planning",
            ]
        else:
            focus_areas = ["general_career_exploration", "aptitude_development"]

        return {
            "primary_focus_areas": focus_areas,
            "timeline_urgency": (
                "high"
                if "12" in str(current_grade)
                else "medium" if "11" in str(current_grade) else "low"
            ),
            "decision_pressure": (
                "immediate"
                if "12" in str(current_grade)
                else "upcoming" if "11" in str(current_grade) else "future_planning"
            ),
        }
