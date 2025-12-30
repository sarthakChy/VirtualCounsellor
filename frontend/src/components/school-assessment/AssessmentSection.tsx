import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { AnswerOption, SameDifferentOption, AssessmentSection as AssessmentSectionEnum } from '../../types/schoolAssessmentTypes';
import type { AssessmentQuestion } from '../../types/schoolAssessmentTypes';

interface AssessmentSectionProps {
  section: AssessmentSectionEnum;
  questions: AssessmentQuestion[];
  answers: Record<string, AnswerOption | SameDifferentOption>;
  onAnswerChange: (questionId: string, answer: AnswerOption | SameDifferentOption) => void;
}

const AssessmentSection: React.FC<AssessmentSectionProps> = ({ section, questions, answers, onAnswerChange }) => {
  const getSectionTitle = (sec: AssessmentSectionEnum) => {
    return sec.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle>{getSectionTitle(section)} Assessment</CardTitle>
        <CardDescription>Please answer all questions to the best of your ability.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-8">
        {questions.map((q, index) => (
          <div key={q.id} className="space-y-4 p-4 border rounded-lg bg-slate-50/50">
            <div className="flex gap-3">
              <span className="font-semibold text-slate-500">Q{index + 1}.</span>
              <p className="font-medium text-slate-900">{q.question}</p>
            </div>
            
            <div className="grid gap-3 pl-8">
              {q.options.map((option) => (
                <label
                  key={option.value}
                  className={`
                    flex items-center gap-3 p-3 rounded-md border cursor-pointer transition-all
                    ${answers[q.id] === option.value 
                      ? 'border-primary bg-primary/5 ring-1 ring-primary' 
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'}
                  `}
                >
                  <input
                    type="radio"
                    name={q.id}
                    value={option.value}
                    checked={answers[q.id] === option.value}
                    onChange={() => onAnswerChange(q.id, option.value)}
                    className="w-4 h-4 text-primary border-slate-300 focus:ring-primary"
                  />
                  <span className="text-sm text-slate-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

export default AssessmentSection;
