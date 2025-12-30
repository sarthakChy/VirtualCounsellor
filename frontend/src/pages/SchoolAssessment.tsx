import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  ArrowLeft, 
  Clock, 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle2
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import BasicInfoForm from '../components/school-assessment/BasicInfoForm';
import { 
  AssessmentSection as AssessmentSectionEnum, 
  AnswerOption,
  SameDifferentOption
} from '../types/schoolAssessmentTypes';
import type { 
  AssessmentState, 
  BasicInfoFormData, 
  BasicInfoFormErrors,
  AssessmentFormData
} from '../types/schoolAssessmentTypes';
import { mockAssessmentQuestions } from '../schoolAssessmentQuestions';

const initialFormData: AssessmentFormData = {
  [AssessmentSectionEnum.VERBAL_SYNONYMS]: {},
  [AssessmentSectionEnum.VERBAL_PROVERBS]: {},
  [AssessmentSectionEnum.NUMERICAL]: {},
  [AssessmentSectionEnum.MECHANICAL]: {},
  [AssessmentSectionEnum.CLERICAL]: {},
  [AssessmentSectionEnum.REASONING]: {}
};

const initialBasicInfoData: BasicInfoFormData = {
  studentName: '',
  currentGrade: '',
  currentStream: '',
  subjects: [],
  academicPerformance: '',
  interests: [],
  careerAspirations: '',
  parentContact: '',
  additionalInfo: ''
};

const SchoolAssessment = () => {
  const navigate = useNavigate();
  const [assessmentState, setAssessmentState] = useState<AssessmentState>({
    currentStep: 'basic-info',
    currentSection: AssessmentSectionEnum.VERBAL_SYNONYMS,
    answers: initialFormData,
    basicInfoData: initialBasicInfoData,
    basicInfoComplete: false,
    isComplete: false,
    sectionProgress: {
      [AssessmentSectionEnum.VERBAL_SYNONYMS]: false,
      [AssessmentSectionEnum.VERBAL_PROVERBS]: false,
      [AssessmentSectionEnum.NUMERICAL]: false,
      [AssessmentSectionEnum.MECHANICAL]: false,
      [AssessmentSectionEnum.CLERICAL]: false,
      [AssessmentSectionEnum.REASONING]: false
    }
  });

  const [basicInfoErrors, setBasicInfoErrors] = useState<BasicInfoFormErrors>({});
  const [activeQuestionIndex, setActiveQuestionIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(45 * 60); // 45 minutes

  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    if (assessmentState.currentStep === 'assessment' && !assessmentState.isComplete && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [assessmentState.currentStep, assessmentState.isComplete, timeLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Section order
  const sectionOrder = [
    AssessmentSectionEnum.VERBAL_SYNONYMS,
    AssessmentSectionEnum.VERBAL_PROVERBS,
    AssessmentSectionEnum.NUMERICAL,
    AssessmentSectionEnum.MECHANICAL,
    AssessmentSectionEnum.CLERICAL,
    AssessmentSectionEnum.REASONING
  ];

  const validateBasicInfo = (): boolean => {
    const errors: BasicInfoFormErrors = {};
    const { basicInfoData } = assessmentState;

    if (!basicInfoData.studentName) errors.studentName = 'Name is required';
    if (!basicInfoData.currentGrade) errors.currentGrade = 'Grade is required';
    if (basicInfoData.subjects.length === 0) errors.subjects = 'At least one subject is required';
    if (!basicInfoData.parentContact) errors.parentContact = 'Parent contact is required';

    setBasicInfoErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleBasicInfoChange = (field: keyof BasicInfoFormData, value: any) => {
    setAssessmentState(prev => ({
      ...prev,
      basicInfoData: {
        ...prev.basicInfoData,
        [field]: value
      }
    }));
    // Clear error when field is modified
    if (basicInfoErrors[field as keyof BasicInfoFormErrors]) {
      setBasicInfoErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleBasicInfoSubmit = () => {
    if (validateBasicInfo()) {
      setAssessmentState(prev => ({
        ...prev,
        basicInfoComplete: true,
        currentStep: 'assessment'
      }));
      window.scrollTo(0, 0);
    }
  };

  const handleAnswerChange = (questionId: string, answer: AnswerOption | SameDifferentOption) => {
    setAssessmentState(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [prev.currentSection]: {
          ...prev.answers[prev.currentSection],
          [questionId]: answer
        }
      }
    }));
  };

  const handleNextSection = () => {
    const currentIndex = sectionOrder.indexOf(assessmentState.currentSection);
    const isComplete = isCurrentSectionComplete();
    
    if (currentIndex < sectionOrder.length - 1) {
      setAssessmentState(prev => ({
        ...prev,
        currentSection: sectionOrder[currentIndex + 1],
        sectionProgress: {
          ...prev.sectionProgress,
          [prev.currentSection]: isComplete
        }
      }));
      setActiveQuestionIndex(0);
      window.scrollTo(0, 0);
    }
  };

  const handlePreviousSection = () => {
    const currentIndex = sectionOrder.indexOf(assessmentState.currentSection);
    if (currentIndex > 0) {
      const prevSection = sectionOrder[currentIndex - 1];
      setAssessmentState(prev => ({
        ...prev,
        currentSection: prevSection
      }));
      // Set to last question of previous section
      const prevSectionQuestions = mockAssessmentQuestions[prevSection];
      setActiveQuestionIndex(prevSectionQuestions.length - 1);
      window.scrollTo(0, 0);
    } else {
      setAssessmentState(prev => ({
        ...prev,
        currentStep: 'basic-info'
      }));
    }
  };

  const handleSubmit = async () => {
    // In a real app, you would send the data to the backend here
    // For now, we'll simulate a submission and redirect to results
    
    // Mark current section as complete
    setAssessmentState(prev => ({
      ...prev,
      sectionProgress: {
        ...prev.sectionProgress,
        [prev.currentSection]: true
      },
      isComplete: true
    }));

    // Simulate API call
    setTimeout(() => {
      navigate('/school-assessment-results?session_id=session_academic_9th');
    }, 1000);
  };

  const isCurrentSectionComplete = () => {
    const currentQuestions = mockAssessmentQuestions[assessmentState.currentSection];
    const currentAnswers = assessmentState.answers[assessmentState.currentSection];
    return currentQuestions.every(q => currentAnswers[q.id] !== undefined);
  };

  const currentQuestions = mockAssessmentQuestions[assessmentState.currentSection];
  const currentQuestion = currentQuestions[activeQuestionIndex];
  const currentAnswer = assessmentState.answers[assessmentState.currentSection][currentQuestion?.id];

  const getSectionTitle = (sec: AssessmentSectionEnum) => {
    return sec.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-20">
        <div className="w-full px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/')}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="font-semibold text-lg">School Assessment</h1>
          </div>
          {assessmentState.currentStep === 'assessment' && (
            <div className="flex items-center gap-2">
               <Clock className="w-4 h-4 text-slate-500" />
               <span className={`font-mono font-medium ${timeLeft < 300 ? 'text-red-600' : 'text-slate-700'}`}>
                 {formatTime(timeLeft)}
               </span>
            </div>
          )}
        </div>
      </div>

      {assessmentState.currentStep === 'basic-info' ? (
        <div className="max-w-3xl mx-auto p-4 md:p-8">
          <BasicInfoForm
            data={assessmentState.basicInfoData}
            errors={basicInfoErrors}
            onChange={handleBasicInfoChange}
            onNext={handleBasicInfoSubmit}
          />
        </div>
      ) : (
        <div className="w-full px-6 py-4 h-[calc(100vh-4rem)] flex flex-col">
          {/* Top Navigation - Sections */}
          <div className="mb-4 overflow-x-auto pb-2 flex-shrink-0">
            <div className="flex gap-2 min-w-max">
              {sectionOrder.map((section, idx) => {
                const isActive = assessmentState.currentSection === section;
                const isCompleted = assessmentState.sectionProgress[section];
                const currentSectionIdx = sectionOrder.indexOf(assessmentState.currentSection);
                const isAccessible = idx <= currentSectionIdx || isCompleted;
                
                return (
                  <Button
                    key={section}
                    variant={isActive ? "default" : "outline"}
                    className={`
                      relative px-4 py-2 h-auto flex flex-col items-start gap-1 min-w-[140px]
                      ${isCompleted ? 'border-green-200 bg-green-50 text-green-700 hover:bg-green-100' : ''}
                      ${isActive ? 'ring-2 ring-offset-2 ring-blue-600' : ''}
                    `}
                    onClick={() => {
                      if (isAccessible && !isActive) {
                        setAssessmentState(prev => ({
                          ...prev,
                          currentSection: section
                        }));
                        setActiveQuestionIndex(0);
                      }
                    }}
                    disabled={!isAccessible}
                  >
                    <span className="text-xs font-medium uppercase tracking-wider opacity-70">
                      Section {idx + 1}
                    </span>
                    <span className="font-semibold text-sm whitespace-nowrap">
                      {getSectionTitle(section)}
                    </span>
                    {isCompleted && (
                      <div className="absolute top-2 right-2">
                        <CheckCircle2 className="w-4 h-4 text-green-600" />
                      </div>
                    )}
                  </Button>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-0">
            {/* Left Sidebar - Question Navigation */}
            <Card className="lg:col-span-3 h-full flex flex-col overflow-hidden">
              <CardContent className="p-4 flex-1 flex flex-col gap-4 min-h-0">
                <div>
                  <h3 className="font-semibold text-slate-900 mb-2">Questions</h3>
                  <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded-full bg-blue-600" />
                      <span>Current</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded-full bg-green-100 border border-green-600" />
                      <span>Answered</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <div className="w-3 h-3 rounded-full bg-slate-100 border border-slate-300" />
                      <span>Pending</span>
                    </div>
                  </div>
                </div>
                
                <ScrollArea className="flex-1 pr-4">
                  <div className="grid grid-cols-5 gap-2">
                    {currentQuestions.map((q, idx) => {
                      const isAnswered = assessmentState.answers[assessmentState.currentSection][q.id] !== undefined;
                      const isCurrent = idx === activeQuestionIndex;
                      
                      return (
                        <button
                          key={q.id}
                          onClick={() => setActiveQuestionIndex(idx)}
                          className={`
                            aspect-square rounded-lg flex items-center justify-center text-sm font-medium transition-all
                            ${isCurrent 
                              ? 'bg-blue-600 text-white shadow-md scale-105' 
                              : isAnswered
                                ? 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
                                : 'bg-slate-50 text-slate-600 border border-slate-200 hover:bg-slate-100'
                            }
                          `}
                        >
                          {idx + 1}
                        </button>
                      );
                    })}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Right Content - Question Area */}
            <Card className="lg:col-span-9 h-full flex flex-col overflow-hidden">
              <CardContent className="p-6 md:p-8 flex-1 flex flex-col min-h-0">
                <div className="flex items-center justify-between mb-4 flex-shrink-0">
                  <Badge variant="outline" className="text-sm px-3 py-1">
                    Question {activeQuestionIndex + 1} of {currentQuestions.length}
                  </Badge>
                  <span className="text-sm text-slate-500">
                    {getSectionTitle(assessmentState.currentSection)}
                  </span>
                </div>

                <div className="flex-1 w-full overflow-y-auto pr-2">
                  <div className="max-w-4xl mx-auto">
                    <h2 className="text-xl font-semibold text-slate-900 mb-6 leading-relaxed">
                      {currentQuestion.question}
                    </h2>

                    <div className="space-y-3">
                      {currentQuestion.options.map((option) => (
                        <label
                          key={option.value}
                          className={`
                            flex items-center gap-4 p-3 rounded-xl border cursor-pointer transition-all group
                            ${currentAnswer === option.value 
                              ? 'border-blue-600 bg-blue-50/50' 
                              : 'border-slate-200 hover:border-blue-200 hover:bg-slate-50'
                            }
                          `}
                        >
                          <div className={`
                            w-5 h-5 rounded-full border flex items-center justify-center flex-shrink-0 transition-colors
                            ${currentAnswer === option.value
                              ? 'border-blue-600 bg-blue-600'
                              : 'border-slate-300 group-hover:border-blue-400'
                            }
                          `}>
                            {currentAnswer === option.value && (
                              <div className="w-2 h-2 rounded-full bg-white" />
                            )}
                          </div>
                          <input
                            type="radio"
                            name={currentQuestion.id}
                            value={option.value}
                            checked={currentAnswer === option.value}
                            onChange={() => handleAnswerChange(currentQuestion.id, option.value)}
                            className="hidden"
                          />
                          <span className={`text-base ${currentAnswer === option.value ? 'text-blue-900 font-medium' : 'text-slate-700'}`}>
                            {option.label}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between mt-4 pt-4 border-t flex-shrink-0">
                  <Button
                    variant="outline"
                    onClick={() => {
                      if (activeQuestionIndex > 0) {
                        setActiveQuestionIndex(prev => prev - 1);
                      } else {
                        handlePreviousSection();
                      }
                    }}
                    disabled={activeQuestionIndex === 0 && assessmentState.currentSection === sectionOrder[0]}
                    className="gap-2"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Previous
                  </Button>

                  {activeQuestionIndex === currentQuestions.length - 1 ? (
                    <Button
                      onClick={
                        assessmentState.currentSection === sectionOrder[sectionOrder.length - 1]
                          ? handleSubmit
                          : handleNextSection
                      }
                      className="gap-2 bg-blue-600 hover:bg-blue-700"
                    >
                      {assessmentState.currentSection === sectionOrder[sectionOrder.length - 1] ? 'Submit Assessment' : 'Next Section'}
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  ) : (
                    <Button
                      onClick={() => setActiveQuestionIndex(prev => Math.min(currentQuestions.length - 1, prev + 1))}
                      className="gap-2"
                    >
                      Next Question
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default SchoolAssessment;
