import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Loader2, 
  CheckCircle2, 
  AlertCircle, 
  ArrowLeft, 
  FileText, 
  Target, 
  TrendingUp, 
  Briefcase, 
  BookOpen, 
  Globe, 
  Award, 
  Flag,
  LayoutDashboard,
  ChevronRight,
  Zap,
  Download,
  Share2,
  Sparkles,
  Users,
  Clock
} from 'lucide-react';
import { createMockAssessmentData } from '../mockAssessmentData';
import type { AssessmentResultsResponse } from '../types/assessmentResultsTypes';

const CollegeAnalysisResult = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get('session_id');
  const [status, setStatus] = useState<'pending' | 'processing' | 'completed' | 'failed'>('pending');
  const [result, setResult] = useState<AssessmentResultsResponse['data']['results'] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    if (!sessionId) {
      const mockResponse = createMockAssessmentData();
      setStatus('completed');
      setResult(mockResponse.data.results);
      setProgress(100);
      return;
    }

    const pollStatus = async () => {
      try {
        const response = await fetch(`http://localhost:8000/status/${sessionId}`);
        const data = await response.json();

        if (data.success) {
          setStatus(data.data.status);
          if (data.data.status === 'completed') {
            setResult(data.data.results);
            setProgress(100);
          } else if (data.data.status === 'failed') {
            setError(data.data.error || 'Analysis failed');
          } else {
            setProgress(prev => Math.min(prev + 5, 90));
            setTimeout(pollStatus, 2000);
          }
        } else {
          console.warn('API failed, falling back to mock data');
          const mockResponse = createMockAssessmentData();
          setStatus('completed');
          setResult(mockResponse.data.results);
          setProgress(100);
        }
      } catch (err) {
        console.error(err);
        console.warn('Network error, falling back to mock data');
        const mockResponse = createMockAssessmentData();
        setStatus('completed');
        setResult(mockResponse.data.results);
        setProgress(100);
      }
    };

    pollStatus();
  }, [sessionId]);

  if (status === 'pending' || status === 'processing') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex flex-col items-center justify-center p-4">
        <Card className="w-full max-w-md shadow-xl border-0">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-2xl">Analyzing Your Profile</CardTitle>
            <CardDescription className="text-base">Our AI agents are reviewing your resume and building your personalized career roadmap...</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex justify-center">
              <div className="relative">
                <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
                <div className="absolute inset-0 w-16 h-16 bg-blue-100 rounded-full blur-xl opacity-50 animate-pulse" />
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between text-sm font-medium">
                <span className="text-slate-600">Progress</span>
                <span className="text-blue-600">{progress}%</span>
              </div>
              <Progress value={progress} className="h-3 bg-slate-200" />
              <p className="text-sm text-center text-slate-600 font-medium">
                {progress < 30 ? '🔍 Extracting resume data...' : 
                 progress < 60 ? '🧠 Analyzing skills and gaps...' : 
                 '✨ Generating recommendations...'}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (status === 'failed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-red-50 to-orange-50 flex flex-col items-center justify-center p-4">
        <Card className="w-full max-w-md border-0 shadow-xl">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto w-16 h-16 bg-gradient-to-br from-red-500 to-orange-600 rounded-2xl flex items-center justify-center shadow-lg">
              <AlertCircle className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-2xl text-red-700">Analysis Failed</CardTitle>
            <CardDescription className="text-base">We encountered an issue while analyzing your profile.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-center text-red-700 font-medium">{error}</p>
            </div>
            <Button onClick={() => navigate('/college-assessment')} className="w-full h-12 text-base bg-gradient-to-r from-red-500 to-orange-600 hover:from-red-600 hover:to-orange-700">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const renderProfileAnalysis = (data: any) => {
    const analysis = data?.comprehensive_analysis;
    const individual = data?.individual_analyses;
    
    if (!analysis) return null;

    return (
      <div className="space-y-8">
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-green-50 to-emerald-50 hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2 text-green-800">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Award className="w-5 h-5 text-green-600" />
                </div>
                Key Strengths
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {analysis.key_strengths?.map((strength: string, idx: number) => (
                  <li key={idx} className="text-sm text-slate-700 flex items-start gap-3 bg-white/70 backdrop-blur p-3 rounded-lg hover:bg-white transition-colors">
                    <CheckCircle2 className="w-5 h-5 text-green-600 mt-0.5 shrink-0" />
                    <span className="leading-relaxed">{strength}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-orange-50 to-amber-50 hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2 text-orange-800">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Target className="w-5 h-5 text-orange-600" />
                </div>
                Areas for Improvement
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {analysis.improvement_priorities?.map((item: string, idx: number) => (
                  <li key={idx} className="text-sm text-slate-700 flex items-start gap-3 bg-white/70 backdrop-blur p-3 rounded-lg hover:bg-white transition-colors">
                    <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
        
        <Card className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-0 shadow-lg">
          <CardContent className="p-8">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-blue-100 rounded-xl">
                <TrendingUp className="w-6 h-6 text-blue-600" />
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-lg mb-3 text-blue-900">Profile Positioning</h4>
                <p className="text-blue-800 leading-relaxed text-base">{analysis.profile_positioning}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {individual && (
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent flex-1" />
              <h3 className="text-xl font-bold text-slate-900">Detailed Breakdown</h3>
              <div className="h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent flex-1" />
            </div>
            
            <div className="grid gap-6 md:grid-cols-2">
              <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                      <FileText className="w-5 h-5 text-blue-600" />
                    </div>
                    Resume Analysis
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-gradient-to-br from-slate-50 to-blue-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-slate-700 text-sm italic leading-relaxed">
                      "{individual.resume?.personal_summary}"
                    </p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 block">Detected Skills</span>
                    <div className="flex flex-wrap gap-2">
                      {individual.resume?.technical_skills?.slice(0, 8).map((skill: string, i: number) => (
                        <Badge key={i} variant="secondary" className="text-xs px-3 py-1 hover:bg-blue-100 transition-colors">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-3">
                    <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-slate-200 transition-colors">
                      <Globe className="w-5 h-5 text-slate-900" />
                    </div>
                    GitHub Profile
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center p-4 bg-gradient-to-br from-slate-50 to-purple-50 rounded-xl border border-slate-100">
                    <span className="text-slate-600 text-sm font-medium">Project Quality</span>
                    <Badge className="bg-slate-900 hover:bg-slate-800">{individual.github?.project_quality_assessment}</Badge>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-600 font-medium">Technical Depth</span>
                      <span className="font-bold text-slate-900">{Math.round(individual.github?.technical_depth_score * 100)}%</span>
                    </div>
                    <Progress value={individual.github?.technical_depth_score * 100} className="h-3" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                      <Briefcase className="w-5 h-5 text-blue-700" />
                    </div>
                    LinkedIn Profile
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center p-4 bg-gradient-to-br from-slate-50 to-blue-50 rounded-xl border border-slate-100">
                    <span className="text-slate-600 text-sm font-medium">Network Strength</span>
                    <Badge className="bg-blue-700 hover:bg-blue-600">{individual.linkedin?.professional_network_strength}</Badge>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-600 font-medium">Profile Completeness</span>
                      <span className="font-bold text-slate-900">{Math.round(individual.linkedin?.profile_completeness * 100)}%</span>
                    </div>
                    <Progress value={individual.linkedin?.profile_completeness * 100} className="h-3" />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 rounded-lg group-hover:bg-indigo-200 transition-colors">
                      <BookOpen className="w-5 h-5 text-indigo-600" />
                    </div>
                    Academic Record
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-gradient-to-br from-slate-50 to-indigo-50 rounded-xl border border-slate-100">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-2">Performance</span>
                    <p className="text-slate-900 font-semibold text-lg">{individual.academic?.academic_performance}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-3">Key Coursework</span>
                    <p className="text-slate-600 text-sm leading-relaxed">
                      {individual.academic?.relevant_coursework?.slice(0, 5).join(', ')}...
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderMarketIntelligence = (data: any) => {
    return (
      <div className="space-y-8">
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-indigo-100 rounded-lg">
                  <Globe className="w-5 h-5 text-indigo-600" />
                </div>
                Industry Trends
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(data?.industry_trends || {}).map(([key, value]: [string, any]) => (
                <div key={key} className="bg-gradient-to-br from-slate-50 to-indigo-50 p-5 rounded-xl border border-slate-100 hover:border-indigo-200 transition-colors">
                  <span className="font-bold text-slate-900 block mb-2 text-base">{key}</span>
                  <span className="text-sm text-slate-600 leading-relaxed">{value}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                </div>
                Salary Insights
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(data?.salary_insights || {}).map(([level, info]: [string, any]) => (
                <div key={level} className="bg-gradient-to-br from-slate-50 to-green-50 p-5 rounded-xl border border-slate-100 hover:border-green-200 transition-colors">
                  <span className="font-bold text-slate-900 block mb-3 capitalize text-base">{level}</span>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {Object.entries(info).map(([k, v]: [string, any]) => (
                      <div key={k}>
                        <span className="text-slate-500 text-xs uppercase tracking-wider font-semibold">{k}</span>
                        <span className="block text-slate-900 font-bold mt-1 text-base">{v}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-purple-600" />
                </div>
                Skill Demand
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {Object.entries(data?.skill_demand?.['Technical Skills'] || {}).slice(0, 5).map(([skill, demand]: [string, any], idx) => (
                <div key={idx} className="flex justify-between items-center text-sm p-4 bg-gradient-to-r from-slate-50 to-purple-50 rounded-xl hover:shadow-md transition-all border border-slate-100">
                  <span className="text-slate-800 font-semibold">{skill}</span>
                  <Badge variant="outline" className="bg-white font-medium">{demand.split('-')[0]}</Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Sparkles className="w-5 h-5 text-blue-600" />
                </div>
                Emerging Technologies
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {data?.emerging_technologies?.map((tech: string, idx: number) => (
                  <Badge key={idx} className="px-4 py-2 text-sm bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transition-all shadow-sm hover:shadow-md">
                    {tech}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  };

  const renderSkillStrategy = (data: any) => {
    return (
      <div className="space-y-8">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BookOpen className="w-6 h-6 text-purple-600" />
              </div>
              Learning Roadmap
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative border-l-4 border-purple-300 ml-4 space-y-10 pl-10 py-4">
              {data?.development_roadmap?.learning_pathway?.map((step: any, idx: number) => (
                <div key={idx} className="relative group">
                  <span className="absolute -left-[49px] top-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 border-4 border-white shadow-lg flex items-center justify-center text-white text-xs font-bold group-hover:scale-110 transition-transform">
                    {idx + 1}
                  </span>
                  <div className="space-y-3">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-3">
                      <h5 className="font-bold text-xl text-slate-900">{step.stage}</h5>
                      <Badge variant="outline" className="w-fit bg-purple-50 border-purple-200 text-purple-700">
                        <Clock className="w-3 h-3 mr-1" />
                        {step.duration}
                      </Badge>
                    </div>
                    <p className="text-slate-700 bg-gradient-to-br from-slate-50 to-purple-50 p-5 rounded-xl border border-slate-200 leading-relaxed shadow-sm">
                      {step.focus}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-red-100 rounded-lg">
                  <Target className="w-5 h-5 text-red-600" />
                </div>
                Priority Skills
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {data?.development_roadmap?.priority_skills?.map((skill: any, idx: number) => (
                  <Badge 
                    key={idx} 
                    className={`px-4 py-2 ${
                      skill.priority === 'High' 
                        ? 'bg-gradient-to-r from-red-500 to-orange-600 hover:from-red-600 hover:to-orange-700' 
                        : 'bg-gradient-to-r from-slate-500 to-slate-600 hover:from-slate-600 hover:to-slate-700'
                    } shadow-sm hover:shadow-md transition-all`}
                  >
                    {skill.skill}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <BookOpen className="w-5 h-5 text-blue-600" />
                </div>
                Recommended Resources
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {data?.development_roadmap?.resource_recommendations?.['Online Courses']?.slice(0, 4).map((course: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 text-sm text-slate-700 p-3 bg-gradient-to-r from-slate-50 to-blue-50 rounded-lg hover:shadow-md transition-all border border-slate-100">
                    <div className="bg-blue-500 p-1.5 rounded-lg mt-0.5 shadow-sm">
                      <BookOpen className="w-3.5 h-3.5 text-white" />
                    </div>
                    <span className="leading-relaxed">{course}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-red-50 to-orange-50 hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg text-red-800 flex items-center gap-3">
                <div className="p-2 bg-red-100 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-red-600" />
                </div>
                Critical Skill Gaps
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {Object.entries(data?.skill_gap_analysis?.skill_gaps || {}).slice(0, 4).map(([skill, priority]: [string, any], idx) => (
                <div key={idx} className="flex justify-between items-center p-4 bg-white/80 backdrop-blur rounded-xl border border-red-100 hover:border-red-200 transition-colors shadow-sm">
                  <span className="font-semibold text-slate-700">{skill}</span>
                  <Badge className="bg-gradient-to-r from-red-500 to-orange-600 font-bold">
                    {priority.split('-')[0]}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-50 to-indigo-50 hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg text-blue-800 flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Briefcase className="w-5 h-5 text-blue-600" />
                </div>
                Portfolio Projects
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {data?.portfolio_projects?.slice(0, 2).map((project: any, idx: number) => (
                <div key={idx} className="bg-white/80 backdrop-blur p-4 rounded-xl border border-blue-100 hover:border-blue-200 transition-colors shadow-sm">
                  <span className="font-bold block text-slate-900 mb-3 text-base">{project.project}</span>
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech: string, i: number) => (
                      <span key={i} className="text-xs bg-blue-100 px-2.5 py-1 rounded-full text-blue-700 font-medium border border-blue-200">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    );
  };

  const renderOpportunities = (data: any) => {
    return (
      <div className="grid gap-6">
        {data?.matched_opportunities?.map((job: any, idx: number) => (
          <Card key={idx} className="border-0 shadow-lg hover:shadow-2xl transition-all duration-300 group overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500" />
            <CardContent className="p-8">
              <div className="flex flex-col md:flex-row justify-between items-start gap-6 mb-6">
                <div className="flex-1">
                  <h4 className="font-bold text-2xl text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">{job.title}</h4>
                  <p className="text-slate-600 font-semibold text-lg">{job.company}</p>
                </div>
                <Badge className="bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 shadow-md text-base px-4 py-2">
                  {job.type}
                </Badge>
              </div>
              
              <div className="flex items-center gap-4 text-sm text-slate-500 mb-5">
                <span className="flex items-center gap-2 bg-slate-100 px-3 py-2 rounded-lg font-medium">
                  <Globe className="w-4 h-4" /> {job.location}
                </span>
              </div>
              
              <p className="text-slate-700 leading-relaxed mb-6 text-base">{job.description}</p>
              
              {data.compatibility_analysis?.[`${job.company} ${job.title}`] && (
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 text-green-900 text-sm p-5 rounded-xl flex gap-4 hover:border-green-300 transition-colors">
                  <div className="p-2 bg-green-100 rounded-lg shrink-0">
                    <Zap className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <span className="font-bold block mb-2 text-base text-green-900">Match Analysis</span>
                    <p className="leading-relaxed">{data.compatibility_analysis[`${job.company} ${job.title}`]}</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    );
  };

  const renderCareerOptimization = (data: any) => {
    return (
      <div className="space-y-8">
        <div className="grid md:grid-cols-2 gap-6">
          {data?.career_goals?.map((goal: any, idx: number) => (
            <Card key={idx} className="border-0 border-l-4 border-l-blue-600 shadow-lg hover:shadow-xl transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex justify-between items-start mb-4">
                  <h4 className="font-bold text-xl text-slate-900">{goal.goal_title}</h4>
                  <Badge className={`${
                    goal.priority === 'High' 
                      ? 'bg-gradient-to-r from-red-500 to-orange-600' 
                      : 'bg-gradient-to-r from-blue-500 to-indigo-600'
                  } shadow-sm`}>
                    {goal.priority}
                  </Badge>
                </div>
                <p className="text-sm text-slate-600 mb-5 leading-relaxed">{goal.description}</p>
                <div className="bg-gradient-to-br from-slate-50 to-blue-50 p-4 rounded-xl border border-slate-200">
                  <p className="font-bold text-sm text-slate-900 mb-3 flex items-center gap-2">
                    <Target className="w-4 h-4 text-blue-600" />
                    Success Metrics:
                  </p>
                  <ul className="space-y-2">
                    {goal.success_metrics?.map((metric: string, i: number) => (
                      <li key={i} className="text-sm text-slate-700 flex items-start gap-2 leading-relaxed">
                        <CheckCircle2 className="w-4 h-4 text-blue-600 mt-0.5 shrink-0" />
                        {metric}
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-600 border-0 shadow-xl text-white">
          <CardHeader>
            <CardTitle className="text-white text-xl flex items-center gap-3">
              <div className="p-2 bg-white/20 rounded-lg backdrop-blur">
                <Flag className="w-6 h-6" />
              </div>
              Career Strategy
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="bg-white/10 backdrop-blur p-5 rounded-xl">
              <span className="text-xs font-bold text-blue-100 uppercase tracking-wider block mb-2">Short Term Strategy</span>
              <p className="text-white font-semibold text-base leading-relaxed">{data?.career_strategy?.short_term_strategy}</p>
            </div>
            <Separator className="bg-white/20" />
            <div className="bg-white/10 backdrop-blur p-5 rounded-xl">
              <span className="text-xs font-bold text-blue-100 uppercase tracking-wider block mb-2">Long Term Vision</span>
              <p className="text-white text-base italic leading-relaxed">"{data?.career_strategy?.long_term_vision}"</p>
            </div>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Users className="w-5 h-5 text-blue-600" />
                </div>
                Networking Plan
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {data?.networking_plan?.networking_goals?.map((goal: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 text-sm text-slate-700 p-3 bg-gradient-to-r from-slate-50 to-blue-50 rounded-lg hover:shadow-md transition-all border border-slate-100">
                    <div className="bg-blue-500 p-1.5 rounded-lg mt-0.5 shadow-sm">
                      <CheckCircle2 className="w-3.5 h-3.5 text-white" />
                    </div>
                    <span className="leading-relaxed">{goal}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Sparkles className="w-5 h-5 text-purple-600" />
                </div>
                Personal Branding
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-5 rounded-xl border border-purple-200">
                <p className="text-sm text-slate-700 italic text-center leading-relaxed font-medium">"{data?.personal_branding?.brand_positioning}"</p>
              </div>
              <div>
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-3">Thought Leadership Areas</span>
                <div className="flex flex-wrap gap-2">
                  {data?.personal_branding?.thought_leadership_areas?.map((area: string, idx: number) => (
                    <Badge key={idx} className="bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-600 hover:to-indigo-700 shadow-sm">
                      {area}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Clock className="w-6 h-6 text-orange-600" />
              </div>
              Monthly Action Plan
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-3">
              {Object.entries(data?.monthly_action_plan || {}).slice(0, 3).map(([month, actions]: [string, any]) => (
                <div key={month} className="border-2 border-slate-200 rounded-xl p-5 hover:bg-gradient-to-br hover:from-slate-50 hover:to-blue-50 hover:border-blue-300 transition-all">
                  <h5 className="font-bold text-slate-900 mb-4 pb-3 border-b-2 border-slate-200 text-lg">{month}</h5>
                  <ul className="space-y-3">
                    {actions.map((action: string, i: number) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2 leading-relaxed">
                        <ChevronRight className="w-4 h-4 text-blue-600 mt-0.5 shrink-0" />
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  };

  const sections = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'profile', label: 'Profile Analysis', icon: FileText },
    { id: 'market', label: 'Market Intelligence', icon: Globe },
    { id: 'skills', label: 'Skill Strategy', icon: BookOpen },
    { id: 'career', label: 'Career Plan', icon: Flag },
    { id: 'opportunities', label: 'Opportunities', icon: Briefcase },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex flex-col">
      <div className="bg-white/80 backdrop-blur-lg border-b border-slate-200 sticky top-0 z-20 shadow-sm">
        <div className="w-full px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/')} className="hover:bg-slate-100">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="font-bold text-lg text-slate-900">Career Analysis Report</h1>
              <p className="text-xs text-slate-500">Powered by AI</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 shadow-sm px-3 py-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" />
              Complete
            </Badge>
            <Button variant="outline" size="sm" className="hidden md:flex gap-2 hover:bg-blue-50 hover:border-blue-300">
              <Download className="w-4 h-4" />
              Export
            </Button>
            <Button variant="outline" size="sm" className="hidden md:flex gap-2 hover:bg-purple-50 hover:border-purple-300">
              <Share2 className="w-4 h-4" />
              Share
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-64 bg-white/80 backdrop-blur-lg border-r border-slate-200 hidden md:flex flex-col shadow-sm">
          <div className="p-4 space-y-2">
            {sections.map((section) => (
              <Button
                key={section.id}
                variant={activeSection === section.id ? "secondary" : "ghost"}
                className={`w-full justify-start gap-3 transition-all ${
                  activeSection === section.id 
                    ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 border border-blue-200 shadow-sm' 
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
                onClick={() => setActiveSection(section.id)}
              >
                <section.icon className="w-4 h-4" />
                {section.label}
              </Button>
            ))}
          </div>
        </div>

        <div className="flex-1 overflow-auto">
          <div className="max-w-6xl mx-auto p-6 md:p-8">
            {result && (
              <div className="space-y-8">
                {activeSection === 'overview' && (
                  <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div>
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Executive Summary</h2>
                      <p className="text-slate-600">Your comprehensive career analysis at a glance</p>
                    </div>
                    
                    <Card className="border-0 border-l-4 border-l-blue-600 shadow-xl bg-gradient-to-br from-white to-blue-50">
                      <CardContent className="p-8">
                        <div className="flex items-start gap-4">
                          <div className="p-3 bg-blue-100 rounded-xl">
                            <Sparkles className="w-6 h-6 text-blue-600" />
                          </div>
                          <p className="text-lg text-slate-700 leading-relaxed flex-1">
                            {result.outputs.agent_outputs.profile_analysis?.data?.comprehensive_analysis?.profile_summary || 
                             "Analysis completed successfully. Please review the detailed recommendations below."}
                          </p>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Quick Stats / Highlights Row */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      <Card className="bg-green-50 border-green-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-green-700 font-semibold text-sm">
                            <Award className="w-4 h-4" /> Top Strength
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {result.outputs.agent_outputs.profile_analysis?.data?.comprehensive_analysis?.key_strengths?.[0] || "N/A"}
                          </p>
                        </CardContent>
                      </Card>
                      
                      <Card className="bg-orange-50 border-orange-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-orange-700 font-semibold text-sm">
                            <AlertCircle className="w-4 h-4" /> Focus Area
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {Object.keys(result.outputs.agent_outputs.skill_development_strategist?.data?.skill_gap_analysis?.skill_gaps || {})[0] || "N/A"}
                          </p>
                        </CardContent>
                      </Card>

                      <Card className="bg-blue-50 border-blue-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-blue-700 font-semibold text-sm">
                            <Flag className="w-4 h-4" /> Primary Goal
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {result.outputs.agent_outputs.career_optimization_planner?.data?.career_goals?.[0]?.goal_title || "N/A"}
                          </p>
                        </CardContent>
                      </Card>

                      <Card className="bg-purple-50 border-purple-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-purple-700 font-semibold text-sm">
                            <Briefcase className="w-4 h-4" /> Top Match
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {result.outputs.agent_outputs.opportunity_matcher?.data?.matched_opportunities?.[0]?.title || "N/A"}
                          </p>
                        </CardContent>
                      </Card>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <Card className="border-0 shadow-lg bg-gradient-to-br from-white to-indigo-50 hover:shadow-xl transition-all duration-300">
                        <CardHeader>
                          <CardTitle className="flex items-center gap-3 text-xl">
                            <div className="p-2 bg-indigo-100 rounded-lg">
                              <Target className="w-6 h-6 text-indigo-600" />
                            </div>
                            Key Recommendations
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-3">
                            {result.outputs.fleet_summary.recommendations?.slice(0, 5).map((rec, idx) => (
                              <li key={idx} className="flex items-start gap-3 bg-white/80 backdrop-blur p-4 rounded-xl border border-slate-100 hover:border-indigo-200 transition-colors shadow-sm">
                                <div className="bg-gradient-to-br from-green-400 to-emerald-600 p-1.5 rounded-lg mt-0.5 shadow-sm">
                                  <CheckCircle2 className="w-4 h-4 text-white" />
                                </div>
                                <span className="text-slate-700 leading-relaxed">{rec}</span>
                              </li>
                            )) || <p className="text-slate-500 italic">No specific recommendations found.</p>}
                          </ul>
                        </CardContent>
                      </Card>

                      <Card className="border-0 shadow-lg bg-gradient-to-br from-white to-emerald-50 hover:shadow-xl transition-all duration-300">
                        <CardHeader>
                          <CardTitle className="flex items-center gap-3 text-xl">
                            <div className="p-2 bg-emerald-100 rounded-lg">
                              <TrendingUp className="w-6 h-6 text-emerald-600" />
                            </div>
                            Next Actions
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-3">
                            {result.outputs.fleet_summary.next_actions?.slice(0, 5).map((action, idx) => (
                              <li key={idx} className="flex items-start gap-3 bg-white/80 backdrop-blur p-4 rounded-xl border border-slate-100 hover:border-emerald-200 transition-colors shadow-sm">
                                <Badge className="bg-gradient-to-r from-blue-500 to-indigo-600 shrink-0 mt-0.5 shadow-sm">
                                  {idx + 1}
                                </Badge>
                                <span className="text-slate-700 leading-relaxed">{action}</span>
                              </li>
                            )) || <p className="text-slate-500 italic">No next actions found.</p>}
                          </ul>
                        </CardContent>
                      </Card>
                    </div>

                    {/* Top Opportunities Preview */}
                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-bold text-slate-900">Top Matched Opportunities</h3>
                        <Button variant="ghost" className="text-blue-600 hover:text-blue-700 hover:bg-blue-50" onClick={() => setActiveSection('opportunities')}>
                          View All <ChevronRight className="w-4 h-4 ml-1" />
                        </Button>
                      </div>
                      <div className="grid md:grid-cols-2 gap-6">
                        {result.outputs.agent_outputs.opportunity_matcher?.data?.matched_opportunities?.slice(0, 2).map((job: any, idx: number) => (
                          <Card key={idx} className="border-0 shadow-md hover:shadow-lg transition-all cursor-pointer" onClick={() => setActiveSection('opportunities')}>
                            <CardContent className="p-6">
                              <div className="flex justify-between items-start mb-3">
                                <div>
                                  <h4 className="font-bold text-lg text-slate-900">{job.title}</h4>
                                  <p className="text-slate-600 font-medium">{job.company}</p>
                                </div>
                                <Badge variant="secondary">{job.type}</Badge>
                              </div>
                              <p className="text-slate-600 text-sm line-clamp-2 mb-3">{job.description}</p>
                              <div className="flex items-center text-sm text-blue-600 font-medium">
                                View Details <ArrowLeft className="w-4 h-4 ml-1 rotate-180" />
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeSection === 'profile' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Profile Analysis</h2>
                      <p className="text-slate-600">Deep dive into your professional profile</p>
                    </div>
                    {result.outputs.agent_outputs.profile_analysis && 
                      renderProfileAnalysis(result.outputs.agent_outputs.profile_analysis.data)}
                  </div>
                )}

                {activeSection === 'market' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Market Intelligence</h2>
                      <p className="text-slate-600">Current industry trends and insights</p>
                    </div>
                    {result.outputs.agent_outputs.market_intelligence && 
                      renderMarketIntelligence(result.outputs.agent_outputs.market_intelligence.data)}
                  </div>
                )}

                {activeSection === 'skills' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Skill Development Strategy</h2>
                      <p className="text-slate-600">Your personalized learning roadmap</p>
                    </div>
                    {result.outputs.agent_outputs.skill_development_strategist && 
                      renderSkillStrategy(result.outputs.agent_outputs.skill_development_strategist.data)}
                  </div>
                )}

                {activeSection === 'career' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Career Optimization Plan</h2>
                      <p className="text-slate-600">Strategic plan for your career growth</p>
                    </div>
                    {result.outputs.agent_outputs.career_optimization_planner && 
                      renderCareerOptimization(result.outputs.agent_outputs.career_optimization_planner.data)}
                  </div>
                )}

                {activeSection === 'opportunities' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Matched Opportunities</h2>
                      <p className="text-slate-600">Curated positions that align with your profile</p>
                    </div>
                    {result.outputs.agent_outputs.opportunity_matcher && 
                      renderOpportunities(result.outputs.agent_outputs.opportunity_matcher.data)}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CollegeAnalysisResult;