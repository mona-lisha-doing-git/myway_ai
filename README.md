# MyWay AI – An AI-Powered College Decision Intelligence Platform

MyWay AI is an AI-powered decision intelligence platform designed to help students make smarter and faster college admission decisions. Instead of manually comparing colleges across multiple websites, MyWay AI analyzes structured educational data using GPU-accelerated analytics and intelligent ranking algorithms to recommend the most suitable colleges based on a student's preferences.

The platform leverages **Google Gemini**, **Google Agent Development Kit (ADK)**, **FastAPI**, and **NVIDIA RAPIDS cuDF** to provide personalized recommendations along with natural language explanations that help students understand why a particular college is recommended.

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
- GPU-accelerated data processing using NVIDIA RAPIDS cuDF
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

- NVIDIA RAPIDS
- cuDF for GPU-accelerated data loading, cleaning, merging, and filtering

Structured CSV datasets containing:

- College information
- Courses
- Admission cutoffs
- Placement statistics

---

# Recommendation Pipeline

```
Prepared Dataset
        ↓
NVIDIA cuDF
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
NVIDIA cuDF
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
│   ├── recommendation_engine.py
│   ├── data_loader.py
│   └── ranking.py
│
├── data/
│   ├── colleges.csv
│   ├── courses.csv
│   ├── cutoffs.csv
│   └── placements.csv
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

The recommendation engine currently uses structured CSV datasets:

- Colleges
- Courses
- Admission Cutoffs
- Placement Statistics

These datasets are cleaned, merged, and processed using NVIDIA RAPIDS cuDF before applying filtering and ranking algorithms.

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
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
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

- BigQuery integration
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

Future deployments can replace CSV datasets with BigQuery for scalable cloud-based data management.

---

# Author

**Monalisha Kalita**

B.Tech Computer Science Engineering

AI | Machine Learning | Generative AI | Full Stack Development

---

# License

This project is developed for educational and research purposes.