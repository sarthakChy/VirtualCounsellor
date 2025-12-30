import { AptitudeDomain, InterestDomain, AcademicStream, ScoreLevel, CollegeType, ScholarshipType, Grade, EntranceExam } from './types/schoolAssessmentTypes';

// Mock data for school assessment results
export const mockSchoolAssessmentData = {
  success: true,
  data: {
    session_id: "session_academic_9th",
    status: "completed" as const,
    updated_at: "2025-09-20T14:16:39.845632",
    results: {
      success: true,
      vertical: "school_students",
      session_id: "session_academic_9th", 
      timestamp: "2025-09-20T14:16:39.842636",
      outputs: {
        fleet_summary: {
          status: "completed" as const,
          confidence: 0.98,
          processing_time: 128.839095,
          recommendations: [
            "Discuss your assessment results with parents and school counselors",
            "Focus on developing your identified cognitive strengths",
            "Explore activities that align with your interest areas",
            "Carefully consider the recommended academic streams",
            "Research subject requirements and career implications for each stream"
          ],
          next_actions: [
            "Review the detailed analysis and recommendations", 
            "Ask follow-up questions for clarification",
            "Begin implementing suggested improvements"
          ]
        },
        agent_outputs: {
          test_score_interpreter: {
            status: "completed" as const,
            confidence: 0.95,
            data: {
              executive_summary: "Student demonstrates exceptional aptitude in several areas, particularly in verbal reasoning, spatial reasoning, and numerical abilities. A strong interest in scientific fields is evident, although this needs to be further explored to determine specific career paths.",
              aptitude_analysis: {
                [AptitudeDomain.VERBAL_REASONING]: "Exceptional verbal reasoning skills (10/10). This suggests a strong capacity for communication, critical thinking, and understanding complex information.",
                [AptitudeDomain.CLERICAL]: "Very high clerical aptitude (9/10) indicating strong organizational skills and attention to detail.",
                [AptitudeDomain.MATHEMATICAL_REASONING]: "Above-average mathematical reasoning skills (7/10). While not exceptional, this is a solid foundation for many STEM fields.",
                [AptitudeDomain.NUMERICAL_ABILITY]: "Above-average numerical ability (7/10), complementing mathematical reasoning skills.",
                [AptitudeDomain.ROTATIONAL_REASONING]: "Very high rotational reasoning skills (9/10). This suggests strong spatial reasoning abilities.",
                [AptitudeDomain.SPATIAL_REASONING]: "Exceptional spatial reasoning skills (10/10). This points towards a strong aptitude for visually-oriented tasks.",
                [AptitudeDomain.VERBAL_FLUENCY]: "Exceptional verbal fluency (10/10). This indicates a natural talent for clear and effective communication."
              },
              interest_analysis: {
                [InterestDomain.SCIENTIFIC]: "Very high interest in scientific fields (9/10). This is a strong motivational driver.",
                [InterestDomain.SOCIAL]: "Average interest in social fields (6/10). This suggests a potential interest in working with people.",
                [InterestDomain.CONVENTIONAL]: "Average interest in conventional fields (5/10). This indicates some interest in structured work environments.",
                [InterestDomain.ARTISTIC]: "Low average interest in artistic fields (4/10). This suggests that artistic pursuits are not a primary focus.",
                [InterestDomain.ENTERPRISING]: "Low average interest in enterprising fields (4/10). This suggests less interest in leadership roles.",
                [InterestDomain.REALISTIC]: "Below average interest in realistic fields (3/10). This suggests less interest in hands-on, practical work."
              },
              score_summaries: {
                dbda_top_aptitudes: [
                  {
                    domain: AptitudeDomain.VERBAL_REASONING,
                    score: 10,
                    level: ScoreLevel.VERY_HIGH,
                    description: "Exceptional verbal reasoning and communication skills"
                  },
                  {
                    domain: AptitudeDomain.SPATIAL_REASONING,
                    score: 10, 
                    level: ScoreLevel.VERY_HIGH,
                    description: "Outstanding spatial visualization and reasoning abilities"
                  },
                  {
                    domain: AptitudeDomain.VERBAL_FLUENCY,
                    score: 10,
                    level: ScoreLevel.VERY_HIGH,
                    description: "Excellent verbal fluency and expression"
                  }
                ],
                cii_top_interests: [
                  {
                    domain: InterestDomain.SCIENTIFIC,
                    score: 9,
                    level: ScoreLevel.VERY_HIGH,
                    description: "Strong passion for scientific fields and research"
                  },
                  {
                    domain: InterestDomain.SOCIAL,
                    score: 6,
                    level: ScoreLevel.AVERAGE,
                    description: "Moderate interest in social and people-oriented activities"
                  },
                  {
                    domain: InterestDomain.CONVENTIONAL,
                    score: 5,
                    level: ScoreLevel.AVERAGE,
                    description: "Some interest in structured and organized work"
                  }
                ]
              }
            }
          },
          academic_stream_advisor: {
            status: "completed" as const,
            confidence: 1.0,
            data: {
              executive_summary: "This student demonstrates exceptional aptitude in verbal and spatial reasoning, strong numerical abilities, and a high interest in scientific fields. The recommendations prioritize streams aligning with these strengths.",
              recommended_streams: [
                {
                  stream_type: AcademicStream.SCIENCE_PCMB,
                  suitability_score: 0.95,
                  primary_strengths_supporting: [
                    "Exceptional verbal reasoning (Ca: 10/10)",
                    "Exceptional spatial reasoning (Sa: 10/10)", 
                    "High rotational reasoning (Ra: 9/10)",
                    "Above-average mathematical reasoning (Ma: 7/10)",
                    "High interest in scientific fields (9/10)"
                  ],
                  career_pathways: [
                    "Engineering (various branches)",
                    "Medicine",
                    "Biotechnology",
                    "Research (various scientific fields)",
                    "Data Science"
                  ],
                  subject_requirements: [
                    "Physics",
                    "Chemistry", 
                    "Mathematics",
                    "Biology"
                  ]
                },
                {
                  stream_type: AcademicStream.SCIENCE_PCM,
                  suitability_score: 0.9,
                  primary_strengths_supporting: [
                    "Exceptional verbal reasoning (Ca: 10/10)",
                    "High rotational reasoning (Ra: 9/10)",
                    "Exceptional spatial reasoning (Sa: 10/10)",
                    "Above-average mathematical reasoning (Ma: 7/10)"
                  ],
                  career_pathways: [
                    "Engineering (various branches)",
                    "Computer Science",
                    "Technology",
                    "Data Science"
                  ],
                  subject_requirements: [
                    "Physics",
                    "Chemistry",
                    "Mathematics"
                  ]
                }
              ]
            }
          },
          career_pathway_explorer: {
            status: "completed" as const,
            confidence: 0.97,
            data: {
              executive_summary: "This student demonstrates exceptional aptitude in verbal and spatial reasoning, strong numerical abilities, and a high interest in scientific fields. The following recommendations prioritize careers aligning with these strengths.",
              recommended_career_pathways: [
                {
                  career_title: "Software Engineer",
                  career_field: "Computer Science & Engineering",
                  suitability_score: 0.9,
                  pathway_description: "Design, develop, and test software applications. Involves problem-solving, coding, and collaboration.",
                  educational_requirements: [
                    "Bachelor's degree in Computer Science or related field",
                    "Potential for further specialization (e.g., Masters, PhD)"
                  ],
                  entry_timeline: "4-6 years after 12th grade (Bachelor's degree)",
                  salary_outlook: {
                    entry_level: "₹4-8 Lakhs per annum",
                    mid_career: "₹10-20 Lakhs per annum",
                    senior: "₹20+ Lakhs per annum"
                  },
                  aptitude_alignment: [
                    "Exceptional spatial reasoning (Sa)",
                    "High rotational reasoning (Ra)",
                    "Above-average numerical ability (Na)"
                  ]
                },
                {
                  career_title: "Data Scientist",
                  career_field: "Data Science & Analytics", 
                  suitability_score: 0.85,
                  pathway_description: "Collect, analyze, and interpret large datasets to extract insights and solve business problems.",
                  educational_requirements: [
                    "Bachelor's degree in Statistics, Mathematics, Computer Science, or related field",
                    "Master's degree preferred for advanced roles"
                  ],
                  entry_timeline: "4-6 years after 12th grade (Bachelor's degree)",
                  salary_outlook: {
                    entry_level: "₹6-10 Lakhs per annum",
                    mid_career: "₹15-25 Lakhs per annum", 
                    senior: "₹25+ Lakhs per annum"
                  },
                  aptitude_alignment: [
                    "Above-average mathematical reasoning (Ma)",
                    "Above-average numerical ability (Na)",
                    "Exceptional verbal fluency (Va)"
                  ]
                },
                {
                  career_title: "Biomedical Engineer",
                  career_field: "Biomedical Engineering",
                  suitability_score: 0.8,
                  pathway_description: "Apply engineering principles to solve problems in biology and medicine. Develop medical devices, diagnostic tools, and therapies.",
                  educational_requirements: [
                    "Bachelor's degree in Biomedical Engineering or related field",
                    "Master's or PhD for research and development roles"
                  ],
                  entry_timeline: "4-6 years after 12th grade (Bachelor's degree)",
                  salary_outlook: {
                    entry_level: "₹5-9 Lakhs per annum",
                    mid_career: "₹12-22 Lakhs per annum",
                    senior: "₹22+ Lakhs per annum"
                  },
                  aptitude_alignment: [
                    "Exceptional spatial reasoning (Sa)",
                    "High rotational reasoning (Ra)",
                    "Above-average numerical ability (Na)"
                  ]
                }
              ]
            }
          },
          educational_roadmap_planner: {
            status: "completed" as const,
            confidence: 1.0,
            data: {
              executive_summary: "This roadmap outlines a comprehensive educational plan for a student with exceptional aptitude in verbal and spatial reasoning, strong numerical abilities, and a keen interest in scientific fields.",
              grade_wise_milestones: [
                {
                  grade: Grade.GRADE_10,
                  academic_focus: [
                    "Board exam preparation (CBSE/ICSE)",
                    "Stream selection (Science - PCM/PCMB)"
                  ],
                  subject_priorities: {
                    Mathematics: "Strong foundation, focus on problem-solving",
                    Science: "Conceptual understanding, practical application",
                    English: "Improve writing and comprehension skills"
                  },
                  entrance_exam_preparation: [
                    "Begin introductory JEE/NEET preparation (basic concepts)",
                    "Explore online resources and sample papers"
                  ]
                },
                {
                  grade: Grade.GRADE_11,
                  academic_focus: [
                    "Stream specialization (PCM or PCMB)",
                    "Foundation for entrance exams (JEE/NEET/other relevant exams)"
                  ],
                  subject_priorities: {
                    Mathematics: "Advanced concepts, problem-solving practice",
                    Physics: "Conceptual clarity, problem-solving",
                    Chemistry: "Conceptual understanding, practical experiments",
                    Biology: "In-depth understanding, practical application (if PCMB)"
                  },
                  entrance_exam_preparation: [
                    "Structured JEE/NEET preparation (begin intensive study)",
                    "Join coaching classes (if needed and feasible)",
                    "Regular mock tests and performance analysis"
                  ]
                },
                {
                  grade: Grade.GRADE_12,
                  academic_focus: [
                    "Board exams",
                    "Intensive entrance exam preparation"
                  ],
                  subject_priorities: {
                    "All Subjects": "Thorough revision and practice"
                  },
                  entrance_exam_preparation: [
                    "Intensive JEE/NEET/other relevant exam preparation",
                    "Regular mock tests and performance analysis",
                    "Focus on weak areas",
                    "Refine exam strategies"
                  ]
                }
              ],
              entrance_exam_strategies: [
                {
                  exam_name: EntranceExam.JEE_MAIN,
                  preparation_timeline: "Begin foundation in Grade 11, intensive preparation in Grade 12",
                  subject_priorities: ["Mathematics", "Physics", "Chemistry"],
                  difficulty_assessment: "Highly competitive, requires dedicated effort and strategic preparation."
                },
                {
                  exam_name: EntranceExam.NEET,
                  preparation_timeline: "Begin foundation in Grade 11, intensive preparation in Grade 12", 
                  subject_priorities: ["Biology", "Chemistry", "Physics"],
                  difficulty_assessment: "Highly competitive, requires dedicated effort and strategic preparation."
                }
              ]
            }
          },
          college_scholarship_navigator: {
            status: "completed" as const,
            confidence: 1.0,
            data: {
              executive_summary: "This plan outlines a cost-effective pathway for a Grade 12 student aiming for a Software Engineering career, considering their strong aptitude in science and technology.",
              recommended_colleges: [
                {
                  college_name: "Indian Institute of Technology (IIT) Delhi",
                  college_type: CollegeType.IIT,
                  location: "Delhi, India",
                  programs_offered: ["B.Tech in Computer Science and Engineering"],
                  admission_requirements: {
                    entrance_exam: "JEE Advanced",
                    requirement: "Top percentile required"
                  },
                  fees_structure: {
                    tuition: "₹2-3 Lakhs per annum",
                    hostel: "₹50,000-1 Lakh per annum",
                    living_expenses: "₹1-2 Lakhs per annum"
                  },
                  placement_statistics: {
                    average_salary: "₹15-25 Lakhs per annum",
                    placement_rate: "95%+"
                  },
                  suitability_score: 0.8
                },
                {
                  college_name: "Indian Institute of Information Technology (IIIT) Hyderabad",
                  college_type: CollegeType.IIIT,
                  location: "Hyderabad, India",
                  programs_offered: ["B.Tech in Computer Science and Engineering"],
                  admission_requirements: {
                    entrance_exam: "IIIT-H entrance exam or JEE Main score",
                    requirement: "Good percentage in PCM"
                  },
                  fees_structure: {
                    tuition: "₹3-4 Lakhs per annum",
                    hostel: "₹80,000-1.2 Lakhs per annum",
                    living_expenses: "₹1-1.5 Lakhs per annum"
                  },
                  placement_statistics: {
                    average_salary: "₹12-20 Lakhs per annum",
                    placement_rate: "90%+"
                  },
                  suitability_score: 0.7
                },
                {
                  college_name: "BITS Pilani",
                  college_type: CollegeType.PRIVATE,
                  location: "Pilani, Rajasthan, India",
                  programs_offered: ["B.E. in Computer Science"],
                  admission_requirements: {
                    entrance_exam: "BITS Admission Test (BITSAT)",
                    requirement: "Good percentage in PCM"
                  },
                  fees_structure: {
                    tuition: "₹4-5 Lakhs per annum",
                    hostel: "₹1-1.5 Lakhs per annum",
                    living_expenses: "₹1-1.5 Lakhs per annum"
                  },
                  placement_statistics: {
                    average_salary: "₹10-18 Lakhs per annum",
                    placement_rate: "85%+"
                  },
                  suitability_score: 0.65
                }
              ],
              scholarship_opportunities: [
                {
                  scholarship_name: "Merit-cum-Means Scholarships (IITs/NITs)",
                  provider: "Institutes",
                  scholarship_type: ScholarshipType.MERIT_BASED,
                  eligibility_criteria: [
                    "High academic performance",
                    "Financial need"
                  ],
                  benefit_amount: "₹50,000-2,00,000 per annum",
                  application_process: ["Apply during college application"],
                  compatibility_score: 0.9
                },
                {
                  scholarship_name: "Government Scholarships (Central/State)",
                  provider: "Government",
                  scholarship_type: ScholarshipType.GOVERNMENT,
                  eligibility_criteria: [
                    "Income criteria",
                    "Caste/community criteria (for reserved categories)"
                  ],
                  benefit_amount: "₹20,000-1,00,000 per annum",
                  application_process: ["Apply through designated portals"],
                  compatibility_score: 0.7
                }
              ]
            }
          }
        }
      }
    }
  }
};