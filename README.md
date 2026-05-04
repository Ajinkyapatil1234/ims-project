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
PostgreSQL (DB)
      ↓
Redis Queue → Worker → Incident Processing

---

##  Setup Instructions

### 1. Clone repo

```bash
git clone 
cd ims-project
