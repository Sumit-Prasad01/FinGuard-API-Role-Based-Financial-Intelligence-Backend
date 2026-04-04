# 🏆 FinGuard API

A production-ready financial management backend system built with FastAPI.

---

## 🚀 Core Features

- User Authentication (JWT based)
- Role-Based Access Control (RBAC)
- Financial Records Management (CRUD)
- Dashboard Analytics
- Redis Caching
- Rate Limiting (slowapi)
- Logging Middleware
- Dockerized Deployment

---

## 🧱 System Architecture (High-Level Design)

```
          ┌───────────────┐
          │    Client     │
          │ (Frontend/UI) │
          └──────┬────────┘
                 │ HTTP Requests
                 ▼
          ┌───────────────┐
          │   FastAPI     │
          │  (API Layer)  │
          └──────┬────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
 ┌──────────────┐   ┌──────────────┐
 │   Services   │   │ Dependencies │
 │ (Business    │   │ Auth / RBAC  │
 │   Logic)     │   └──────────────┘
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │     DB       │
 │  (SQLite)    │
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │   Redis      │
 │   (Cache)    │
 └──────────────┘
```

---

## 🔐 Authentication System

- Access Token (short-lived)
- Refresh Token (long-lived)

### Endpoints:
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

---

## 🛡️ Role-Based Access Control

Roles:
- Admin
- Analyst
- Viewer

Example:
```python
Depends(require_roles(["admin"]))
```

---

## 💰 Financial Records APIs

- POST   /records/
- GET    /records/
- PUT    /records/{id}
- DELETE /records/{id}

### Features:
- Search (notes/category)
- Filters (date, type, category)
- Pagination (limit, offset)

---

## 📊 Dashboard API

GET /dashboard/

### Provides:
- Total Income
- Total Expense
- Net Balance
- Category Breakdown
- Monthly Trends

---

## ⚡ Performance Enhancements

- Async FastAPI + Async SQLAlchemy
- Redis caching (Dashboard)
- Rate limiting (slowapi)

---

## 🧠 Project Structure

```
FinGuard/
│
├── app/
│   ├── api/            # API route definitions
│   ├── cache/          # Redis caching logic
│   ├── core/           # Config & settings
│   ├── db/             # Database models & session
│   ├── dependencies/   # Auth & RBAC dependencies
│   ├── middlewares/    # Logging & request handling
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic layer
│   ├── utils/          # Utility functions
│   ├── __init__.py
│   └── main.py         # Entry point
│
├── logs/               # Application logs
├── tests/              # Test cases
├── .env                # Environment variables
├── .gitignore
├── API_DOCS.md         # API documentation
├── docker-compose.yml
├── dockerfile
├── fin_guard.db        # SQLite database
├── prometheus.yml      # Monitoring config
├── README.md
├── requirements.txt
├── setup.py
└── templates.py
```

---

## 🐳 Docker Setup

### Run:
```bash
docker-compose up --build
```

### Services:
- FastAPI → http://localhost:8000
- Redis → localhost:6379
- Prometheus → http://localhost:9090
- Grafana → http://localhost:3000

---

## 🌱 Environment Variables (.env)

```
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REDIS_URL=
```

---

## 🔁 Auto Role Seeding

Roles created on startup:
- admin
- analyst
- viewer

---

## 🧪 API Coverage

✔ Register  
✔ Login  
✔ Refresh Token  
✔ Create Records  
✔ Filter/Search  
✔ Update/Delete  
✔ Dashboard  

---

## 📌 Future Improvements

- AI-based financial insights
- Budget planning module
- Notification system
- Graph analytics

---

