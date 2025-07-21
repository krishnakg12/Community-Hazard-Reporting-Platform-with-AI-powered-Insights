# 🛑 Community Hazard Reporting Platform  
> Submitted to the **Google Developers Group Solution Challenge 2025**

An end-to-end AI-powered platform that enables citizens to report local hazards in real-time and assists authorities in prioritizing critical issues using ML-powered classification. Built using a full-stack architecture with real-time features, AI integration, and a responsive UI.



  Overview

The platform allows users to:
- Report environmental, infrastructural, or public safety hazards.
- Attach descriptions and images of the hazard.
- Automatically classify the type of hazard (e.g., Fire, Garbage, Pothole) using ML.
- Predict and display hazard **priority** (High/Medium/Low) based on risk factors like location, time, traffic, and weather.
- Notify local authorities via real-time alerts.



 Tech Stack

###  Frontend:
- React.js + Tailwind CSS  
- Mapbox API for location pinning  
- Axios for API integration

###  Backend:
- Django (WebSocket + REST APIs)  
- Node.js + Express (used in alternate version)  
- MongoDB (Cloud Atlas) for data storage  
- JWT for secure user authentication

 Machine Learning:
- FastAPI serving ML models:
  - Text & Image Classification (scikit-learn, PyTorch)
  - Hazard Priority Scoring (Random Forest, XGBoost)
- Deployed models as REST endpoints
- LangChain used for chatbot integration
- Pinecone for vector search (planned extension)


 Features

- 🧠 AI-based Hazard Type & Priority Classification
- 📍 Location tagging with latitude/longitude
- 📷 Image upload & classification
- 🔴 Real-time dashboard for authorities with live updates
- 🧾 Chatbot for citizen query support (via Gemini API)
- ✅ Separate dashboards for citizens and administrators




  How to Run Locally

1. Clone the repo  

Set up Backend

cd server
npm install
npm run dev

Set up Frontend

cd client
npm install
npm start

Run ML API (FastAPI)

cd ml-api
uvicorn main:app --reload
