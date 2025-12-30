export enum QuestionType {
  MULTIPLE_CHOICE = 'multiple_choice',
  SAME_DIFFERENT = 'same_different'
}

export enum AssessmentSection {
  VERBAL_SYNONYMS = 'verbal_synonyms',
  VERBAL_PROVERBS = 'verbal_proverbs', 
  NUMERICAL = 'numerical',
  MECHANICAL = 'mechanical',
  CLERICAL = 'clerical',
  REASONING = 'reasoning'
}

export enum AnswerOption {
  A = 'a',
  B = 'b', 
  C = 'c',
  D = 'd',
  E = 'e'
}

export enum SameDifferentOption {
  SAME = 'same',
  DIFFERENT = 'different'
}

export enum AptitudeDomain {
  VERBAL_REASONING = 'verbal_reasoning',
  CLERICAL = 'clerical',
  MATHEMATICAL_REASONING = 'mathematical_reasoning',
  NUMERICAL_ABILITY = 'numerical_ability',
  ROTATIONAL_REASONING = 'rotational_reasoning',
  SPATIAL_REASONING = 'spatial_reasoning',
  VERBAL_FLUENCY = 'verbal_fluency'
}

export enum InterestDomain {
  SCIENTIFIC = 'scientific',
  SOCIAL = 'social',
  CONVENTIONAL = 'conventional',
  ARTISTIC = 'artistic',
  ENTERPRISING = 'enterprising',
  REALISTIC = 'realistic'
}

export enum AcademicStream {
  SCIENCE_PCMB = 'Science (PCMB)',
  SCIENCE_PCM = 'Science (PCM)',
  SCIENCE_PCB = 'Science (PCB)',
  COMMERCE = 'Commerce',
  ARTS = 'Arts'
}

export enum ScoreLevel {
  VERY_HIGH = 'Very High',
  HIGH = 'High',
  AVERAGE = 'Average',
  LOW = 'Low'
}

export enum CollegeType {
  IIT = 'IIT',
  IIIT = 'IIIT',
  NIT = 'NIT',
  PRIVATE = 'Private',
  GOVERNMENT = 'Government'
}

export enum ScholarshipType {
  MERIT_BASED = 'Merit-based',
  NEED_BASED = 'Need-based',
  GOVERNMENT = 'Government'
}

export enum Grade {
  GRADE_9 = 'Grade 9',
  GRADE_10 = 'Grade 10',
  GRADE_11 = 'Grade 11',
  GRADE_12 = 'Grade 12'
}

export enum EntranceExam {
  JEE_MAIN = 'JEE Main',
  JEE_ADVANCED = 'JEE Advanced',
  NEET = 'NEET',
  BITSAT = 'BITSAT'
}

// Basic Information Form Data
export interface BasicInfoFormData {
  studentName: string;
  currentGrade: string;
  currentStream: string;
  subjects: string[];
  academicPerformance: string;
  interests: string[];
  careerAspirations: string;
  parentContact: string;
  additionalInfo: string;
}

// Form validation errors
export interface BasicInfoFormErrors {
  studentName?: string;
  currentGrade?: string;
  currentStream?: string;
  subjects?: string;
  academicPerformance?: string;
  interests?: string;
  careerAspirations?: string;
  parentContact?: string;
}

// Assessment question types
export interface AssessmentOption {
  value: AnswerOption | SameDifferentOption;
  label: string;
}

export interface AssessmentQuestion {
  id: string;
  question: string;
  type?: QuestionType;
  options: AssessmentOption[];
  correctAnswer: AnswerOption | SameDifferentOption;
}

export interface AssessmentFormData {
  [AssessmentSection.VERBAL_SYNONYMS]: Record<string, AnswerOption>;
  [AssessmentSection.VERBAL_PROVERBS]: Record<string, AnswerOption>;
  [AssessmentSection.NUMERICAL]: Record<string, AnswerOption>;
  [AssessmentSection.MECHANICAL]: Record<string, AnswerOption>;
  [AssessmentSection.CLERICAL]: Record<string, SameDifferentOption>;
  [AssessmentSection.REASONING]: Record<string, AnswerOption>;
}

export interface AssessmentState {
  currentStep: 'basic-info' | 'assessment';
  currentSection: AssessmentSection;
  answers: AssessmentFormData;
  basicInfoData: BasicInfoFormData;
  basicInfoComplete: boolean;
  isComplete: boolean;
  sectionProgress: Record<AssessmentSection, boolean>;
}
