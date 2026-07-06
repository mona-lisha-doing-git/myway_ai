# MyWay AI – An AI-Powered College Decision Intelligence Platform

MyWay AI is an AI-powered decision intelligence platform designed to help students make smarter and faster college admission decisions. Instead of manually comparing colleges across multiple websites, MyWay AI analyzes structured educational data using GPU-accelerated analytics and intelligent ranking algorithms to recommend the most suitable colleges based on a student's preferences.

The platform leverages **Google Gemini**, **Google Agent Development Kit (ADK)**, **FastAPI**, and **Google BigQuery** to provide personalized recommendations along with natural language explanations that help students understand why a particular college is recommended.

---

## Problem Statement

Every year, millions of students face the difficult task of selecting the right college. Important information such as tuition fees, placement statistics, admission cutoffs, rankings, courses offered, and scholarship opportunities is scattered across multiple websites and official portals. Students often spend days comparing this information manually, making the decision-making process time-consuming, confusing, and prone to errors.

MyWay AI addresses this challenge by providing an AI-powered Decision Intelligence Platform that transforms structured educational data into actionable recommendations. Instead of simply searching for colleges, the platform analyzes multiple decision factors simultaneously—including budget, preferred course, state, admission rank, placement performance, and institutional rankings—to recommend the most suitable colleges for each student.

The platform combines GPU-accelerated data analytics, intelligent ranking algorithms, and Gemini-powered natural language explanations to help students make faster and more informed educational decisions.

---

# Features

- AI-powered college recommendation system
- Intelligent filtering based on student preferences
- Weighted ranking algorithm for better decision making
- BigQuery-backed data access for scalable cloud analytics
- Natural language explanations powered by Google Gemini
- FastAPI backend APIs
- React-based responsive user interface
- Modular agent architecture using Google Agent Development Kit (ADK)

---

# Technology Stack

## Frontend

- React.js
- Responsive dashboard for entering student preferences and displaying recommendations

---

## Backend

- Python
- Google Agent Development Kit (ADK) for agent orchestration
- FastAPI for backend APIs
- Google Gemini for generating personalized explanations of recommendations

---

## Data Processing & Analytics

- Google BigQuery
- Official `google-cloud-bigquery` Python client
- Environment-variable-based authentication using Application Default Credentials or a service account key

Structured BigQuery tables containing:

- College information
- Courses
- Admission cutoffs
- Placement statistics

---

# Recommendation Pipeline

```
Prepared Dataset
        ↓
Google BigQuery
        ↓
Data Cleaning & Merging
        ↓
Filtering
        ↓
Weighted Ranking Algorithm
        ↓
Top College Recommendations
        ↓
Gemini AI Explanation
        ↓
Student Decision Support
```

---

# System Architecture

```
Student
      ↓
React Frontend
      ↓
FastAPI Backend
      ↓
Recommendation Agent (Google ADK)
      ↓
Recommendation Engine
      ↓
Google BigQuery
      ↓
Merged Educational Dataset
      ↓
Filtering & Ranking
      ↓
Top College Recommendations
      ↓
Gemini
      ↓
AI-powered Explanation
```

---

# Project Structure

```
myway_ai/
│
├── agents/
│   ├── recommendation_agent.py
│   ├── career_agent.py
│   └── study_planner_agent.py
│
├── utils/
│   ├── bigquery_client.py
│   ├── bigquery_config.py
│   ├── bigquery_queries.py
│   ├── recommendation_engine.py
│   ├── data_loader.py
│   └── ranking.py
│
├── frontend/
│
├── agent.py
├── app.py
├── requirements.txt
└── README.md
```

---

# Agent Architecture

### Recommendation Agent

The Recommendation Agent is responsible for understanding student preferences, filtering the educational dataset, applying ranking logic, and generating personalized college recommendations.

---

### Future Scope

The project already contains additional agents inside the `agents` folder:

- Career Agent
- Study Planner Agent

These agents are intentionally kept as placeholders for future enhancements and are **not modified** in the current implementation.

Future versions of MyWay AI will integrate these agents to provide:

- Personalized career guidance
- Semester-wise study planning
- Skill roadmap generation
- Learning resource recommendations
- Career path prediction

---

# Recommendation Criteria

The recommendation engine evaluates colleges using multiple factors, including:

- Student's preferred course
- Budget
- State preference
- Government/Private institution preference
- Admission cutoff
- Placement package
- Institutional ranking

Each factor contributes to a weighted score that determines the final recommendation ranking.

---

# Dataset

The recommendation engine reads structured BigQuery tables:

- Colleges
- Courses
- Admission Cutoffs
- Placement Statistics

These tables are fetched through reusable BigQuery access modules, normalized into dataframes, merged, filtered, and ranked using the existing recommendation logic.

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/mona-lisha-doing-git/myway_ai.git
```

```bash
cd myway_ai
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_CLOUD_PROJECT=myway-ai-501316
BIGQUERY_DATASET=myway_ai
BIGQUERY_LOCATION=asia-south1

# Optional local service-account key. Prefer Cloud Run service identity in production.
# GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json

# Optional table overrides. Defaults are colleges, courses, placements, cutoffs.
BIGQUERY_COLLEGES_TABLE=colleges
BIGQUERY_COURSES_TABLE=courses
BIGQUERY_PLACEMENTS_TABLE=placements
BIGQUERY_CUTOFFS_TABLE=cutoffs

# Optional Gemini configuration.
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_LOCATION=global
GEMINI_MODEL=gemini-2.5-flash
```

---

## Run the Backend

```bash
adk web
```

or

```bash
uvicorn app:app --reload
```

(depending on your project configuration)

---

## Run the Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Future Improvements

- Real-time admission cutoffs
- Live placement statistics
- Scholarship recommendation system
- Career Recommendation Agent integration
- Study Planner Agent integration
- Personalized educational roadmap
- Cloud deployment on Google Cloud Run
- Authentication and user profiles

---

# Deployment

The application is designed to be deployed using:

- Google Cloud Run
- Docker
- FastAPI
- Google ADK
- React Frontend

The backend uses BigQuery for scalable cloud-based data management.

---

# Author

**Monalisha Kalita**

B.Tech Computer Science Engineering

AI | Machine Learning | Generative AI | Full Stack Development

---

# License

This project is developed for educational and research purposes.
