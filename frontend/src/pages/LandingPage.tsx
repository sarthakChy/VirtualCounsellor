import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Compass, GraduationCap, Briefcase, Target, TrendingUp, Shield, Map, Code, Award, BookOpen, ArrowRight, Sparkles, Brain, Zap, CheckCircle2 } from 'lucide-react';
import AssessmentModal from '@/components/ui/assesmentModel';

const LandingPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleAssessmentSelect = (type: 'school' | 'college' | 'professional') => {
    setIsModalOpen(false);
    // Navigate to respective assessment page
    if (type === 'school') {
      window.location.href = '/school-assessment';
    } else if (type === 'college') {
      window.location.href = '/college-assessment';
    } else {
      window.location.href = '/professional-assessment';
    }
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offset = -10; // Account for sticky navbar
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  return (
    <div className="min-h-screen bg-background scroll-smooth">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 flex h-16 items-center justify-between max-w-7xl">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
              <Compass className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">Virtual Counsellor</span>
          </div>
          <div className="flex items-center gap-6">
            <div className="hidden md:flex items-center gap-6">
              <button 
                onClick={() => scrollToSection('students')}
                className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
              >
                For Students
              </button>
              <button 
                onClick={() => scrollToSection('college')}
                className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
              >
                For College
              </button>
              <button 
                onClick={() => scrollToSection('professionals')}
                className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
              >
                For Professionals
              </button>
            </div>
            <Button className="shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all cursor-pointer" onClick={() => setIsModalOpen(true)}>
              Start Your Assessment
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5"></div>
        <div className="container mx-auto px-4 py-10 md:py-10 max-w-7xl relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20 hover:bg-primary/20">
                <Sparkles className="w-3 h-3 mr-1" />
                AI-Powered Career Guidance
              </Badge>
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-tight">
                Your Career Roadmap,
                <span className="block mt-2 bg-gradient-to-r from-primary via-primary to-secondary bg-clip-text text-transparent">
                  Powered by Agentic AI
                </span>
              </h1>
              <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-xl">
                Move beyond generic advice. Combine psychometric science with real-time market data for a personalized, actionable plan.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-2">
                <Button size="lg" className="text-base h-14 px-8 shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all group cursor-pointer" onClick={() => setIsModalOpen(true)}>
                  Find My Path
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
                <Button size="lg" variant="outline" className="text-base h-14 px-8 border-2 cursor-pointer">
                  Watch Demo
                </Button>
              </div>
              <div className="flex items-center gap-8 pt-4">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">No Credit Card</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">Free Assessment</span>
                </div>
              </div>
            </div>
            <div className="relative h-[450px] lg:h-[550px]">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-primary/10 to-secondary/20 rounded-3xl transform rotate-3"></div>
              <div className="absolute inset-0 bg-gradient-to-tl from-secondary/20 via-primary/10 to-primary/20 rounded-3xl transform -rotate-3"></div>
              <div className="absolute inset-4 bg-background/80 backdrop-blur-sm rounded-3xl flex items-center justify-center p-8 border border-primary/10">
                <div className="grid grid-cols-3 gap-4 w-full max-w-sm">
                  {[...Array(9)].map((_, i) => (
                    <div
                      key={i}
                      className="aspect-square bg-gradient-to-br from-primary/30 to-secondary/30 rounded-2xl animate-pulse shadow-lg"
                      style={{ 
                        animationDelay: `${i * 0.15}s`, 
                        animationDuration: '2s',
                        transform: `scale(${1 - i * 0.02})`
                      }}
                    ></div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Choose Your Path Section */}
      <section className="py-20 md:py-24 bg-muted/30">
        <div className="container mx-auto px-4 max-w-7xl space-y-12">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
              <Brain className="w-3 h-3 mr-1" />
              Personalized for Every Stage
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold">
              Choose Your Journey
            </h2>
            <p className="text-lg text-muted-foreground">
              Tailored guidance for every stage of your career path
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
              <CardContent className="pt-8 pb-8 space-y-6">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Compass className="w-8 h-8 text-primary" />
                </div>
                <div className="space-y-3">
                  <h3 className="text-2xl font-bold">For School Students</h3>
                  <p className="text-sm font-semibold text-primary">Choosing Your Stream?</p>
                  <p className="text-muted-foreground leading-relaxed">
                    Navigate high school with confidence. AI analyzes your aptitude to recommend academic streams.
                  </p>
                </div>
                <Button 
                  variant="ghost" 
                  onClick={() => scrollToSection('students')}
                  className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors cursor-pointer"
                >
                  Learn More
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
              <CardContent className="pt-8 pb-8 space-y-6">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-secondary/20 to-secondary/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <GraduationCap className="w-8 h-8 text-primary" />
                </div>
                <div className="space-y-3">
                  <h3 className="text-2xl font-bold">For University Students</h3>
                  <p className="text-sm font-semibold text-primary">Ready to Upskill?</p>
                  <p className="text-muted-foreground leading-relaxed">
                    Bridge the gap between college and career. Get a roadmap of courses and certifications.
                  </p>
                </div>
                <Button 
                  variant="ghost" 
                  onClick={() => scrollToSection('college')}
                  className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors cursor-pointer"
                >
                  Learn More
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
              <CardContent className="pt-8 pb-8 space-y-6">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Briefcase className="w-8 h-8 text-primary" />
                </div>
                <div className="space-y-3">
                  <h3 className="text-2xl font-bold">For Professionals</h3>
                  <p className="text-sm font-semibold text-primary">Career Switch?</p>
                  <p className="text-muted-foreground leading-relaxed">
                    Make your next move count. AI analyzes skills to find fulfilling career transitions.
                  </p>
                </div>
                <Button 
                  variant="ghost" 
                  onClick={() => scrollToSection('professionals')}
                  className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors cursor-pointer"
                >
                  Learn More
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* School Students Section */}
      <section id="students" className="py-20 md:py-24 scroll-mt-16">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8 order-2 lg:order-1">
              <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
                For School Students
              </Badge>
              <h2 className="text-4xl md:text-5xl font-bold">
                Find Your Perfect Academic Stream
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Science, Commerce, or Arts? Make the right choice based on your strengths and interests.
              </p>
              
              <div className="space-y-4">
                {[
                  { icon: Target, title: 'Stream Selection', desc: 'Personalized recommendations for Science, Commerce, or Arts' },
                  { icon: BookOpen, title: 'Subject Guidance', desc: 'Discover which subjects align with your natural abilities' },
                  { icon: TrendingUp, title: 'Future Planning', desc: 'Explore career paths and college options' }
                ].map((item, i) => (
                  <div key={i} className="flex gap-4 p-4 rounded-xl hover:bg-muted/50 transition-colors">
                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <item.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold mb-1">{item.title}</h4>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>

              <Button size="lg" className="shadow-lg shadow-primary/25 cursor-pointer" onClick={() => setIsModalOpen(true)}>
                Start Assessment
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>

            <div className="order-1 lg:order-2">
              <Card className="border-2 border-primary/20 shadow-2xl shadow-primary/10 overflow-hidden">
                <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 border-b">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold">Your Journey</h3>
                    <Badge variant="secondary" className="text-xs">3 Steps</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    A simple, guided path to finding your perfect academic stream
                  </p>
                </div>
                <CardContent className="p-8 space-y-8">
                  {[
                    { step: 1, title: 'Take Assessment', desc: 'Complete our comprehensive aptitude test', color: 'bg-[#146C94]', icon: Target },
                    { step: 2, title: 'Get Recommendations', desc: 'Receive personalized stream suggestions', color: 'bg-[#19A7CE]', icon: Sparkles },
                    { step: 3, title: 'Plan Your Future', desc: 'Access detailed career roadmaps', color: 'bg-[#AFD3E2]', icon: Map }
                  ].map((item) => (
                    <div key={item.step} className="flex gap-4 items-start group hover:translate-x-2 transition-transform">
                      <div className={`w-14 h-14 rounded-2xl ${item.color} text-white flex items-center justify-center font-bold text-xl flex-shrink-0 shadow-lg group-hover:shadow-xl transition-all`}>
                        <item.icon className="w-7 h-7" />
                      </div>
                      <div className="pt-1 space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-muted-foreground">STEP {item.step}</span>
                        </div>
                        <h4 className="font-bold text-lg">{item.title}</h4>
                        <p className="text-sm text-muted-foreground">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* College Students Section */}
      <section id="college" className="py-20 md:py-24 bg-gradient-to-br from-primary/5 to-secondary/5 scroll-mt-16">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-3xl blur-2xl"></div>
                <Card className="border-2 border-primary/20 shadow-2xl shadow-primary/10 relative bg-background/95 backdrop-blur-sm overflow-hidden">
                  <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-primary/20 to-transparent rounded-bl-full"></div>
                  <CardContent className="p-10 relative">
                    <div className="space-y-8">
                      <div className="text-center space-y-6">
                        <div className="relative inline-block">
                          <div className="absolute inset-0 bg-gradient-to-br from-primary to-secondary rounded-3xl blur-xl opacity-50"></div>
                          <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-primary to-secondary mx-auto flex items-center justify-center shadow-2xl relative">
                            <GraduationCap className="w-12 h-12 text-white" />
                          </div>
                        </div>
                        <div className="space-y-3">
                          <h3 className="text-6xl font-bold bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">85%</h3>
                          <p className="text-lg font-semibold text-foreground">Job Placement Rate</p>
                          <p className="text-sm text-muted-foreground max-w-xs mx-auto leading-relaxed">
                            Students land jobs within 6 months of completing their roadmap
                          </p>
                        </div>
                      </div>
                      
                      <div className="pt-6 border-t space-y-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <CheckCircle2 className="w-5 h-5 text-primary" />
                          </div>
                          <p className="text-sm font-medium">Industry-ready skills</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <CheckCircle2 className="w-5 h-5 text-primary" />
                          </div>
                          <p className="text-sm font-medium">Verified project portfolio</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                            <CheckCircle2 className="w-5 h-5 text-primary" />
                          </div>
                          <p className="text-sm font-medium">Career support included</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            <div className="space-y-8">
              <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
                For University Students
              </Badge>
              <h2 className="text-4xl md:text-5xl font-bold">
                Bridge the Gap to Your Career
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Transform your degree into market-ready skills with our personalized upskilling roadmap.
              </p>
              
              <div className="grid sm:grid-cols-2 gap-4">
                {[
                  { icon: Code, title: 'Skill Gap Analysis', desc: 'Identify what you need' },
                  { icon: Award, title: 'Certifications', desc: 'Industry-recognized' },
                  { icon: Briefcase, title: 'Project Portfolio', desc: 'Real-world projects' },
                  { icon: TrendingUp, title: 'Career Growth', desc: 'Track your progress' }
                ].map((item, i) => (
                  <Card key={i} className="border hover:border-primary transition-all hover:shadow-lg">
                    <CardContent className="p-6 space-y-3">
                      <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                        <item.icon className="w-6 h-6 text-primary" />
                      </div>
                      <h4 className="font-semibold">{item.title}</h4>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <Button size="lg" className="shadow-lg shadow-primary/25 cursor-pointer" onClick={() => setIsModalOpen(true)}>
                Start Upskilling
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Professionals Section */}
      <section id="professionals" className="py-20 md:py-24 scroll-mt-16">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8 order-2 lg:order-1">
              <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
                For Professionals
              </Badge>
              <h2 className="text-4xl md:text-5xl font-bold">
                Make Your Career Switch Confidently
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Leverage your existing skills for a fulfilling career transition with AI-powered guidance.
              </p>
              
              <div className="space-y-4">
                {[
                  { icon: Target, title: 'Skills Assessment', desc: 'Analyze transferability to new roles' },
                  { icon: ArrowRight, title: 'Transition Planning', desc: 'Step-by-step roadmap without starting over' },
                  { icon: TrendingUp, title: 'Market Intelligence', desc: 'Real-time insights into job trends' }
                ].map((item, i) => (
                  <div key={i} className="flex gap-4 p-4 rounded-xl hover:bg-muted/50 transition-colors">
                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <item.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold mb-1">{item.title}</h4>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>

              <Button size="lg" className="shadow-lg shadow-primary/25 cursor-pointer" onClick={() => setIsModalOpen(true)}>
                Explore Transitions
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>

            <div className="order-1 lg:order-2">
              <Card className="border-2 border-primary/20 shadow-2xl shadow-primary/10 overflow-hidden">
                <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 border-b">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold">Transition Journey</h3>
                    <Badge variant="secondary" className="text-xs">4 Steps</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    A proven pathway to your next successful career move
                  </p>
                </div>
                <CardContent className="p-8 space-y-8">
                  {[
                    { step: 1, title: 'Skills Audit', desc: 'Assess your transferable skills', color: 'bg-[#146C94]', icon: Target },
                    { step: 2, title: 'Career Matching', desc: 'AI-powered role recommendations', color: 'bg-[#19A7CE]', icon: Brain },
                    { step: 3, title: 'Gap Analysis', desc: 'Identify learning opportunities', color: 'bg-[#AFD3E2]', icon: TrendingUp },
                    { step: 4, title: 'Execute Plan', desc: 'Follow your custom roadmap', color: 'bg-[#146C94]', icon: Map }
                  ].map((item) => (
                    <div key={item.step} className="flex gap-4 items-start group hover:translate-x-2 transition-transform">
                      <div className={`w-14 h-14 rounded-2xl ${item.color} text-white flex items-center justify-center font-bold text-xl flex-shrink-0 shadow-lg group-hover:shadow-xl transition-all`}>
                        <item.icon className="w-7 h-7" />
                      </div>
                      <div className="pt-1 space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-muted-foreground">STEP {item.step}</span>
                        </div>
                        <h4 className="font-bold text-lg">{item.title}</h4>
                        <p className="text-sm text-muted-foreground">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 md:py-24 bg-muted/30">
        <div className="container mx-auto px-4 max-w-7xl space-y-16">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
              <Zap className="w-3 h-3 mr-1" />
              Why Choose Us
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold">
              The New Standard in Career Guidance
            </h2>
            <p className="text-lg text-muted-foreground">
              Combining cutting-edge AI with proven psychological science
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: Brain, title: 'Psychometric Science + Agentic AI', desc: 'Validated assessments with specialized AI agents for deep career matching' },
              { icon: TrendingUp, title: 'Real-Time Market Intelligence', desc: 'Live job portal data ensures relevant, in-demand recommendations' },
              { icon: Shield, title: 'Grounded by RAG', desc: 'Retrieval-Augmented Generation ensures factual, up-to-date advice' },
              { icon: Map, title: 'Actionable Plans', desc: 'Detailed, milestone-based roadmaps from course selection to skills' }
            ].map((item, i) => (
              <Card key={i} className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
                <CardContent className="pt-8 pb-8 space-y-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <item.icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="text-lg font-semibold leading-tight">{item.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 md:py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary via-primary to-secondary"></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjEiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center space-y-8 max-w-3xl mx-auto text-white">
            <Badge className="text-xs px-3 py-1 bg-white/20 text-white border-white/30">
              <Sparkles className="w-3 h-3 mr-1" />
              Start Your Journey Today
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold">
              Ready to Unlock Your True Potential?
            </h2>
            <p className="text-lg md:text-xl opacity-90 leading-relaxed">
              Start with our scientifically-backed assessment and receive your initial AI-driven insights for free.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Button size="lg" variant="secondary" className="text-base h-14 px-8 shadow-2xl hover:scale-105 transition-transform cursor-pointer" onClick={() => setIsModalOpen(true)}>
                Start My Free Assessment
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </div>
            <div className="flex items-center justify-center gap-8 pt-6 text-sm">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                <span>No Credit Card Required</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                <span>100% Free Assessment</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-background py-12">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-16">
            <div className="col-span-2 md:col-span-1 space-y-4">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
                  <Compass className="h-5 w-5 text-white" />
                </div>
                <span className="text-base font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">Virtual Counsellor</span>
              </div>
              <p className="text-xs text-muted-foreground">
                © 2025 Virtual Counsellor. All rights reserved.
              </p>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-foreground text-sm mb-3">Product</h4>
              <ul className="space-y-2">
                <li>
                  <button 
                    onClick={() => scrollToSection('students')} 
                    className="text-sm text-muted-foreground hover:text-primary transition-colors cursor-pointer"
                  >
                    For Students
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => scrollToSection('college')} 
                    className="text-sm text-muted-foreground hover:text-primary transition-colors cursor-pointer"
                  >
                    For College
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => scrollToSection('professionals')} 
                    className="text-sm text-muted-foreground hover:text-primary transition-colors cursor-pointer"
                  >
                    For Professionals
                  </button>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-foreground text-sm mb-3">Company</h4>
              <ul className="space-y-2">
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">About Us</a></li>
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">Blog</a></li>
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">Careers</a></li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-foreground text-sm mb-3">Resources</h4>
              <ul className="space-y-2">
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">Help Center</a></li>
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">Terms of Service</a></li>
                <li><a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
        </div>
      </footer>

      <AssessmentModal 
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSelect={handleAssessmentSelect}
      />
    </div>
  );
};

export default LandingPage;