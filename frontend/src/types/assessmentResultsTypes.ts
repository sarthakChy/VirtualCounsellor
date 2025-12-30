export enum AssessmentStatus {
  COMPLETED = 'completed',
  FAILED = 'failed',
  PROCESSING = 'processing',
  PENDING = 'pending'
}

export enum PriorityLevel {
  HIGH = 'High',
  MEDIUM = 'Medium',
  LOW = 'Low'
}

export enum SkillLevel {
  ADVANCED = 'Advanced',
  INTERMEDIATE = 'Intermediate',
  BEGINNER = 'Beginner'
}

export enum IndustryDomain {
  TECHNOLOGY = 'Technology',
  FINANCE = 'Finance',
  HEALTHCARE = 'Healthcare',
  ECOMMERCE = 'E-commerce'
}

export enum JobType {
  FULL_TIME = 'Full-time',
  INTERNSHIP = 'Internship',
  CONTRACT = 'Contract'
}

export interface AssessmentResultsResponse {
  success: boolean;
  session_id: string;
  timestamp: string;
  data: {
    session_id: string;
    status: AssessmentStatus;
    updated_at: string;
    results: {
      success: boolean;
      vertical: string;
      session_id: string;
      timestamp: string;
      outputs: {
        fleet_summary: {
          status: AssessmentStatus;
          confidence: number;
          processing_time: number;
          recommendations: string[];
          next_actions: string[];
        };
        agent_outputs: Record<string, {
          status: AssessmentStatus;
          confidence: number;
          data: any;
        }>;
      };
    };
    error?: string;
  };
}
