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
  Brain, 
  Target, 
  TrendingUp, 
  GraduationCap, 
  Briefcase, 
  Map, 
  Building, 
  Award,
  LayoutDashboard,
  ChevronRight,
  BookOpen,
  Sparkles,
  Download,
  Share2
} from 'lucide-react';
import { mockSchoolAssessmentData } from '../schoolAssessmentMockData';

const SchoolAssessmentResults = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get('session_id');
  const [status, setStatus] = useState<'pending' | 'processing' | 'completed' | 'failed'>('pending');
  const [result, setResult] = useState<typeof mockSchoolAssessmentData['data']['results'] | null>(null);
  const [error] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    if (!sessionId) {
      // Use mock data if no session ID
      setStatus('completed');
      setResult(mockSchoolAssessmentData.data.results);
      setProgress(100);
      return;
    }

    // Simulate loading
    setStatus('processing');
    let p = 0;
    const interval = setInterval(() => {
      p += 10;
      setProgress(p);
      if (p >= 100) {
        clearInterval(interval);
        setStatus('completed');
        setResult(mockSchoolAssessmentData.data.results);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [sessionId]);

  if (status === 'pending' || status === 'processing') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Analyzing Your Assessment</CardTitle>
            <CardDescription>Our AI agents are evaluating your aptitude and interests...</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex justify-center">
              <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
            </div>
            <div className="space-y-2">
              <Progress value={progress} className="h-2" />
              <p className="text-sm text-center text-slate-500">
                {progress < 30 ? 'Calculating aptitude scores...' : 
                 progress < 60 ? 'Analyzing interest patterns...' : 
                 'Generating stream recommendations...'}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (status === 'failed') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <Card className="w-full max-w-md border-red-200">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>
            <CardTitle className="text-red-700">Analysis Failed</CardTitle>
            <CardDescription>We couldn't complete your assessment analysis.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-center text-slate-600">{error}</p>
            <Button onClick={() => navigate('/school-assessment')} className="w-full">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const renderAptitudeAnalysis = (data: any) => {
    const analysis = data?.aptitude_analysis;
    const interests = data?.interest_analysis;
    const scoreSummaries = data?.score_summaries;
    
    if (!analysis) return null;

    return (
      <div className="space-y-8">
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Brain className="w-5 h-5 text-blue-600" />
                Aptitude Profile
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(analysis).map(([key, value]: [string, any]) => (
                <div key={key} className="bg-slate-50 p-4 rounded-lg">
                  <h4 className="font-medium text-slate-900 mb-1 capitalize">{key.replace(/_/g, ' ')}</h4>
                  <p className="text-sm text-slate-600">{value}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          {interests && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Target className="w-5 h-5 text-indigo-600" />
                  Interest Profile
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(interests).map(([key, value]: [string, any]) => (
                  <div key={key} className="bg-slate-50 p-4 rounded-lg">
                    <h4 className="font-medium text-slate-900 mb-1 capitalize">{key.replace(/_/g, ' ')}</h4>
                    <p className="text-sm text-slate-600">{value}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>

        {scoreSummaries && (
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="border-blue-100 bg-blue-50/50">
              <CardHeader>
                <CardTitle className="text-base text-blue-900">Top Aptitudes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {scoreSummaries.dbda_top_aptitudes?.map((item: any, idx: number) => (
                  <div key={idx} className="flex justify-between items-center bg-white p-3 rounded-md border border-blue-100">
                    <span className="text-slate-700 font-medium capitalize">{item.domain.replace(/_/g, ' ')}</span>
                    <Badge className="bg-blue-600">{item.level}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
            <Card className="border-green-100 bg-green-50/50">
              <CardHeader>
                <CardTitle className="text-base text-green-900">Top Interests</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {scoreSummaries.cii_top_interests?.map((item: any, idx: number) => (
                  <div key={idx} className="flex justify-between items-center bg-white p-3 rounded-md border border-green-100">
                    <span className="text-slate-700 font-medium capitalize">{item.domain.replace(/_/g, ' ')}</span>
                    <Badge variant="outline" className="text-green-700 border-green-200 bg-green-50">{item.level}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    );
  };

  const renderStreamRecommendations = (data: any) => {
    const recommendations = data?.recommended_streams;
    if (!recommendations) return null;

    return (
      <div className="space-y-6">
        {recommendations.map((rec: any, idx: number) => (
          <Card key={idx} className="overflow-hidden hover:shadow-md transition-shadow">
            <div className="bg-slate-50 p-4 border-b flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold">
                  {idx + 1}
                </div>
                <h4 className="font-bold text-lg text-slate-900">{rec.stream_type}</h4>
              </div>
              <Badge variant={idx === 0 ? 'default' : 'secondary'} className="text-sm px-3 py-1">
                Fit Score: {Math.round(rec.suitability_score * 100)}%
              </Badge>
            </div>
            
            <CardContent className="p-6 space-y-6">
              <div>
                <h5 className="font-semibold text-sm mb-2 text-slate-900 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-600" />
                  Why this stream?
                </h5>
                <ul className="grid md:grid-cols-2 gap-2">
                  {rec.primary_strengths_supporting?.map((strength: string, i: number) => (
                    <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-300 mt-1.5 shrink-0" />
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>
              
              <Separator />

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h5 className="font-semibold text-sm mb-3 text-slate-900">Key Subjects</h5>
                  <div className="flex flex-wrap gap-2">
                    {rec.subject_requirements?.map((sub: string, i: number) => (
                      <Badge key={i} variant="secondary" className="bg-slate-100 text-slate-700 hover:bg-slate-200">
                        {sub}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <h5 className="font-semibold text-sm mb-3 text-slate-900">Career Paths</h5>
                  <ul className="space-y-1">
                    {rec.career_pathways?.slice(0, 3).map((path: string, i: number) => (
                      <li key={i} className="text-sm text-slate-600 flex items-center gap-2">
                        <ChevronRight className="w-3 h-3 text-slate-400" />
                        {path}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  };

  const renderCareerPathways = (data: any) => {
    const pathways = data?.recommended_career_pathways;
    if (!pathways) return null;

    return (
      <div className="grid gap-6">
        {pathways.map((path: any, idx: number) => (
          <Card key={idx} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-xl text-slate-900">{path.career_title}</CardTitle>
                  <CardDescription className="mt-1">{path.career_field}</CardDescription>
                </div>
                <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                  Match: {Math.round(path.suitability_score * 100)}%
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-slate-700 text-sm leading-relaxed bg-slate-50 p-3 rounded-md">
                {path.pathway_description}
              </p>
              
              <div className="grid md:grid-cols-2 gap-6 pt-2">
                <div>
                  <h5 className="font-semibold text-sm mb-2 flex items-center gap-2">
                    <GraduationCap className="w-4 h-4 text-slate-500" />
                    Education Required
                  </h5>
                  <ul className="space-y-1">
                    {path.educational_requirements?.map((req: string, i: number) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                        <span className="w-1 h-1 rounded-full bg-slate-400 mt-2 shrink-0" />
                        {req}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="font-semibold text-sm mb-2 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-slate-500" />
                    Salary Outlook
                  </h5>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm p-2 bg-slate-50 rounded">
                      <span className="text-slate-600">Entry Level</span>
                      <span className="font-medium text-slate-900">{path.salary_outlook?.entry_level}</span>
                    </div>
                    <div className="flex justify-between text-sm p-2 bg-slate-50 rounded">
                      <span className="text-slate-600">Mid Career</span>
                      <span className="font-medium text-slate-900">{path.salary_outlook?.mid_career}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  };

  const renderEducationalRoadmap = (data: any) => {
    const milestones = data?.grade_wise_milestones;
    const examStrategies = data?.entrance_exam_strategies;
    
    if (!milestones) return null;

    return (
      <div className="space-y-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Map className="w-5 h-5 text-orange-600" />
              Grade-wise Milestones
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative border-l-2 border-slate-200 ml-3 space-y-10 pl-8 py-2">
              {milestones.map((milestone: any, idx: number) => (
                <div key={idx} className="relative">
                  <span className="absolute -left-[41px] top-0 w-6 h-6 rounded-full bg-white border-4 border-blue-600 shadow-sm" />
                  <h4 className="font-bold text-lg text-slate-900 mb-4">{milestone.grade}</h4>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                      <h5 className="font-semibold text-sm mb-3 text-blue-900 flex items-center gap-2">
                        <BookOpen className="w-4 h-4" />
                        Academic Focus
                      </h5>
                      <ul className="space-y-2">
                        {milestone.academic_focus?.map((focus: string, i: number) => (
                          <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-400 mt-1.5 shrink-0" />
                            {focus}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-indigo-50/50 p-4 rounded-lg border border-indigo-100">
                      <h5 className="font-semibold text-sm mb-3 text-indigo-900 flex items-center gap-2">
                        <Target className="w-4 h-4" />
                        Entrance Prep
                      </h5>
                      <ul className="space-y-2">
                        {milestone.entrance_exam_preparation?.map((prep: string, i: number) => (
                          <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                            {prep}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {examStrategies && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5 text-red-600" />
                Entrance Exam Strategy
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                {examStrategies.map((exam: any, idx: number) => (
                  <div key={idx} className="border rounded-lg p-4 hover:bg-slate-50 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-bold text-slate-900">{exam.exam_name}</h5>
                      <Badge variant="outline">{exam.difficulty_assessment}</Badge>
                    </div>
                    
                    <div className="space-y-3 mt-4">
                      <div>
                        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Timeline</span>
                        <p className="text-sm text-slate-700 mt-1">{exam.preparation_timeline}</p>
                      </div>
                      <div>
                        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Priority Subjects</span>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {exam.subject_priorities?.map((sub: string, i: number) => (
                            <Badge key={i} variant="secondary" className="text-xs">{sub}</Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  };

  const renderCollegeScholarships = (data: any) => {
    return (
      <div className="space-y-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building className="w-5 h-5 text-indigo-600" />
              Recommended Colleges
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              {data?.recommended_colleges?.map((college: any, idx: number) => (
                <div key={idx} className="border rounded-lg p-4 hover:shadow-sm transition-shadow">
                  <div className="flex justify-between items-start mb-3">
                    <h5 className="font-bold text-slate-900">{college.college_name}</h5>
                    <Badge>{college.college_type}</Badge>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                    <Map className="w-4 h-4" />
                    {college.location}
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="bg-slate-50 p-2 rounded">
                      <span className="font-semibold block text-slate-700">Programs</span>
                      <span className="text-slate-600">{college.programs_offered?.join(', ')}</span>
                    </div>
                    <div className="bg-slate-50 p-2 rounded">
                      <span className="font-semibold block text-slate-700">Entrance</span>
                      <span className="text-slate-600">{college.admission_requirements?.entrance_exam}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Award className="w-5 h-5 text-yellow-600" />
              Scholarship Opportunities
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2">
              {data?.scholarship_opportunities?.map((scholarship: any, idx: number) => (
                <div key={idx} className="bg-gradient-to-br from-yellow-50 to-orange-50 border border-yellow-100 rounded-lg p-5">
                  <h5 className="font-bold text-yellow-900 text-lg mb-1">{scholarship.scholarship_name}</h5>
                  <p className="text-sm text-yellow-700 font-medium mb-4">{scholarship.provider}</p>
                  
                  <div className="space-y-3">
                    <div className="flex items-start gap-2">
                      <div className="bg-white/50 p-1 rounded text-yellow-600">
                        <Award className="w-4 h-4" />
                      </div>
                      <div>
                        <span className="text-xs font-semibold text-yellow-800 uppercase">Benefit</span>
                        <p className="text-sm text-yellow-900">{scholarship.benefit_amount}</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-2">
                      <div className="bg-white/50 p-1 rounded text-yellow-600">
                        <CheckCircle2 className="w-4 h-4" />
                      </div>
                      <div>
                        <span className="text-xs font-semibold text-yellow-800 uppercase">Eligibility</span>
                        <p className="text-sm text-yellow-900">{scholarship.eligibility_criteria?.join(', ')}</p>
                      </div>
                    </div>
                  </div>
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
    { id: 'aptitude', label: 'Aptitude & Interests', icon: Brain },
    { id: 'streams', label: 'Stream Recommendations', icon: GraduationCap },
    { id: 'careers', label: 'Career Pathways', icon: Briefcase },
    { id: 'roadmap', label: 'Educational Roadmap', icon: Map },
    { id: 'colleges', label: 'Colleges & Scholarships', icon: Building },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex flex-col">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-lg border-b border-slate-200 sticky top-0 z-20 shadow-sm">
        <div className="w-full px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/')} className="hover:bg-slate-100">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="font-bold text-lg text-slate-900">Assessment Report</h1>
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
        {/* Sidebar Navigation */}
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

        {/* Main Content Area */}
        <div className="flex-1 overflow-auto">
          <div className="max-w-6xl mx-auto p-6 md:p-8">
            {result && (
              <div className="space-y-8">
                {activeSection === 'overview' && (
                  <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div>
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Executive Summary</h2>
                      <p className="text-slate-600">Your comprehensive assessment analysis at a glance</p>
                    </div>
                    
                    <Card className="border-0 border-l-4 border-l-blue-600 shadow-xl bg-gradient-to-br from-white to-blue-50">
                      <CardContent className="p-8">
                        <div className="flex items-start gap-4">
                          <div className="p-3 bg-blue-100 rounded-xl">
                            <Sparkles className="w-6 h-6 text-blue-600" />
                          </div>
                          <p className="text-lg text-slate-700 leading-relaxed flex-1">
                            {result.outputs.agent_outputs.test_score_interpreter?.data?.executive_summary}
                          </p>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Quick Stats / Highlights Row */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      <Card className="bg-blue-50 border-blue-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-blue-700 font-semibold text-sm">
                            <Brain className="w-4 h-4" /> Top Aptitude
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2 capitalize">
                            {result.outputs.agent_outputs.test_score_interpreter?.data?.score_summaries?.dbda_top_aptitudes?.[0]?.domain.replace(/_/g, ' ') || "N/A"}
                          </p>
                        </CardContent>
                      </Card>
                      
                      <Card className="bg-indigo-50 border-indigo-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-indigo-700 font-semibold text-sm">
                            <Target className="w-4 h-4" /> Top Interest
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2 capitalize">
                            {result.outputs.agent_outputs.test_score_interpreter?.data?.score_summaries?.cii_top_interests?.[0]?.domain.replace(/_/g, ' ') || "N/A"}
                          </p>
                        </CardContent>
                      </Card>

                      <Card className="bg-green-50 border-green-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-green-700 font-semibold text-sm">
                            <GraduationCap className="w-4 h-4" /> Best Stream
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {result.outputs.agent_outputs.academic_stream_advisor?.data?.recommended_streams?.[0]?.stream_type || "N/A"}
                          </p>
                        </CardContent>
                      </Card>

                      <Card className="bg-purple-50 border-purple-100 shadow-sm hover:shadow-md transition-all">
                        <CardContent className="p-4 flex flex-col gap-2">
                          <div className="flex items-center gap-2 text-purple-700 font-semibold text-sm">
                            <Briefcase className="w-4 h-4" /> Top Career
                          </div>
                          <p className="text-slate-900 font-medium line-clamp-2">
                            {result.outputs.agent_outputs.career_pathway_explorer?.data?.recommended_career_pathways?.[0]?.career_title || "N/A"}
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

                    {/* Top Stream Preview */}
                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-bold text-slate-900">Top Recommended Stream</h3>
                        <Button variant="ghost" className="text-blue-600 hover:text-blue-700 hover:bg-blue-50" onClick={() => setActiveSection('streams')}>
                          View All <ChevronRight className="w-4 h-4 ml-1" />
                        </Button>
                      </div>
                      {result.outputs.agent_outputs.academic_stream_advisor?.data?.recommended_streams?.[0] && (
                        <Card className="border-0 shadow-md hover:shadow-lg transition-all cursor-pointer bg-gradient-to-r from-slate-50 to-blue-50" onClick={() => setActiveSection('streams')}>
                          <CardContent className="p-6">
                            <div className="flex justify-between items-center mb-4">
                              <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xl shadow-sm">
                                  1
                                </div>
                                <div>
                                  <h4 className="font-bold text-xl text-slate-900">
                                    {result.outputs.agent_outputs.academic_stream_advisor.data.recommended_streams[0].stream_type}
                                  </h4>
                                  <Badge variant="secondary" className="mt-1">
                                    Fit Score: {Math.round(result.outputs.agent_outputs.academic_stream_advisor.data.recommended_streams[0].suitability_score * 100)}%
                                  </Badge>
                                </div>
                              </div>
                              <ChevronRight className="w-6 h-6 text-slate-400" />
                            </div>
                            <div className="grid md:grid-cols-2 gap-6">
                              <div>
                                <h5 className="font-semibold text-sm mb-2 text-slate-900">Why this stream?</h5>
                                <ul className="space-y-1">
                                  {result.outputs.agent_outputs.academic_stream_advisor.data.recommended_streams[0].primary_strengths_supporting?.slice(0, 3).map((strength: string, i: number) => (
                                    <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                                      <CheckCircle2 className="w-3.5 h-3.5 text-green-600 mt-0.5 shrink-0" />
                                      {strength}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              <div>
                                <h5 className="font-semibold text-sm mb-2 text-slate-900">Career Paths</h5>
                                <div className="flex flex-wrap gap-2">
                                  {result.outputs.agent_outputs.academic_stream_advisor.data.recommended_streams[0].career_pathways?.slice(0, 4).map((path: string, i: number) => (
                                    <Badge key={i} variant="outline" className="bg-white">
                                      {path}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      )}
                    </div>
                  </div>
                )}

                {activeSection === 'aptitude' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Aptitude & Interest Analysis</h2>
                      <p className="text-slate-600">Detailed breakdown of your cognitive strengths and interests</p>
                    </div>
                    {result.outputs.agent_outputs.test_score_interpreter && 
                      renderAptitudeAnalysis(result.outputs.agent_outputs.test_score_interpreter.data)}
                  </div>
                )}

                {activeSection === 'streams' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Recommended Streams</h2>
                      <p className="text-slate-600">Academic paths aligned with your profile</p>
                    </div>
                    {result.outputs.agent_outputs.academic_stream_advisor && 
                      renderStreamRecommendations(result.outputs.agent_outputs.academic_stream_advisor.data)}
                  </div>
                )}

                {activeSection === 'careers' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Career Pathways</h2>
                      <p className="text-slate-600">Future career options to explore</p>
                    </div>
                    {result.outputs.agent_outputs.career_pathway_explorer && 
                      renderCareerPathways(result.outputs.agent_outputs.career_pathway_explorer.data)}
                  </div>
                )}

                {activeSection === 'roadmap' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Educational Roadmap</h2>
                      <p className="text-slate-600">Step-by-step guide for your academic journey</p>
                    </div>
                    {result.outputs.agent_outputs.educational_roadmap_planner && 
                      renderEducationalRoadmap(result.outputs.agent_outputs.educational_roadmap_planner.data)}
                  </div>
                )}

                {activeSection === 'colleges' && (
                  <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <div className="mb-8">
                      <h2 className="text-3xl font-bold text-slate-900 mb-2">Colleges & Scholarships</h2>
                      <p className="text-slate-600">Higher education opportunities</p>
                    </div>
                    {result.outputs.agent_outputs.college_scholarship_navigator && 
                      renderCollegeScholarships(result.outputs.agent_outputs.college_scholarship_navigator.data)}
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

export default SchoolAssessmentResults;
