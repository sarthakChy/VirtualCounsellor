import { AssessmentSection, AnswerOption, SameDifferentOption } from './types/schoolAssessmentTypes';

// Mock data for assessment questions
export const mockAssessmentQuestions = {
  [AssessmentSection.VERBAL_SYNONYMS]: [
    {
      id: 'vs1',
      question: 'FAST',
      options: [
        { value: AnswerOption.A, label: 'old' },
        { value: AnswerOption.B, label: 'rapid' },
        { value: AnswerOption.C, label: 'slow' },
        { value: AnswerOption.D, label: 'early' },
        { value: AnswerOption.E, label: 'late' }
      ],
      correctAnswer: AnswerOption.B
    },
    {
      id: 'vs2', 
      question: 'DECEIVE',
      options: [
        { value: AnswerOption.A, label: 'blunder' },
        { value: AnswerOption.B, label: 'obtain' },
        { value: AnswerOption.C, label: 'conceal' },
        { value: AnswerOption.D, label: 'mislead' },
        { value: AnswerOption.E, label: 'disclose' }
      ],
      correctAnswer: AnswerOption.D
    },
    {
      id: 'vs3',
      question: 'EXCESS', 
      options: [
        { value: AnswerOption.A, label: 'waste' },
        { value: AnswerOption.B, label: 'departure' },
        { value: AnswerOption.C, label: 'surplus' },
        { value: AnswerOption.D, label: 'tax' },
        { value: AnswerOption.E, label: 'approach' }
      ],
      correctAnswer: AnswerOption.C
    }
  ],
  [AssessmentSection.VERBAL_PROVERBS]: [
    {
      id: 'vp1',
      question: 'STRIKE WHILE THE IRON IS HOT',
      options: [
        { value: AnswerOption.A, label: 'Take things as you find them' },
        { value: AnswerOption.B, label: 'Hot love is soon cold' },
        { value: AnswerOption.C, label: 'Make hay while the sun shines' },
        { value: AnswerOption.D, label: 'First think and then speak' },
        { value: AnswerOption.E, label: 'Look before you leap' }
      ],
      correctAnswer: AnswerOption.C
    },
    {
      id: 'vp2',
      question: 'IT NEVER RAINS BUT IT POURS',
      options: [
        { value: AnswerOption.A, label: 'cloudy mornings turn to clear evenings' },
        { value: AnswerOption.B, label: 'misfortunes never come one at a time' },
        { value: AnswerOption.C, label: 'the least predictable thing in life is the weather' },
        { value: AnswerOption.D, label: 'riches alone will not make a man happy' },
        { value: AnswerOption.E, label: 'every cloud has a silver lining' }
      ],
      correctAnswer: AnswerOption.B
    },
    {
      id: 'vp3',
      question: 'LET SLEEPING DOGS LIE',
      options: [
        { value: AnswerOption.A, label: 'as you make your bed, so you must lie on it' },
        { value: AnswerOption.B, label: 'do not keep a dog and bark yourself' },
        { value: AnswerOption.C, label: 'there will be sleeping enough in the grave' },
        { value: AnswerOption.D, label: 'never look for trouble; let trouble look for you' },
        { value: AnswerOption.E, label: 'an old dog does not bark for nothing' }
      ],
      correctAnswer: AnswerOption.D
    }
  ],
  [AssessmentSection.NUMERICAL]: [
    {
      id: 'na1',
      question: '92×(25−19)​=',
      options: [
        { value: AnswerOption.A, label: '32​' },
        { value: AnswerOption.B, label: '131​' },
        { value: AnswerOption.C, label: '191​' },
        { value: AnswerOption.D, label: '197​' },
        { value: AnswerOption.E, label: '232​' }
      ],
      correctAnswer: AnswerOption.E
    },
    {
      id: 'na2',
      question: 'Which one of the numbers below could replace X in both places in: 4+X=6−X?',
      options: [
        { value: AnswerOption.A, label: '4' },
        { value: AnswerOption.B, label: '3' },
        { value: AnswerOption.C, label: '2' },
        { value: AnswerOption.D, label: '1' },
        { value: AnswerOption.E, label: '0' }
      ],
      correctAnswer: AnswerOption.D
    },
    {
      id: 'na3',
      question: 'If a car travels 60 miles in 1.5 hours, what is its average speed?',
      options: [
        { value: AnswerOption.A, label: '30 mph' },
        { value: AnswerOption.B, label: '35 mph' },
        { value: AnswerOption.C, label: '40 mph' },
        { value: AnswerOption.D, label: '45 mph' },
        { value: AnswerOption.E, label: '50 mph' }
      ],
      correctAnswer: AnswerOption.C
    }
  ],
  [AssessmentSection.MECHANICAL]: [
    {
      id: 'ma1',
      question: 'If Gear A turns clockwise, which way will Gear B turn if they are meshed together?',
      options: [
        { value: AnswerOption.A, label: 'Clockwise' },
        { value: AnswerOption.B, label: 'Counter-clockwise' },
        { value: AnswerOption.C, label: 'It wont move' },
        { value: AnswerOption.D, label: 'Depends on size' },
        { value: AnswerOption.E, label: 'None of the above' }
      ],
      correctAnswer: AnswerOption.B
    },
    {
      id: 'ma2',
      question: 'Which tool is best for tightening a nut?',
      options: [
        { value: AnswerOption.A, label: 'Hammer' },
        { value: AnswerOption.B, label: 'Wrench' },
        { value: AnswerOption.C, label: 'Screwdriver' },
        { value: AnswerOption.D, label: 'Pliers' },
        { value: AnswerOption.E, label: 'Saw' }
      ],
      correctAnswer: AnswerOption.B
    },
    {
      id: 'ma3',
      question: 'In a lever system, if the fulcrum is closer to the load, is it easier or harder to lift?',
      options: [
        { value: AnswerOption.A, label: 'Harder' },
        { value: AnswerOption.B, label: 'Easier' },
        { value: AnswerOption.C, label: 'Same effort' },
        { value: AnswerOption.D, label: 'Impossible to tell' },
        { value: AnswerOption.E, label: 'Depends on the load' }
      ],
      correctAnswer: AnswerOption.B
    }
  ],
  [AssessmentSection.CLERICAL]: [
    {
      id: 'cl1',
      question: 'Compare: 84729 vs 84729',
      options: [
        { value: SameDifferentOption.SAME, label: 'Same' },
        { value: SameDifferentOption.DIFFERENT, label: 'Different' }
      ],
      correctAnswer: SameDifferentOption.SAME
    },
    {
      id: 'cl2',
      question: 'Compare: Smith & Co. vs Smyth & Co.',
      options: [
        { value: SameDifferentOption.SAME, label: 'Same' },
        { value: SameDifferentOption.DIFFERENT, label: 'Different' }
      ],
      correctAnswer: SameDifferentOption.DIFFERENT
    },
    {
      id: 'cl3',
      question: 'Compare: 12/05/2023 vs 12/05/2023',
      options: [
        { value: SameDifferentOption.SAME, label: 'Same' },
        { value: SameDifferentOption.DIFFERENT, label: 'Different' }
      ],
      correctAnswer: SameDifferentOption.SAME
    }
  ],
  [AssessmentSection.REASONING]: [
    {
      id: 'ra1',
      question: 'Complete the series: 2, 4, 8, 16, ...',
      options: [
        { value: AnswerOption.A, label: '24' },
        { value: AnswerOption.B, label: '30' },
        { value: AnswerOption.C, label: '32' },
        { value: AnswerOption.D, label: '36' },
        { value: AnswerOption.E, label: '40' }
      ],
      correctAnswer: AnswerOption.C
    },
    {
      id: 'ra2',
      question: 'If all Bloops are Zazzles, and some Zazzles are Quirks, are all Bloops Quirks?',
      options: [
        { value: AnswerOption.A, label: 'Yes' },
        { value: AnswerOption.B, label: 'No' },
        { value: AnswerOption.C, label: 'Maybe' },
        { value: AnswerOption.D, label: 'Impossible' },
        { value: AnswerOption.E, label: 'None of the above' }
      ],
      correctAnswer: AnswerOption.C
    },
    {
      id: 'ra3',
      question: 'Which shape does not belong?',
      options: [
        { value: AnswerOption.A, label: 'Square' },
        { value: AnswerOption.B, label: 'Triangle' },
        { value: AnswerOption.C, label: 'Circle' },
        { value: AnswerOption.D, label: 'Rectangle' },
        { value: AnswerOption.E, label: 'Pentagon' }
      ],
      correctAnswer: AnswerOption.C
    }
  ]
};
