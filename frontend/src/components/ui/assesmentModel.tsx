// import React from 'react';
// import { Dialog, DialogContent } from '@/components/ui/dialog';
// import { Card, CardContent } from '@/components/ui/card';
// import { Button } from '@/components/ui/button';
// import { Badge } from '@/components/ui/badge';
// import { Compass, GraduationCap, Briefcase, ArrowRight, X } from 'lucide-react';

// interface AssessmentModalProps {
//   open: boolean;
//   onClose: () => void;
//   onSelect: (type: 'school' | 'college' | 'professional') => void;
// }

// const AssessmentModal: React.FC<AssessmentModalProps> = ({ open, onClose, onSelect }) => {
//   return (
//     <Dialog open={open} onOpenChange={onClose}>
//       <DialogContent className="max-w-5xl p-0 gap-0 bg-background overflow-hidden">
//         <div className="relative">
//           {/* Close Button */}
//           <button
//             onClick={onClose}
//             className="absolute top-6 right-6 z-10 rounded-full p-2 hover:bg-muted transition-colors"
//           >
//             <X className="w-5 h-5" />
//           </button>

//           {/* Header */}
//           <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-10 border-b">
//             <div className="text-center space-y-4">
//               <Badge className="text-xs px-3 py-1 bg-primary/10 text-primary border-primary/20">
//                 <Sparkles className="w-3 h-3 mr-1 inline" />
//                 Choose Your Path
//               </Badge>
//               <h2 className="text-3xl md:text-4xl font-bold">
//                 Select Your Assessment
//               </h2>
//               <p className="text-muted-foreground max-w-2xl mx-auto text-base">
//                 Choose the assessment that best matches your current stage to receive personalized guidance
//               </p>
//             </div>
//           </div>

//           {/* Options Grid */}
//           <div className="p-10">
//             <div className="grid md:grid-cols-3 gap-6">
//               {/* School Students */}
//               <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
//                 <CardContent className="pt-8 pb-8 space-y-6">
//                   <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform mx-auto">
//                     <Compass className="w-10 h-10 text-primary" />
//                   </div>
//                   <div className="text-center space-y-3">
//                     <h3 className="text-xl font-bold">School Students</h3>
//                     <p className="text-sm font-semibold text-primary">Choosing Your Stream?</p>
//                     <p className="text-sm text-muted-foreground leading-relaxed min-h-[60px]">
//                       Get guidance on selecting the right academic stream based on your interests
//                     </p>
//                   </div>
//                   <Button 
//                     onClick={() => onSelect('school')}
//                     className="w-full group-hover:shadow-lg transition-all cursor-pointer"
//                   >
//                     Start Assessment
//                     <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
//                   </Button>
//                 </CardContent>
//               </Card>

//               {/* College Students */}
//               <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
//                 <CardContent className="pt-8 pb-8 space-y-6">
//                   <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-secondary/20 to-secondary/10 flex items-center justify-center group-hover:scale-110 transition-transform mx-auto">
//                     <GraduationCap className="w-10 h-10 text-primary" />
//                   </div>
//                   <div className="text-center space-y-3">
//                     <h3 className="text-xl font-bold">College Students</h3>
//                     <p className="text-sm font-semibold text-primary">Ready to Upskill?</p>
//                     <p className="text-sm text-muted-foreground leading-relaxed min-h-[60px]">
//                       Bridge the gap between college and career with personalized roadmaps
//                     </p>
//                   </div>
//                   <Button 
//                     onClick={() => onSelect('college')}
//                     className="w-full group-hover:shadow-lg transition-all cursor-pointer"
//                   >
//                     Start Assessment
//                     <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
//                   </Button>
//                 </CardContent>
//               </Card>

//               {/* Professionals */}
//               <Card className="border-2 hover:border-primary transition-all hover:shadow-xl hover:shadow-primary/10 group">
//                 <CardContent className="pt-8 pb-8 space-y-6">
//                   <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform mx-auto">
//                     <Briefcase className="w-10 h-10 text-primary" />
//                   </div>
//                   <div className="text-center space-y-3">
//                     <h3 className="text-xl font-bold">Professionals</h3>
//                     <p className="text-sm font-semibold text-primary">Career Switch?</p>
//                     <p className="text-sm text-muted-foreground leading-relaxed min-h-[60px]">
//                       Transition confidently with AI-powered career matching and planning
//                     </p>
//                   </div>
//                   <Button 
//                     onClick={() => onSelect('professional')}
//                     className="w-full group-hover:shadow-lg transition-all cursor-pointer"
//                   >
//                     Start Assessment
//                     <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
//                   </Button>
//                 </CardContent>
//               </Card>
//             </div>
//           </div>

//           {/* Footer Note */}
//           <div className="border-t px-10 py-6 bg-muted/30">
//             <p className="text-center text-sm text-muted-foreground">
//               All assessments are <span className="font-semibold text-foreground">100% free</span> and take approximately <span className="font-semibold text-foreground">10-15 minutes</span> to complete
//             </p>
//           </div>
//         </div>
//       </DialogContent>
//     </Dialog>
//   );
// };

// const Sparkles = ({ className }: { className?: string }) => (
//   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
//     <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
//     <path d="M5 3v4"/>
//     <path d="M19 17v4"/>
//     <path d="M3 5h4"/>
//     <path d="M17 19h4"/>
//   </svg>
// );

// export default AssessmentModal;


import React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Compass, GraduationCap, Briefcase, ArrowRight, X, Sparkles } from 'lucide-react';

interface AssessmentModalProps {
  open: boolean;
  onClose: () => void;
  onSelect: (type: 'school' | 'college' | 'professional') => void;
}

const AssessmentModal: React.FC<AssessmentModalProps> = ({ open, onClose, onSelect }) => {
  return (
    <DialogPrimitive.Root open={open} onOpenChange={onClose}>
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm" />

        <DialogPrimitive.Content className="
          fixed left-1/2 top-1/2 z-50 
          w-full max-w-4xl 
          -translate-x-1/2 -translate-y-1/2 
          rounded-2xl border bg-background shadow-lg
          max-h-[80vh] overflow-hidden
        ">
          <div className="relative">

            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 z-10 rounded-full p-2 hover:bg-muted transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Header */}
            <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-6 md:p-7 border-b">
              <div className="text-center space-y-2">
                <Badge className="text-xs px-2 py-0.5 bg-primary/10 text-primary border-primary/20">
                  <Sparkles className="w-3 h-3 mr-1 inline" /> Choose Your Path
                </Badge>

                <h2 className="text-2xl md:text-3xl font-bold">
                  Select Your Assessment
                </h2>

                <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
                  Choose the assessment that matches your stage to get personalized guidance
                </p>
              </div>
            </div>

            {/* Options Grid */}
            <div className="p-6 md:p-7">
              <div className="grid md:grid-cols-3 gap-4">

                {/* School Students */}
                <Card className="border-2 hover:border-primary transition-all hover:shadow-lg group">
                  <CardContent className="pt-6 pb-6 space-y-4">
                    <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mx-auto group-hover:scale-105 transition-transform">
                      <Compass className="w-8 h-8 text-primary" />
                    </div>

                    <div className="text-center space-y-1">
                      <h3 className="text-lg font-bold">School Students</h3>
                      <p className="text-sm font-semibold text-primary">Choosing Your Stream?</p>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Get guidance on selecting the right academic stream.
                      </p>
                    </div>

                    <Button 
                      onClick={() => onSelect('school')}
                      className="w-full group-hover:shadow-md cursor-pointer"
                    >
                      Start
                      <ArrowRight className="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </CardContent>
                </Card>

                {/* College Students */}
                <Card className="border-2 hover:border-primary transition-all hover:shadow-lg group">
                  <CardContent className="pt-6 pb-6 space-y-4">
                    <div className="w-14 h-14 rounded-xl bg-secondary/10 flex items-center justify-center mx-auto group-hover:scale-105 transition-transform">
                      <GraduationCap className="w-8 h-8 text-primary" />
                    </div>

                    <div className="text-center space-y-1">
                      <h3 className="text-lg font-bold">College Students</h3>
                      <p className="text-sm font-semibold text-primary">Ready to Upskill?</p>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Bridge the gap between college and career.
                      </p>
                    </div>

                    <Button 
                      onClick={() => onSelect('college')}
                      className="w-full group-hover:shadow-md cursor-pointer"
                    >
                      Start
                      <ArrowRight className="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </CardContent>
                </Card>

                {/* Professionals */}
                <Card className="border-2 hover:border-primary transition-all hover:shadow-lg group">
                  <CardContent className="pt-6 pb-6 space-y-4">
                    <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mx-auto group-hover:scale-105 transition-transform">
                      <Briefcase className="w-8 h-8 text-primary" />
                    </div>

                    <div className="text-center space-y-1">
                      <h3 className="text-lg font-bold">Professionals</h3>
                      <p className="text-sm font-semibold text-primary">Career Switch?</p>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Transition confidently with career matching and planning.
                      </p>
                    </div>

                    <Button 
                      onClick={() => onSelect('professional')}
                      className="w-full group-hover:shadow-md cursor-pointer"
                    >
                      Start
                      <ArrowRight className="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </CardContent>
                </Card>

              </div>
            </div>

            {/* Footer */}
            <div className="border-t px-6 py-4 bg-muted/30">
              <p className="text-center text-xs md:text-sm text-muted-foreground">
                All assessments are <span className="font-semibold">free</span> and take around <span className="font-semibold">10–15 minutes</span>.
              </p>
            </div>

          </div>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
};

export default AssessmentModal;
