from typing import Dict, List, Any, Optional, TypedDict
from enum import Enum
from pydantic import BaseModel, Field
from dataclasses import dataclass


class AgentDependency:
    """Represents dependencies between agents"""

    def __init__(
        self,
        agent_id: str,
        depends_on: List[str] = None,
        required_outputs: List[str] = None,
    ):
        self.agent_id = agent_id
        self.depends_on = depends_on or []
        self.required_outputs = required_outputs or []


class AgentType(Enum):
    """Types of agents in the system"""

    VERTICAL_SPECIFIC = "vertical_specific"
    SHARED = "shared"
    UTILITY = "utility"


class ProcessingStatus(Enum):
    """Status of agent processing"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AgentResult:
    """Standardized result structure for all agents"""

    agent_id: str
    agent_name: str
    status: ProcessingStatus
    output_data: Dict[str, Any]
    confidence_score: float  # 0.0 to 1.0
    processing_time: float  # in seconds
    error_message: Optional[str] = None
    warnings: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}


class AgentInput(TypedDict):
    """Standardized input structure for agents"""

    user_data: Dict[str, Any]
    conversation_context: Dict[str, Any]
    previous_agent_outputs: Dict[str, AgentResult]
    session_metadata: Dict[str, Any]


class FleetExecutionStrategy(Enum):
    """Execution strategies for agent fleets"""

    SEQUENTIAL = "sequential"  # Execute agents one by one in order
    PARALLEL = "parallel"  # Execute independent agents in parallel
    CONDITIONAL = "conditional"  # Execute based on conditions/dependencies
    ADAPTIVE = "adaptive"  # Adapt execution based on intermediate results


class FleetStatus(Enum):
    """Status of fleet execution"""

    INITIALIZING = "initializing"
    EXECUTING = "executing"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    FAILED = "failed"


@dataclass
class FleetResult:
    """Result from fleet execution"""

    fleet_id: str
    fleet_name: str
    status: FleetStatus
    agent_results: Dict[str, AgentResult]
    execution_summary: Dict[str, Any]
    overall_confidence: float
    total_processing_time: float
    recommendations: List[str]
    next_actions: List[str]
    metadata: Dict[str, Any]


# Structured output models for each input processing
class ResumeAnalysis(BaseModel):
    """Structured analysis of resume data"""

    personal_summary: str = Field(description="Brief professional summary")
    technical_skills: List[str] = Field(
        description="List of technical skills extracted"
    )
    soft_skills: List[str] = Field(description="List of soft skills identified")
    education_highlights: List[Dict[str, str]] = Field(
        description="Key education details"
    )
    experience_summary: str = Field(description="Summary of work/internship experience")
    achievements: List[str] = Field(
        description="Notable achievements and accomplishments"
    )
    career_trajectory: str = Field(description="Observed career direction/interests")
    strengths: List[str] = Field(description="Key professional strengths")
    areas_for_improvement: List[str] = Field(description="Areas that could be enhanced")
    completeness_score: float = Field(description="Resume completeness score (0-1)")


class LinkedInAnalysis(BaseModel):
    """Structured analysis of LinkedIn profile"""

    professional_network_strength: str = Field(
        description="Assessment of network size and quality"
    )
    content_engagement: str = Field(
        description="Level of professional content creation/sharing"
    )
    industry_connections: List[str] = Field(
        description="Industries represented in network"
    )
    professional_presence_score: float = Field(
        description="Overall professional presence (0-1)"
    )
    profile_completeness: str = Field(description="Assessment of profile completeness")
    networking_opportunities: List[str] = Field(
        description="Suggested networking improvements"
    )
    visibility_enhancement: List[str] = Field(
        description="Ways to improve professional visibility"
    )


class GitHubAnalysis(BaseModel):
    """Structured analysis of GitHub profile"""

    technical_proficiency: Dict[str, str] = Field(
        description="Programming languages and proficiency levels"
    )
    project_quality_assessment: str = Field(
        description="Overall quality of repositories"
    )
    contribution_consistency: str = Field(
        description="Frequency and consistency of contributions"
    )
    collaboration_evidence: str = Field(
        description="Evidence of collaborative development"
    )
    portfolio_strength: str = Field(description="Strength of technical portfolio")
    recommended_improvements: List[str] = Field(
        description="Suggestions for GitHub improvement"
    )
    standout_projects: List[str] = Field(description="Most impressive projects")
    technical_depth_score: float = Field(description="Technical depth assessment (0-1)")


class AcademicAnalysis(BaseModel):
    """Structured analysis of academic status"""

    academic_performance: str = Field(
        description="Assessment of grades and performance"
    )
    relevant_coursework: List[str] = Field(
        description="Courses relevant to career goals"
    )
    academic_trajectory: str = Field(description="Trend in academic performance")
    specialization_alignment: str = Field(
        description="How well specialization aligns with career goals"
    )
    academic_achievements: List[str] = Field(
        description="Notable academic accomplishments"
    )
    knowledge_gaps: List[str] = Field(
        description="Areas where additional learning is needed"
    )
    academic_strength_score: float = Field(description="Academic strength score (0-1)")


class ExperienceAnalysis(BaseModel):
    """Structured analysis of internship and project experience"""

    practical_skills_demonstrated: List[str] = Field(
        description="Skills shown through experience"
    )
    industry_exposure: List[str] = Field(description="Industries/sectors experienced")
    project_complexity_level: str = Field(
        description="Complexity level of projects undertaken"
    )
    leadership_evidence: List[str] = Field(
        description="Evidence of leadership or initiative"
    )
    real_world_application: str = Field(
        description="How well experience applies to career goals"
    )
    experience_gaps: List[str] = Field(description="Types of experience still needed")
    practical_readiness: str = Field(description="Assessment of job readiness")
    experience_strength_score: float = Field(
        description="Experience strength score (0-1)"
    )


class ProfileAnalysisResult(BaseModel):
    """Comprehensive profile analysis result"""

    overall_profile_strength: float = Field(
        description="Overall profile strength (0-1)"
    )
    career_readiness_score: float = Field(
        description="How ready the student is for their target career (0-1)"
    )
    profile_summary: str = Field(
        description="Executive summary of the student's profile"
    )
    key_strengths: List[str] = Field(description="Top 5 strengths of the profile")
    improvement_priorities: List[str] = Field(
        description="Top 5 areas needing improvement"
    )
    competitive_advantages: List[str] = Field(
        description="What makes this profile stand out"
    )
    risk_factors: List[str] = Field(description="Potential weaknesses in job market")
    profile_positioning: str = Field(
        description="How to position this profile to employers"
    )
    recommended_next_steps: List[str] = Field(
        description="Immediate actions to improve profile"
    )
    estimated_job_match_rate: float = Field(
        description="Estimated match rate for target positions (0-1)"
    )


class MarketIntelligenceOutput(BaseModel):
    """Output schema for Market Intelligence Agent"""

    industry_trends: Dict[str, Any] = Field(
        description="Current industry trends and growth areas"
    )
    skill_demand: Dict[str, Any] = Field(
        description="In-demand skills with demand levels"
    )
    salary_insights: Dict[str, Any] = Field(
        description="Salary ranges and compensation trends"
    )
    job_market_outlook: Dict[str, Any] = Field(
        description="Job market projections and opportunities"
    )
    geographic_insights: Dict[str, Any] = Field(
        description="Location-based market opportunities"
    )
    emerging_technologies: List[str] = Field(
        description="Emerging technologies and their impact"
    )
    market_recommendations: List[str] = Field(
        description="Strategic market recommendations"
    )


class SkillGapAnalysis(BaseModel):
    """Schema for skill gap analysis"""

    current_skills: Dict[str, str] = Field(
        description="Current skills with proficiency levels"
    )
    market_required_skills: Dict[str, str] = Field(
        description="Skills required by market with importance"
    )
    skill_gaps: Dict[str, str] = Field(
        description="Identified skill gaps with priority levels"
    )
    skill_overlap: List[str] = Field(
        description="Skills that align well with market demand"
    )
    gap_severity: str = Field(description="Overall assessment of skill gap severity")


class DevelopmentRoadmap(BaseModel):
    """Schema for skill development roadmap"""

    priority_skills: List[Dict[str, Any]] = Field(
        description="Skills prioritized for development"
    )
    learning_pathway: List[Dict[str, Any]] = Field(
        description="Structured learning path with timelines"
    )
    resource_recommendations: Dict[str, List[str]] = Field(
        description="Learning resources by skill category"
    )
    milestone_timeline: Dict[str, str] = Field(
        description="Key milestones with target dates"
    )
    validation_strategies: List[str] = Field(
        description="Ways to validate and demonstrate new skills"
    )


class SkillDevelopmentOutput(BaseModel):
    """Complete output schema for Skill Development Strategist Agent"""

    skill_gap_analysis: SkillGapAnalysis = Field(
        description="Detailed skill gap assessment"
    )
    development_roadmap: DevelopmentRoadmap = Field(
        description="Strategic skill development plan"
    )
    immediate_actions: List[str] = Field(description="Actions to start immediately")
    long_term_strategy: List[str] = Field(
        description="Long-term skill building strategy"
    )
    portfolio_projects: List[Dict[str, Any]] = Field(
        description="Suggested projects to build skills"
    )
    certification_recommendations: List[Dict[str, Any]] = Field(
        description="Relevant certifications to pursue"
    )
    networking_opportunities: List[str] = Field(
        description="Skill-building networking opportunities"
    )


class CareerGoal(BaseModel):
    """Individual career goal with timeline and metrics"""

    goal_title: str = Field(description="Clear title of the career goal")
    description: str = Field(
        description="Detailed description of what needs to be achieved"
    )
    timeline: str = Field(description="Expected timeline for achievement")
    success_metrics: List[str] = Field(description="How to measure success")
    priority: str = Field(description="High/Medium/Low priority")
    dependencies: List[str] = Field(description="What needs to be done first")


class CareerStrategy(BaseModel):
    """Overall career strategy with actionable plans"""

    short_term_strategy: str = Field(description="6-month strategic approach")
    long_term_vision: str = Field(description="2-3 year career vision")
    key_differentiators: List[str] = Field(
        description="What will set the student apart"
    )
    risk_mitigation: List[str] = Field(description="How to handle potential setbacks")


class NetworkingPlan(BaseModel):
    """Professional networking strategy"""

    target_connections: List[str] = Field(
        description="Types of professionals to connect with"
    )
    networking_channels: List[str] = Field(description="Where and how to network")
    networking_goals: List[str] = Field(description="Specific networking objectives")
    follow_up_strategy: str = Field(
        description="How to maintain professional relationships"
    )


class JobSearchStrategy(BaseModel):
    """Job search and application strategy"""

    target_companies: List[str] = Field(description="Types of companies to target")
    application_timeline: str = Field(description="When to start applying and timeline")
    application_strategy: str = Field(description="How to approach applications")
    interview_preparation: List[str] = Field(
        description="Key interview preparation areas"
    )
    negotiation_strategy: str = Field(
        description="Approach for salary/offer negotiation"
    )


class PersonalBranding(BaseModel):
    """Personal branding and online presence strategy"""

    brand_positioning: str = Field(description="How to position professionally")
    content_strategy: List[str] = Field(description="What content to create/share")
    platform_optimization: Dict[str, str] = Field(
        description="How to optimize each platform"
    )
    thought_leadership_areas: List[str] = Field(
        description="Areas to build expertise visibility"
    )


class CareerOptimizationOutput(BaseModel):
    """Complete career optimization strategy output"""

    career_goals: List[CareerGoal] = Field(
        description="Structured career goals with timelines"
    )
    career_strategy: CareerStrategy = Field(description="Overall strategic approach")
    networking_plan: NetworkingPlan = Field(
        description="Professional networking strategy"
    )
    job_search_strategy: JobSearchStrategy = Field(
        description="Job search and application plan"
    )
    personal_branding: PersonalBranding = Field(
        description="Personal branding strategy"
    )
    monthly_action_plan: Dict[str, List[str]] = Field(
        description="Month-by-month action items"
    )
    success_tracking: Dict[str, str] = Field(description="KPIs and tracking methods")
    contingency_plans: List[str] = Field(description="Backup plans and alternatives")


class OpportunityMatchingOutput(BaseModel):
    """Output schema for opportunity matching analysis"""

    matched_opportunities: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of opportunities matched to student profile",
    )
    compatibility_analysis: Dict[str, Any] = Field(
        default_factory=dict,
        description="Analysis of student-opportunity compatibility",
    )
    application_strategy: Dict[str, Any] = Field(
        default_factory=dict,
        description="Customized application strategy for each opportunity",
    )
    success_probability: Dict[str, Any] = Field(
        default_factory=dict,
        description="Success probability assessment for different opportunities",
    )
    preparation_requirements: Dict[str, Any] = Field(
        default_factory=dict,
        description="Skills and preparation needed for each opportunity",
    )
    alternative_pathways: Dict[str, Any] = Field(
        default_factory=dict, description="Alternative routes to target opportunities"
    )
    networking_strategy: Dict[str, Any] = Field(
        default_factory=dict, description="Networking approach for opportunity access"
    )
