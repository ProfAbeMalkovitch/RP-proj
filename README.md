# RP-proj
https://github.com/ProfAbeMalkovitch/RP-proj

# 📘 E-Learning Platform – Personalized Micro-Learning with Adaptive Content Structuring and Progress Analytics  
**Project ID:** 25-26J-233  

## 👥 Team Members  
| Name | Student ID | Role |
|------|-------------|------|
| **B. Iroshan** | IT22901262 | Education Content Extraction & Structuring Engine (ECESE) |
| **Ahamed M.N.A** | IT22243508 | Intelligent Learning Pathway Generator (ILPG) |
| **Weerasekara W.M.P.S** | IT22215406 | Progress Monitoring & Streak Analytics System (PMSAS) |
| **Ahmed M.N.A** | IT22920386 | Micro-Learning via Daily Challenges |

**Supervisor:** Mrs. Geethanjali Wimalaratne  
**Co-Supervisor:** Dr. Kapila Dissanayake  

---

## 🧩 Overview
This platform proposes a **teacher-supervised, AI-assisted e-learning ecosystem** that solves common issues in digital learning such as:  
- Generic content  
- Lack of personalization  
- No real-time motivation or analytics  
- No curriculum alignment  
- Limited teacher control  

The platform integrates four components:
1. **Education Content Extraction & Structuring Engine (ECESE)**
2. **Intelligent Learning Pathway Generator (ILPG)**
3. **Micro-Learning via Daily Challenges**
4. **Progress Monitoring & Streak Analytics System (PMSAS)**

---

## 🧠 1. Education Content Extraction & Structuring Engine (ECESE)

### Purpose  
Extracts, parses, and structures educational content from textbooks, teacher guides, and PDFs—fully aligned with curriculum requirements.

### Features  
- NLP-driven content extraction  
- Taxonomy & ontology-based curriculum mapping  
- Teacher validation dashboards  
- Structured output for downstream modules  

### Technologies  
- **NLP:** spaCy, NLTK, Hugging Face  
- **Parsing:** PDFBox, PyPDF2  
- **Backend:** Spring Boot / Node.js  
- **Frontend:** React.js / React Native  
- **Database:** MongoDB / Firebase / AWS S3  

### Evaluation  
- ≥ 90% curriculum alignment  
- Validation by teachers using official textbooks and guides  

---

## 🧭 2. Intelligent Learning Pathway Generator (ILPG)

### Purpose  
Creates personalized learning paths for students based on performance and engagement.

### Features  
- Learner categorization: **Basic**, **Balanced**, **Accelerated**  
- Rule-based and transparent (no black-box AI)  
- Teacher-driven content and control  
- Dynamic adaptation based on quiz history, behavior, and streaks  

### Technologies  
- **Frontend:** React.js, Bootstrap  
- **Backend:** Node.js, Express  
- **Analytics:** D3.js, Matomo, Google Analytics  
- **Database:** Firebase / MongoDB / AWS S3  

### Evaluation  
- ≥ 90% pathway alignment  
- Reduced drop-offs, improved engagement  
- AES-256 encryption & access control for all data  

---

## 📚 3. Micro-Learning via Daily Challenges

### Purpose  
Delivers daily, syllabus-aligned micro-learning tasks to improve engagement, retention, and habit formation.

### Features  
- Adaptive task scheduling  
- Teacher-approved micro-lessons  
- Motivation-aware reminders  
- Comparative analytics (micro vs clustered learning)  

### Technologies  
- **Frontend:** React.js / React Native  
- **Backend:** Spring Boot / Node.js  
- **Analytics:** D3.js, Matomo  
- **Database:** MongoDB / Firebase / AWS S3  

### Evaluation Metrics  
- Retention improvement  
- Streak continuation rate  
- Dropout reduction  

---

## 📈 4. Progress Monitoring & Streak Analytics System (PMSAS)

### Purpose  
Tracks student engagement and progress using streaks, badges, awards, and predictive analytics.

### Features  
- Curriculum-linked streak engine  
- Predictive disengagement alerts  
- Teacher dashboard for interventions  
- Real-time analytics & visualizations  

### Technologies  
- **Frontend:** React.js / React Native  
- **Backend:** Node.js / Spring Boot  
- **Analytics:** Python (scikit-learn, pandas), D3.js  
- **Database:** MongoDB / Firebase / AWS S3  

### Evaluation  
- 20%+ improvement in engagement consistency  
- Metrics: **Avg streak length**, **drop-off reduction**, **intervention success rate**  

---

## 🏗️ System Architecture
- Microservice-based design  
- REST API integration between components  
- Secure cloud deployment (AWS / Firebase)  
- AES-256 encrypted data handling  
- Role-based user authentication  

---

## ⚙️ Non-Functional Requirements  
| Category | Requirement |
|-----------|--------------|
| *Performance* | < 2 sec response time |
| *Availability* | 99.9% uptime |
| *Security* | AES-256, HTTPS, RBAC |
| *Usability* | Mobile + Desktop compatibility |
| *Scalability* | Cloud-native microservices |

---

## 💡 Commercialization  
- SaaS platform for *schools, **tutoring centers, and **universities*  
- Subscription/licensing model  
- Unique selling point: *Curriculum-specific personalization + teacher oversight*  

---

## ▶️ How to run the application
## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and npm (for frontend)
- **MongoDB** (local or cloud instance)
- **Groq API Key** (for AI features)

## Setup

### Backend Setup

1. Navigate to the backend directory:
   
   cd backend
   2. Create a virtual environment (recommended):
 
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install Python dependencies:
   pip install -r requirements.txt
   4. Create a `.env` file in the backend directory:v
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET_KEY=your_jwt_secret_key
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama-3.1-8b-instant
   ### Frontend Setup

1. Navigate to the frontend directory:
   cd frontend
   2. Install dependencies:
   npm install
   ## Running the Application

### Backend Services

The application requires two backend services:

1. **Main Flask API** (port 5000):
   
   cd backend
   python app.py
   2. **ECESE FastAPI Service** (port 5001):
   cd backend
   uvicorn ecese_app:app --port 5001 --reload
   ### Frontend

1. Start the development server:
   
   cd frontend
   npm run dev
      The frontend will typically run on `http://localhost:5173`

## Access Points

- **Frontend**: http://localhost:5173
- **Main API**: http://localhost:5000
- **ECESE API**: http://localhost:5001
- **ECESE API Docs**: http://localhost:5001/docs

## Notes

- Make sure MongoDB is running and accessible
- Both backend services must be running for full functionality
- The ECESE service handles PDF content extraction and AI-powered structuring
- The main Flask API handles authentication, learning pathways, and progress tracking
