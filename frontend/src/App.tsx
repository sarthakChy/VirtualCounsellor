import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import CollegeAssessmentForm from "./pages/CollegeAssesmentForm";
import CollegeAnalysisResult from "./pages/CollegeAnalysisResult";
import SchoolAssessment from "./pages/SchoolAssessment";
import SchoolAssessmentResults from "./pages/SchoolAssessmentResults";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/college-assessment" element={<CollegeAssessmentForm />} />
      <Route path="/college-assessment-results" element={<CollegeAnalysisResult />} />
      <Route path="/school-assessment" element={<SchoolAssessment />} />
      <Route path="/school-assessment-results" element={<SchoolAssessmentResults />} />
    </Routes>
  );
}

export default App;