import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import type { BasicInfoFormData, BasicInfoFormErrors } from '../../types/schoolAssessmentTypes';

interface BasicInfoFormProps {
  data: BasicInfoFormData;
  errors: BasicInfoFormErrors;
  onChange: (field: keyof BasicInfoFormData, value: any) => void;
  onNext: () => void;
}

const BasicInfoForm: React.FC<BasicInfoFormProps> = ({ data, errors, onChange, onNext }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    onChange(name as keyof BasicInfoFormData, value);
  };

  const handleArrayChange = (e: React.ChangeEvent<HTMLInputElement>, field: keyof BasicInfoFormData) => {
    const value = e.target.value.split(',').map(item => item.trim());
    onChange(field, value);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Student Information</CardTitle>
        <CardDescription>Please provide some basic details to get started.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="studentName">Full Name</Label>
          <Input
            id="studentName"
            name="studentName"
            value={data.studentName}
            onChange={handleChange}
            placeholder="Enter your full name"
            className={errors.studentName ? 'border-red-500' : ''}
          />
          {errors.studentName && <p className="text-sm text-red-500">{errors.studentName}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="currentGrade">Current Grade</Label>
            <Input
              id="currentGrade"
              name="currentGrade"
              value={data.currentGrade}
              onChange={handleChange}
              placeholder="e.g. 9th Grade"
              className={errors.currentGrade ? 'border-red-500' : ''}
            />
            {errors.currentGrade && <p className="text-sm text-red-500">{errors.currentGrade}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="currentStream">Current Stream (if applicable)</Label>
            <Input
              id="currentStream"
              name="currentStream"
              value={data.currentStream}
              onChange={handleChange}
              placeholder="e.g. Science, Commerce"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="subjects">Current Subjects (comma separated)</Label>
          <Input
            id="subjects"
            name="subjects"
            value={data.subjects.join(', ')}
            onChange={(e) => handleArrayChange(e, 'subjects')}
            placeholder="Math, Science, English..."
            className={errors.subjects ? 'border-red-500' : ''}
          />
          {errors.subjects && <p className="text-sm text-red-500">{errors.subjects}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="academicPerformance">Academic Performance (GPA/Percentage)</Label>
          <Input
            id="academicPerformance"
            name="academicPerformance"
            value={data.academicPerformance}
            onChange={handleChange}
            placeholder="e.g. 9.5 GPA or 95%"
            className={errors.academicPerformance ? 'border-red-500' : ''}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="interests">Interests & Hobbies (comma separated)</Label>
          <Input
            id="interests"
            name="interests"
            value={data.interests.join(', ')}
            onChange={(e) => handleArrayChange(e, 'interests')}
            placeholder="Coding, Reading, Sports..."
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="careerAspirations">Career Aspirations</Label>
          <Textarea
            id="careerAspirations"
            name="careerAspirations"
            value={data.careerAspirations}
            onChange={handleChange}
            placeholder="What do you want to become in the future?"
            className={errors.careerAspirations ? 'border-red-500' : ''}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="parentContact">Parent Contact Number</Label>
          <Input
            id="parentContact"
            name="parentContact"
            value={data.parentContact}
            onChange={handleChange}
            placeholder="Enter parent's contact number"
            className={errors.parentContact ? 'border-red-500' : ''}
          />
        </div>

        <div className="pt-4">
          <Button onClick={onNext} className="w-full">Start Assessment</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default BasicInfoForm;
