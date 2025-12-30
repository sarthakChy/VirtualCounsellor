# VirtualCounsellor

VirtualCounsellor is an advanced AI-powered career counseling platform designed to guide students and professionals through their career journeys. It leverages a sophisticated agentic architecture to provide personalized advice, roadmap planning, and market intelligence.

## 🚀 Features

The platform caters to three main verticals:

### 1. School Students (Grades 9-12)
*   **Test Score Interpretation**: Analyzes DBDA (David's Battery of Differential Abilities) scores and CII (Career Interest Inventory) results.
*   **Academic Stream Advisor**: Recommends suitable academic streams based on aptitude and interests.
*   **Career Pathway Explorer**: Explores potential career paths aligned with the student's profile.
*   **Educational Roadmap Planner**: Creates a step-by-step roadmap for academic and career goals.
*   **College & Scholarship Navigator**: Suggests colleges and scholarship opportunities.

### 2. College Students (Upskilling & Career Optimization)
*   **Profile Analysis**: Evaluates resumes, GitHub, and LinkedIn profiles to identify strengths and gaps.
*   **Market Intelligence**: Provides real-time insights into job market trends and demand.
*   **Skill Development Strategist**: Recommends skills to acquire for target roles.
*   **Opportunity Matcher**: Matches students with relevant internships and job openings.
*   **Career Optimization**: Optimizes career paths for maximum growth and satisfaction.

### 3. Career Transition (Planned/In-Progress)
*   **Transition Planning**: Helps professionals switch careers by leveraging transferable skills.
*   **Gap Analysis**: Identifies skill gaps required for the new role.

## 🏗 Architecture

The system is built on a robust **Agentic Layer** using **LangGraph** and **LangChain**.

*   **Agent Orchestrator**: Manages the workflow and routes user requests to the appropriate specialized agents.
*   **Specialized Agents**: Each vertical has a fleet of agents (e.g., `MarketIntelligenceAgent`, `AcademicStreamAdvisorAgent`) that perform specific tasks.
*   **Sub-Agents**: Granular tasks are handled by sub-agents like `SalaryBenchmarkingSubAgent` or `DomainExtractionSubAgent`.
*   **Fleet Managers**: Coordinate the activities of agents within a specific vertical.

## 🛠 Tech Stack

### Backend
*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **AI/LLM**: LangChain, LangGraph, Google Gemini, OpenAI GPT
*   **Observability**: LangSmith
*   **Scraping**: JobSpy, Playwright, BeautifulSoup4
*   **Data Processing**: Pandas, NumPy

### Frontend
*   **Framework**: React 19
*   **Build Tool**: Vite
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS
*   **UI Components**: Radix UI, Lucide React

### DevOps
*   **Containerization**: Docker

## 📋 Prerequisites

*   Python 3.10 or higher
*   Node.js 18 or higher
*   API Keys for:
    *   OpenAI
    *   Google Gemini
    *   LangSmith (Optional, for tracing)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/coounsellor.git
cd coounsellor
```

### 2. Backend Setup

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install
```

Create a `.env` file in the root directory and add your API keys:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=coounsellor
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

## 🏃‍♂️ Running the Application

### Start the Backend Server

From the root directory:

```bash
uvicorn server.run:app --reload
```
The API will be available at `http://localhost:8000`.
API Documentation is available at `http://localhost:8000/docs`.

### Start the Frontend Development Server

From the `frontend` directory:

```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

