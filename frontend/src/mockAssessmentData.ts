import {
  AssessmentStatus,
  PriorityLevel,
  SkillLevel,
  IndustryDomain,
  JobType,
} from './types/assessmentResultsTypes';
import type { AssessmentResultsResponse } from './types/assessmentResultsTypes';

export const createMockAssessmentData = (): AssessmentResultsResponse => {
  const sessionId = `session_${Date.now()}`;
  const timestamp = new Date().toISOString();

  return {
    success: true,
    session_id: sessionId,
    timestamp,
    data: {
      session_id: sessionId,
      status: AssessmentStatus.COMPLETED,
      updated_at: timestamp,
      results: {
        success: true,
        vertical: 'college-upskilling',
        session_id: sessionId,
        timestamp,
        outputs: {
          fleet_summary: {
            status: AssessmentStatus.COMPLETED,
            confidence: 0.87,
            processing_time: 45.2,
            recommendations: [
              'Focus on developing advanced Python and machine learning skills',
              'Build a strong portfolio with 3-4 data engineering projects',
              'Obtain AWS or Google Cloud certifications',
              'Strengthen your LinkedIn presence and network with data professionals',
              'Practice coding interviews and system design questions'
            ],
            next_actions: [
              'Complete AWS Data Engineer certification within 3 months',
              'Build an end-to-end data pipeline project using Apache Airflow',
              'Update LinkedIn profile with recent projects and skills',
              'Apply to 5 data engineer positions at target companies',
              'Schedule informational interviews with data engineers'
            ]
          },
          agent_outputs: {
            profile_analysis: {
              status: AssessmentStatus.COMPLETED,
              confidence: 0.85,
              data: {
                comprehensive_analysis: {
                  overall_profile_strength: 0.78,
                  career_readiness_score: 0.72,
                  profile_summary: 'Strong technical foundation with AI/ML specialization. Good academic performance and relevant project experience. LinkedIn and GitHub profiles show consistent activity but need optimization for data engineering roles.',
                  key_strengths: [
                    'Strong academic performance (9.5/10 GPA)',
                    'Relevant AI/ML specialization',
                    'Active GitHub profile with data science projects',
                    'Clear career transition goals',
                    'Good technical foundation in Python and machine learning'
                  ],
                  improvement_priorities: [
                    'Develop data engineering specific skills (Apache Spark, Kafka, Airflow)',
                    'Build cloud platform expertise (AWS/GCP)',
                    'Create more data pipeline focused projects',
                    'Strengthen system design knowledge',
                    'Improve professional networking'
                  ],
                  competitive_advantages: [
                    'Strong analytical and problem-solving skills',
                    'Academic excellence in relevant field',
                    'Demonstrated interest in data through projects',
                    'Clear career direction and motivation'
                  ],
                  risk_factors: [
                    'Limited production-level data engineering experience',
                    'Gap between current ML focus and data engineering requirements',
                    'Need for more industry-relevant project portfolio'
                  ],
                  profile_positioning: 'Emerging data professional with strong analytical foundation seeking transition from AI/ML to data engineering',
                  recommended_next_steps: [
                    'Complete data engineering certification',
                    'Build end-to-end data pipeline projects',
                    'Gain cloud platform experience',
                    'Network with data engineering professionals',
                    'Apply to junior data engineer positions'
                  ],
                  estimated_job_match_rate: 0.68
                },
                individual_analyses: {
                  resume: {
                    personal_summary: 'Final year B.Tech student with AI/ML specialization seeking data engineer role',
                    technical_skills: [
                      'Python', 'Machine Learning', 'Data Analysis', 'SQL', 'Pandas', 'NumPy', 'Scikit-learn'
                    ],
                    soft_skills: [
                      'Problem Solving', 'Analytical Thinking', 'Communication', 'Team Collaboration'
                    ],
                    education_highlights: [
                      {
                        Institution: 'Indian Institute of Technology',
                        Degree: 'B.Tech Computer Science',
                        CGPA: '9.5/10',
                        'Graduation Year': '2024'
                      }
                    ],
                    experience_summary: 'Academic projects and internships focused on AI/ML applications',
                    achievements: [
                      'Maintained 9.5/10 GPA throughout academic career',
                      'Completed multiple data science projects',
                      'Active contributor to open-source projects'
                    ],
                    career_trajectory: 'Transitioning from AI/ML academic focus to data engineering career',
                    strengths: [
                      'Strong technical foundation',
                      'Excellent academic performance',
                      'Clear career goals'
                    ],
                    areas_for_improvement: [
                      'Limited industry experience',
                      'Need for data engineering specific skills',
                      'Lack of cloud platform experience'
                    ],
                    completeness_score: 0.75
                  },
                  linkedin: {
                    professional_network_strength: 'Moderate - needs expansion in data engineering domain',
                    content_engagement: 'Low - limited professional content sharing',
                    industry_connections: ['Technology', 'Education', 'Data Science'],
                    professional_presence_score: 0.65,
                    profile_completeness: 0.80,
                    networking_opportunities: [
                      'Connect with data engineers at target companies',
                      'Join data engineering LinkedIn groups',
                      'Share data engineering project updates'
                    ],
                    visibility_enhancement: [
                      'Post about data engineering learning journey',
                      'Share insights from projects',
                      'Engage with data engineering content'
                    ]
                  },
                  github: {
                    technical_proficiency: {
                      'Python': SkillLevel.ADVANCED,
                      'Machine Learning': SkillLevel.INTERMEDIATE,
                      'Data Analysis': SkillLevel.INTERMEDIATE,
                      'SQL': SkillLevel.BEGINNER,
                      'Cloud Platforms': SkillLevel.BEGINNER
                    },
                    project_quality_assessment: 'Good quality projects with clear documentation',
                    contribution_consistency: 'Regular contributions over past year',
                    collaboration_evidence: 'Limited collaborative projects',
                    portfolio_strength: 'Strong in ML/AI, needs data engineering projects',
                    recommended_improvements: [
                      'Add data pipeline projects',
                      'Include cloud deployment examples',
                      'Create ETL process demonstrations',
                      'Add system design documentation'
                    ],
                    standout_projects: [
                      'ML model for predictive analytics',
                      'Data visualization dashboard',
                      'Kaggle competition solutions'
                    ],
                    technical_depth_score: 0.72
                  },
                  academic: {
                    academic_performance: 'Excellent - 9.5/10 GPA with consistent high performance',
                    relevant_coursework: [
                      'Data Structures and Algorithms',
                      'Database Management Systems',
                      'Machine Learning',
                      'Artificial Intelligence',
                      'Computer Networks',
                      'Software Engineering'
                    ],
                    academic_trajectory: 'Consistent excellence with focus on AI/ML specialization',
                    specialization_alignment: 'Strong foundation, needs data engineering focus',
                    academic_achievements: [
                      'Dean\'s List for 6 consecutive semesters',
                      'Best Project Award in AI/ML course',
                      'Research publication in conference'
                    ],
                    knowledge_gaps: [
                      'Distributed systems',
                      'Data warehousing',
                      'Stream processing',
                      'Cloud architecture'
                    ],
                    academic_strength_score: 0.90
                  }
                },
                analysis_metadata: {
                  analyzed_components: ['Resume', 'LinkedIn', 'GitHub', 'Academic Records'],
                  missing_components: ['Professional References', 'Certifications'],
                  analysis_timestamp: timestamp,
                  data_sources_count: 4
                },
                recommendations_summary: {
                  immediate_actions: [
                    'Update LinkedIn profile for data engineering focus',
                    'Create data pipeline project on GitHub',
                    'Start AWS/GCP certification course'
                  ],
                  profile_improvements: [
                    'Add data engineering keywords to profiles',
                    'Showcase relevant technical skills',
                    'Highlight transferable experience'
                  ],
                  competitive_positioning: 'Position as emerging data engineer with strong analytical foundation'
                }
              }
            },
            market_intelligence: {
              status: AssessmentStatus.COMPLETED,
              confidence: 0.82,
              data: {
                industry_trends: {
                  'Data Engineering': 'High demand with 25% year-over-year growth',
                  'Cloud Computing': 'Essential skill with 90% of companies adopting cloud',
                  'Real-time Analytics': 'Growing importance in business decision making',
                  'MLOps': 'Emerging field bridging ML and data engineering'
                },
                skill_demand: {
                  'Technical Skills': {
                    'Python': 'Very High - 85% of job postings',
                    'SQL': 'Very High - 90% of job postings',
                    'Apache Spark': 'High - 65% of job postings',
                    'AWS/GCP': 'High - 70% of job postings',
                    'Docker/Kubernetes': 'Medium - 45% of job postings'
                  },
                  'Soft Skills': {
                    'Problem Solving': 'Critical for troubleshooting data issues',
                    'Communication': 'Important for stakeholder interaction',
                    'Project Management': 'Valuable for leading data initiatives'
                  }
                },
                salary_insights: {
                  'Entry Level': {
                    'India': '₹6-12 LPA',
                    'US': '$70,000-$95,000',
                    'Growth Potential': '15-20% annually'
                  },
                  'Mid Level': {
                    'India': '₹12-25 LPA',
                    'US': '$95,000-$130,000',
                    'Growth Potential': '10-15% annually'
                  }
                },
                job_market_outlook: {
                  'Overall Demand': 'Very Strong - 35% growth expected by 2026',
                  'Competition Level': 'Moderate - Good opportunities for skilled candidates',
                  'Remote Opportunities': 'High - 60% of positions offer remote work',
                  'Industry Hotspots': 'Technology, Finance, Healthcare, E-commerce'
                },
                geographic_insights: {
                  'India': 'Bangalore, Hyderabad, Pune are top markets',
                  'US': 'San Francisco, Seattle, New York lead in opportunities',
                  'Remote': 'Increasing acceptance of remote data engineers'
                },
                emerging_technologies: [
                  'Apache Iceberg for data lakes',
                  'dbt for data transformation',
                  'Snowflake for cloud data warehousing',
                  'Apache Kafka for streaming',
                  'Terraform for infrastructure as code'
                ],
                market_recommendations: [
                  'Focus on cloud-native data engineering skills',
                  'Learn modern data stack tools (dbt, Airflow, Snowflake)',
                  'Develop expertise in both batch and streaming processing',
                  'Understand data governance and security principles',
                  'Build experience with infrastructure as code'
                ],
                domain_selection_reasoning: {
                  identified_domains: [IndustryDomain.TECHNOLOGY],
                  domain_explanations: {
                    [IndustryDomain.TECHNOLOGY]: {
                      relevance_score: 0.95,
                      reasoning: 'Strong technical background and AI/ML specialization align perfectly with technology sector data engineering roles'
                    }
                  },
                  overall_strategy: 'Focus on technology companies with strong data engineering teams',
                  extraction_confidence: 0.88
                },
                analysis_metadata: {
                  analysis_date: timestamp,
                  domains_analyzed: 'Technology, Finance, Healthcare',
                  domain_extraction_method: 'Profile analysis and career goals assessment',
                  geographic_scope: 'India and US markets',
                  data_sources: ['Job boards', 'Salary surveys', 'Industry reports'],
                  confidence_factors: {
                    'market_data_recency': 0.90,
                    'sample_size': 0.85,
                    'geographic_coverage': 0.80
                  }
                }
              }
            },
            skill_development_strategist: {
              status: AssessmentStatus.COMPLETED,
              confidence: 0.88,
              data: {
                skill_gap_analysis: {
                  current_skills: {
                    'Python': SkillLevel.ADVANCED,
                    'Machine Learning': SkillLevel.INTERMEDIATE,
                    'SQL': SkillLevel.BEGINNER,
                    'Data Analysis': SkillLevel.INTERMEDIATE,
                    'Git': SkillLevel.INTERMEDIATE
                  },
                  market_required_skills: {
                    'Apache Spark': 'Essential for big data processing',
                    'Apache Airflow': 'Critical for workflow orchestration',
                    'AWS/GCP': 'Required for cloud data engineering',
                    'Docker': 'Important for containerization',
                    'Kafka': 'Needed for streaming data'
                  },
                  skill_gaps: {
                    'Cloud Platforms': 'High priority - essential for modern data engineering',
                    'Data Pipeline Tools': 'High priority - core requirement',
                    'Distributed Computing': 'Medium priority - important for scalability',
                    'DevOps': 'Medium priority - valuable for deployment'
                  },
                  skill_overlap: [
                    'Python programming',
                    'Data analysis fundamentals',
                    'Problem-solving approach'
                  ],
                  gap_severity: 'Moderate - addressable with focused learning'
                },
                development_roadmap: {
                  priority_skills: [
                    {
                      skill: 'AWS Data Engineering',
                      reason: 'Most in-demand cloud platform for data engineering',
                      priority: PriorityLevel.HIGH
                    },
                    {
                      skill: 'Apache Airflow',
                      reason: 'Industry standard for workflow orchestration',
                      priority: PriorityLevel.HIGH
                    },
                    {
                      skill: 'Apache Spark',
                      reason: 'Essential for big data processing',
                      priority: PriorityLevel.HIGH
                    },
                    {
                      skill: 'Docker & Kubernetes',
                      reason: 'Important for containerized deployments',
                      priority: PriorityLevel.MEDIUM
                    }
                  ],
                  learning_pathway: [
                    {
                      stage: 'Foundation (Month 1-2)',
                      duration: '8 weeks',
                      focus: 'Cloud fundamentals and SQL mastery'
                    },
                    {
                      stage: 'Core Skills (Month 3-4)',
                      duration: '8 weeks',
                      focus: 'Data pipeline tools and distributed computing'
                    },
                    {
                      stage: 'Advanced (Month 5-6)',
                      duration: '8 weeks',
                      focus: 'System design and production deployment'
                    }
                  ],
                  resource_recommendations: {
                    'Online Courses': [
                      'AWS Certified Data Engineer - Associate',
                      'Apache Airflow Complete Course',
                      'Spark and Python for Big Data'
                    ],
                    'Books': [
                      'Designing Data-Intensive Applications',
                      'Data Engineering with Python',
                      'Learning Spark 2.0'
                    ],
                    'Practice Platforms': [
                      'AWS Free Tier',
                      'Databricks Community Edition',
                      'Google Colab for Spark'
                    ]
                  },
                  milestone_timeline: {
                    'Month 1': 'Complete AWS fundamentals and advanced SQL',
                    'Month 2': 'Build first data pipeline with Airflow',
                    'Month 3': 'Deploy Spark application on cloud',
                    'Month 4': 'Complete end-to-end data engineering project',
                    'Month 5': 'Obtain AWS Data Engineer certification',
                    'Month 6': 'Build portfolio and start job applications'
                  },
                  validation_strategies: [
                    'Build and deploy real projects',
                    'Obtain industry certifications',
                    'Contribute to open-source projects',
                    'Present work in technical forums'
                  ]
                },
                immediate_actions: [
                  'Enroll in AWS Data Engineer certification course',
                  'Set up local Airflow development environment',
                  'Complete SQL advanced course on HackerRank',
                  'Start building first data pipeline project'
                ],
                long_term_strategy: [
                  'Become proficient in modern data stack',
                  'Develop expertise in both batch and streaming',
                  'Build reputation through open-source contributions',
                  'Establish thought leadership in data engineering'
                ],
                portfolio_projects: [
                  {
                    project: 'Real-time Data Pipeline',
                    technologies: ['Apache Kafka', 'Spark Streaming', 'AWS Kinesis'],
                    description: 'Build end-to-end streaming data pipeline for e-commerce analytics'
                  },
                  {
                    project: 'Data Lake Architecture',
                    technologies: ['AWS S3', 'Glue', 'Athena', 'dbt'],
                    description: 'Design and implement scalable data lake with automated ETL'
                  },
                  {
                    project: 'ML Pipeline Orchestration',
                    technologies: ['Airflow', 'MLflow', 'Docker', 'Kubernetes'],
                    description: 'Create automated ML pipeline with model deployment'
                  }
                ],
                certification_recommendations: [
                  {
                    certification: 'AWS Certified Data Engineer - Associate',
                    provider: 'Amazon Web Services',
                    reason: 'Industry-recognized cloud data engineering credential'
                  },
                  {
                    certification: 'Google Cloud Professional Data Engineer',
                    provider: 'Google Cloud',
                    reason: 'Alternative cloud platform certification'
                  },
                  {
                    certification: 'Databricks Certified Data Engineer',
                    provider: 'Databricks',
                    reason: 'Specialized in modern data engineering tools'
                  }
                ],
                networking_opportunities: [
                  'Join local data engineering meetups',
                  'Participate in data engineering conferences',
                  'Engage with data engineering communities online',
                  'Connect with professionals on LinkedIn'
                ],
                strategy_metadata: {
                  analysis_date: timestamp,
                  current_skills_analyzed: 8,
                  market_trends_considered: 15,
                  learning_timeline: '6 months intensive program',
                  confidence_factors: {
                    'skill_gap_accuracy': 0.85,
                    'market_alignment': 0.90,
                    'timeline_feasibility': 0.80
                  }
                }
              }
            },
            career_optimization_planner: {
              status: AssessmentStatus.COMPLETED,
              confidence: 0.84,
              data: {
                career_goals: [
                  {
                    goal_title: 'Secure Data Engineer Position',
                    description: 'Land a junior data engineer role at a top tech company within 6 months',
                    timeline: '6 months',
                    success_metrics: [
                      'Receive job offer from target company',
                      'Salary range ₹8-12 LPA',
                      'Role involves modern data stack'
                    ],
                    priority: PriorityLevel.HIGH,
                    dependencies: ['Complete certifications', 'Build portfolio', 'Network effectively']
                  },
                  {
                    goal_title: 'Build Technical Expertise',
                    description: 'Develop proficiency in cloud data engineering tools and practices',
                    timeline: '4 months',
                    success_metrics: [
                      'AWS certification obtained',
                      '3 portfolio projects completed',
                      'Contributions to open-source projects'
                    ],
                    priority: PriorityLevel.HIGH,
                    dependencies: ['Dedicated learning time', 'Hands-on practice']
                  }
                ],
                career_strategy: {
                  short_term_strategy: 'Focus on rapid skill development and portfolio building while actively networking and applying to positions',
                  long_term_vision: 'Become a senior data engineer with expertise in modern data architecture and team leadership',
                  key_differentiators: [
                    'Strong analytical background from AI/ML studies',
                    'Academic excellence demonstrating learning ability',
                    'Clear transition plan with concrete steps'
                  ],
                  risk_mitigation: [
                    'Apply to multiple companies to increase chances',
                    'Consider internships as stepping stones',
                    'Build network for referrals and opportunities'
                  ]
                },
                networking_plan: {
                  target_connections: [
                    'Data engineers at target companies',
                    'Hiring managers in data teams',
                    'Alumni working in data engineering',
                    'Data engineering influencers and thought leaders'
                  ],
                  networking_channels: [
                    'LinkedIn professional networking',
                    'Data engineering meetups and conferences',
                    'Online communities (Reddit, Stack Overflow)',
                    'University alumni networks'
                  ],
                  networking_goals: [
                    'Connect with 50 data professionals',
                    'Attend 2 industry events monthly',
                    'Engage meaningfully with 10 thought leaders'
                  ],
                  follow_up_strategy: 'Regular engagement with valuable content sharing and thoughtful comments'
                },
                job_search_strategy: {
                  target_companies: [
                    'Amazon', 'Google', 'Microsoft', 'Flipkart', 'Swiggy', 'Zomato',
                    'Paytm', 'PhonePe', 'Razorpay', 'Freshworks'
                  ],
                  application_timeline: 'Start applications after 3 months of skill development',
                  application_strategy: 'Quality over quantity - 5-10 well-researched applications per week',
                  interview_preparation: [
                    'Practice system design for data systems',
                    'Review SQL and Python coding questions',
                    'Prepare behavioral interview responses',
                    'Study company-specific data challenges'
                  ],
                  negotiation_strategy: 'Research market rates and highlight unique value proposition'
                },
                personal_branding: {
                  brand_positioning: 'Emerging data engineer with strong analytical foundation and passion for scalable data solutions',
                  content_strategy: [
                    'Share learning journey and project updates',
                    'Write technical blogs about data engineering concepts',
                    'Contribute to discussions in data communities'
                  ],
                  platform_optimization: {
                    'LinkedIn': 'Professional updates and industry engagement',
                    'GitHub': 'Showcase technical projects and contributions',
                    'Medium/Dev.to': 'Technical writing and thought leadership'
                  },
                  thought_leadership_areas: [
                    'Modern data stack adoption',
                    'Career transition from ML to data engineering',
                    'Best practices for data pipeline development'
                  ]
                },
                monthly_action_plan: {
                  'Month 1': [
                    'Complete AWS fundamentals course',
                    'Update LinkedIn profile for data engineering focus',
                    'Start building first data pipeline project',
                    'Join 3 data engineering LinkedIn groups'
                  ],
                  'Month 2': [
                    'Complete Airflow course and certification',
                    'Finish first portfolio project',
                    'Attend 2 data engineering meetups',
                    'Connect with 15 data professionals'
                  ],
                  'Month 3': [
                    'Complete AWS Data Engineer certification',
                    'Start second portfolio project',
                    'Begin job application preparation',
                    'Conduct 3 informational interviews'
                  ],
                  'Month 4': [
                    'Complete all portfolio projects',
                    'Start targeted job applications',
                    'Prepare for technical interviews',
                    'Expand professional network'
                  ]
                },
                success_tracking: {
                  'Skills Development': 'Track certification progress and project completion',
                  'Network Growth': 'Monitor LinkedIn connections and engagement',
                  'Job Applications': 'Track application response rates and interview conversion',
                  'Market Positioning': 'Measure profile views and recruiter outreach'
                },
                contingency_plans: [
                  'Consider data analyst roles as stepping stones',
                  'Look into internship opportunities for experience',
                  'Explore freelance data projects for portfolio building',
                  'Consider additional certifications if needed'
                ],
                optimization_metadata: {
                  analysis_date: timestamp,
                  planning_horizon: '6 months with 2-year vision',
                  strategy_components: ['Skills', 'Networking', 'Branding', 'Applications'],
                  personalization_level: 'High - tailored to individual profile',
                  implementation_complexity: 'Medium - requires dedicated effort',
                  success_probability: 0.75
                },
                implementation_timeline: {
                  'Week 1-2': ['Set up learning environment', 'Create study schedule'],
                  'Week 3-4': ['Begin AWS course', 'Update professional profiles'],
                  'Month 2': ['Complete first certification', 'Start networking'],
                  'Month 3': ['Build portfolio projects', 'Prepare applications'],
                  'Month 4-6': ['Active job search', 'Interview preparation']
                }
              }
            },
            opportunity_matcher: {
              status: AssessmentStatus.COMPLETED,
              confidence: 0.79,
              data: {
                matched_opportunities: [
                  {
                    opportunity_id: 'opp_001',
                    company: 'Amazon',
                    title: 'Data Engineer I',
                    location: 'Bangalore, India',
                    type: JobType.FULL_TIME,
                    description: 'Build and maintain data pipelines for Amazon\'s e-commerce platform using AWS services'
                  },
                  {
                    opportunity_id: 'opp_002',
                    company: 'Flipkart',
                    title: 'Junior Data Engineer',
                    location: 'Bangalore, India',
                    type: JobType.FULL_TIME,
                    description: 'Work on data infrastructure for India\'s largest e-commerce platform'
                  },
                  {
                    opportunity_id: 'opp_003',
                    company: 'Swiggy',
                    title: 'Data Engineer - Analytics',
                    location: 'Bangalore, India',
                    type: JobType.FULL_TIME,
                    description: 'Build data pipelines for food delivery analytics and business intelligence'
                  },
                  {
                    opportunity_id: 'opp_004',
                    company: 'Microsoft',
                    title: 'Data Engineer Intern',
                    location: 'Hyderabad, India',
                    type: JobType.INTERNSHIP,
                    description: 'Summer internship program for data engineering with Azure cloud services'
                  }
                ],
                compatibility_analysis: {
                  'Amazon Data Engineer I': '78% match - Strong technical fit, need cloud experience',
                  'Flipkart Junior Data Engineer': '82% match - Good cultural fit, relevant scale challenges',
                  'Swiggy Data Engineer': '75% match - Analytics focus aligns with ML background',
                  'Microsoft Intern': '85% match - Perfect for gaining experience and learning'
                },
                application_strategy: {
                  'Amazon': 'Emphasize AWS learning commitment and scalability interest',
                  'Flipkart': 'Highlight e-commerce analytics projects and Indian market understanding',
                  'Swiggy': 'Focus on real-time analytics and ML integration capabilities',
                  'Microsoft': 'Showcase academic excellence and learning agility'
                },
                success_probability: {
                  'Amazon Data Engineer I': '65% - Competitive but achievable with preparation',
                  'Flipkart Junior Data Engineer': '70% - Good fit for entry-level position',
                  'Swiggy Data Engineer': '60% - Need to demonstrate analytics expertise',
                  'Microsoft Intern': '80% - Strong academic profile advantage'
                },
                preparation_requirements: {
                  'Technical Skills': 'Complete AWS certification, build cloud projects',
                  'System Design': 'Study data system architecture and scalability',
                  'Behavioral': 'Prepare STAR method responses for leadership principles',
                  'Company Research': 'Understand each company\'s data challenges and culture'
                },
                alternative_pathways: {
                  description: 'Consider data analyst roles, consulting positions, or startup opportunities as alternative entry points'
                },
                networking_strategy: {
                  description: 'Connect with employees at target companies, attend their tech talks, and engage with their content'
                },
                matching_metadata: {
                  analysis_date: timestamp,
                  opportunities_analyzed: 50,
                  matching_criteria: ['Skills', 'Experience', 'Location', 'Company Culture'],
                  success_factors: ['Technical competency', 'Cultural fit', 'Growth potential'],
                  personalization_level: 'High - based on individual profile and preferences'
                },
                implementation_guidance: {
                  immediate_actions: [
                    'Research target companies thoroughly',
                    'Customize resume for each application',
                    'Prepare company-specific interview questions',
                    'Connect with employees on LinkedIn'
                  ],
                  weekly_tasks: [
                    'Apply to 2-3 positions',
                    'Follow up on previous applications',
                    'Practice interview questions',
                    'Engage with company content'
                  ],
                  monthly_goals: [
                    'Submit 8-10 quality applications',
                    'Complete 2-3 phone screenings',
                    'Attend 1-2 company events',
                    'Expand network by 20 connections'
                  ]
                }
              }
            }
          }
        }
      }
    }
  };
};