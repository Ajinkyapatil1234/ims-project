#  Incident Management System (IMS)

A simple Incident Management System built using FastAPI, PostgreSQL, Redis, and Docker to simulate real-world SRE/DevOps incident workflows.

---

##  Tech Stack

- Backend: FastAPI (Python)
- Database: PostgreSQL
- Queue: Redis
- Worker: Background worker (queue consumer)
- Frontend: HTML + JavaScript
- Containerization: Docker & Docker Compose

---

##  Features

- Create incidents manually (UI)
- Create incidents via API signals
- Background worker processes signals
- Incident lifecycle:
  - OPEN → RESOLVED
- Tracks:
  - Component
  - Severity (P0 / P1 / P2)
  - Description
  - Created Time
  - Resolved Time
  - MTTR (Mean Time To Resolve)

---

##  Architecture

Frontend (HTML)  
↓  
FastAPI Backend  
↓  
PostgreSQL (Database)  
↓  
Redis Queue → Worker → Incident Processing  

---

## ⚙️ Setup Instructions

### 1. Clone repository

git clone 
cd ims-project  

---

### 2. Run using Docker

docker-compose up --build  

---

### 3. Access the application

- Frontend UI: http://localhost:5500  
- Backend API (Swagger): http://localhost:8000/docs  

---

## 📡 API Endpoints

### Create Incident  
POST /incidents  

### Get Incidents  
GET /incidents  

### Resolve Incident  
POST /incidents/{id}/resolve  

### Send Signal (Queue-based)

curl -X POST http://localhost:8000/signal 
-H "Content-Type: application/json" 
-d '{"component":"API_SERVER","severity":"P1","description":"CPU High"}'

---

##  Incident Flow

1. Signal sent → Redis queue  
2. Worker consumes signal  
3. Incident created in database  
4. Incident resolved via UI/API  
5. MTTR calculated automatically  

---

##  Example Output

| ID | Component   | Status   | Severity | MTTR |
|----|------------|----------|----------|------|
| 1  | API_SERVER | RESOLVED | P1       | 539s |

---

##  Non-functional Improvements (Bonus)

- Authentication (JWT / RBAC)
- Rate limiting for APIs
- Retry mechanism for failed jobs
- Dead-letter queue for failures
- Monitoring with Prometheus & Grafana

---

##  Author

Ajinkya Patil  
DevOps / Cloud Enthusia

