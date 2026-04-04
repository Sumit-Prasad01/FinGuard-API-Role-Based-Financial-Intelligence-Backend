# FinGuard API Documentation (Enhanced)

## Base URL
http://localhost:8000

---

## 📌 Overview
FinGuard is a financial tracking and analytics API that allows users to manage income, expenses, and gain insights through dashboards.

---

## 🔐 Auth APIs

### 1. Register
**POST /auth/register**

**Description:** Create a new user account.

**Request:**
```json
{
  "name": "user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "user",
  "email": "user@example.com",
  "role_id": 3
}
```

---

### 2. Login
**POST /auth/login**

**Description:** Authenticate user and return JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

### 3. Refresh Token
**POST /auth/refresh**

**Description:** Generate new tokens using refresh token.

**Request:**
```json
{
  "refresh_token": "..."
}
```

**Response:**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

## 👤 User APIs

### Get All Users
**GET /users/**

**Headers:** Authorization: Bearer <token>

**Response:**
```json
[
  {
    "id": 1,
    "name": "user",
    "email": "user@example.com"
  }
]
```

---

### Get User by ID
**GET /users/{id}**

**Description:** Retrieve a specific user.

---

## 💰 Records APIs

### Create Record
**POST /records/**

**Description:** Add income or expense record.

```json
{
  "amount": 5000,
  "type": "expense",
  "category": "food",
  "date": "2026-04-03T10:00:00",
  "notes": "Lunch"
}
```

---

### Get Records
**GET /records/**

**Query Params:**
- category
- type
- search
- limit
- offset

---

### Update Record
**PUT /records/{id}**

**Description:** Update an existing record.

---

### Delete Record
**DELETE /records/{id}**

**Description:** Remove a record.

---

## 📊 Dashboard API

### Get Dashboard
**GET /dashboard/**

**Description:** Returns financial summary and trends.

**Response:**
```json
{
  "summary": {
    "total_income": 10000,
    "total_expense": 2000,
    "net_balance": 8000
  },
  "category_breakdown": [],
  "monthly_trends": []
}
```

---

## 🔐 Authentication

All protected routes require:
Authorization: Bearer <access_token>

---

## ⚠️ Error Handling

### Common Errors
```json
{
  "detail": "Invalid credentials"
}
```

| Status Code | Meaning |
|------------|--------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## ⚡ Features

- JWT Authentication
- Role-Based Access Control
- Redis Caching (Improves performance)
- Pagination & Filtering
- Scalable FastAPI architecture

---

## 📌 Notes

- Roles: admin, analyst, viewer
- Ensure secure token storage

