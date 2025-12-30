import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { 
  Upload, 
  GraduationCap, 
  Github, 
  Linkedin, 
  Target, 
  CheckCircle2,
  AlertCircle,
  FileText,
  Award,
  Briefcase,
  Sparkles,
  ArrowRight,
  X
} from 'lucide-react';

const CollegeAssessmentForm = () => {
  const [formData, setFormData] = useState({
    resume: null as File | null,
    githubProfile: '',
    linkedinProfile: '',
    initialMessage: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [completionPercentage, setCompletionPercentage] = useState(0);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    calculateCompletion();
  }, [formData]);

  const calculateCompletion = () => {
    const fields = [
      formData.resume !== null,
      formData.initialMessage.trim().split(/\s+/).filter(w => w.length > 0).length >= 20
    ];
    const completed = fields.filter(Boolean).length;
    setCompletionPercentage((completed / fields.length) * 100);
  };

  const handleFileChange = (file: File | null) => {
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setErrors(prev => ({ ...prev, resume: 'File size must be less than 5MB' }));
        return;
      }
      if (!file.name.match(/\.(pdf|doc|docx)$/i)) {
        setErrors(prev => ({ ...prev, resume: 'Only PDF, DOC, or DOCX files are allowed' }));
        return;
      }
    }
    setFormData(prev => ({ ...prev, resume: file }));
    setErrors(prev => ({ ...prev, resume: '' }));
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    const newErrors: Record<string, string> = {};

    if (!formData.resume) newErrors.resume = 'Resume is required';
    
    const wordCount = formData.initialMessage.trim().split(/\s+/).filter(w => w.length > 0).length;
    if (wordCount < 20) newErrors.initialMessage = 'Please provide at least 20 words';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);

    try {
      const formDataToSend = new FormData();
      if (formData.resume) formDataToSend.append('resume', formData.resume);
      
      if (formData.githubProfile) {
          formDataToSend.append('github_profile', JSON.stringify({ username: formData.githubProfile }));
      }
      if (formData.linkedinProfile) {
          formDataToSend.append('linkedin_profile', JSON.stringify({ connections: 0 })); 
      }
      
      formDataToSend.append('initial_message', JSON.stringify(formData.initialMessage));

      const response = await fetch('http://localhost:8000/college-upskilling', {
          method: 'POST',
          body: formDataToSend,
      });
      
      const data = await response.json();
      
      if (data.success) {
          navigate(`/analysis-result?session_id=${data.session_id}`);
      } else {
          alert('Error: ' + (data.error || 'Unknown error occurred'));
      }
    } catch (error) {
      console.error(error);
      alert('Failed to submit assessment. Please check your connection.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const wordCount = formData.initialMessage.trim().split(/\s+/).filter(w => w.length > 0).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10 backdrop-blur-sm bg-white/95">
        <div className="container mx-auto px-4 py-4 max-w-7xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
                <GraduationCap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">College Assessment</h1>
                <p className="text-sm text-slate-600">Shape your career journey</p>
              </div>
            </div>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              <Sparkles className="w-4 h-4 mr-2" />
              {Math.round(completionPercentage)}% Complete
            </Badge>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 max-w-7xl">
          <Progress value={completionPercentage} className="h-1" />
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Hero Section */}
        <div className="text-center mb-12 space-y-4">
          <Badge className="bg-blue-100 text-blue-700 border-blue-200">
            <Award className="w-3 h-3 mr-1" />
            Personalized Career Guidance
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900">
            Let's Build Your Career Roadmap
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Share your academic journey and aspirations. Our AI will analyze your profile and create a personalized upskilling plan.
          </p>
        </div>

        {/* Main Form Layout - Masonry Style */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Resume Upload Card */}
          <Card className="border-2 hover:border-blue-300 transition-all">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
                  <Upload className="w-4 h-4 text-blue-600" />
                </div>
                Upload Resume
              </CardTitle>
              <CardDescription>PDF, DOC, or DOCX (Max 5MB)</CardDescription>
            </CardHeader>
            <CardContent>
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`
                  border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
                  transition-all duration-200
                  ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:border-blue-400 hover:bg-slate-50'}
                  ${formData.resume ? 'border-green-500 bg-green-50' : ''}
                `}
              >
                <input
                  type="file"
                  id="resume-upload"
                  className="hidden"
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => handleFileChange(e.target.files?.[0] || null)}
                />
                <label htmlFor="resume-upload" className="cursor-pointer">
                  {formData.resume ? (
                    <div className="space-y-3">
                      <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mx-auto">
                        <CheckCircle2 className="w-6 h-6 text-green-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900">{formData.resume.name}</p>
                        <p className="text-sm text-slate-600">
                          {(formData.resume.size / 1024).toFixed(1)} KB
                        </p>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={(e) => {
                          e.preventDefault();
                          handleFileChange(null);
                        }}
                      >
                        <X className="w-4 h-4 mr-1" />
                        Remove
                      </Button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto">
                        <FileText className="w-6 h-6 text-slate-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-slate-900">Drop your resume here</p>
                        <p className="text-sm text-slate-600">or click to browse</p>
                      </div>
                    </div>
                  )}
                </label>
              </div>
              {errors.resume && (
                <div className="flex items-center gap-2 text-red-600 text-sm mt-2">
                  <AlertCircle className="w-4 h-4" />
                  {errors.resume}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Professional Profiles Card */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center">
                  <Briefcase className="w-4 h-4 text-slate-600" />
                </div>
                Professional Profiles
              </CardTitle>
              <CardDescription>Optional: Share your online profiles for deeper analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="github" className="flex items-center gap-2">
                    <Github className="w-4 h-4" />
                    GitHub Profile
                  </Label>
                  <Input
                    id="github"
                    placeholder="https://github.com/username"
                    value={formData.githubProfile}
                    onChange={(e) => setFormData(prev => ({ ...prev, githubProfile: e.target.value }))}
                    className={errors.githubProfile ? 'border-red-500' : ''}
                  />
                  {errors.githubProfile && (
                    <p className="text-sm text-red-600 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" />
                      {errors.githubProfile}
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="linkedin" className="flex items-center gap-2">
                    <Linkedin className="w-4 h-4" />
                    LinkedIn Profile
                  </Label>
                  <Input
                    id="linkedin"
                    placeholder="https://linkedin.com/in/username"
                    value={formData.linkedinProfile}
                    onChange={(e) => setFormData(prev => ({ ...prev, linkedinProfile: e.target.value }))}
                    className={errors.linkedinProfile ? 'border-red-500' : ''}
                  />
                  {errors.linkedinProfile && (
                    <p className="text-sm text-red-600 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" />
                      {errors.linkedinProfile}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Career Goals - Full Width */}
        <Card className="border-2 border-blue-200 mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
                <Target className="w-4 h-4 text-blue-600" />
              </div>
              Your Career Aspirations
            </CardTitle>
            <CardDescription>
              Describe your career goals, interests, and what kind of guidance you're looking for (minimum 20 words)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Textarea
                placeholder="Example: I am a final year B.Tech student specializing in AI/ML. I want to transition into a data engineer role at top tech companies. Can you help me identify skill gaps and provide a learning roadmap?"
                value={formData.initialMessage}
                onChange={(e) => setFormData(prev => ({ ...prev, initialMessage: e.target.value }))}
                className={`min-h-32 ${errors.initialMessage ? 'border-red-500' : ''}`}
              />
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {wordCount >= 20 ? (
                    <>
                      <CheckCircle2 className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-green-600">Great! You've provided enough detail</span>
                    </>
                  ) : (
                    <>
                      <AlertCircle className="w-4 h-4 text-amber-600" />
                      <span className="text-sm text-amber-600">{20 - wordCount} more words needed</span>
                    </>
                  )}
                </div>
                <span className="text-sm text-slate-500">{wordCount} words</span>
              </div>
              {errors.initialMessage && (
                <p className="text-sm text-red-600 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.initialMessage}
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Submit Button */}
        <div className="flex justify-center pt-4">
          <Button
            size="lg"
            onClick={handleSubmit}
            disabled={completionPercentage < 100 || isSubmitting}
            className="h-14 px-12 text-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-xl shadow-blue-500/30 hover:shadow-2xl hover:shadow-blue-500/40 transition-all"
          >
            {isSubmitting ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                Processing...
              </>
            ) : (
              <>
                Submit Assessment
                <ArrowRight className="ml-2 w-5 h-5" />
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CollegeAssessmentForm;