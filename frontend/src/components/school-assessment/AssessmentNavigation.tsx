import React from 'react';
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight, CheckCircle2 } from 'lucide-react';

interface NavigationProps {
  canGoNext: boolean;
  canGoPrevious: boolean;
  isLastSection: boolean;
  onNext: () => void;
  onPrevious: () => void;
  onSubmit: () => void;
}

const AssessmentNavigation: React.FC<NavigationProps> = ({
  canGoNext,
  canGoPrevious,
  isLastSection,
  onNext,
  onPrevious,
  onSubmit
}) => {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4 shadow-lg z-10">
      <div className="max-w-3xl mx-auto flex justify-between items-center">
        <Button
          variant="outline"
          onClick={onPrevious}
          disabled={!canGoPrevious}
          className="w-32"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Previous
        </Button>

        {isLastSection ? (
          <Button 
            onClick={onSubmit}
            disabled={!canGoNext}
            className="w-32 bg-green-600 hover:bg-green-700"
          >
            Submit
            <CheckCircle2 className="w-4 h-4 ml-2" />
          </Button>
        ) : (
          <Button
            onClick={onNext}
            disabled={!canGoNext}
            className="w-32"
          >
            Next
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        )}
      </div>
    </div>
  );
};

export default AssessmentNavigation;
