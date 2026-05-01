# Organic Botanist — AI Plant Detection Platform

A full-stack plant identification web application powered by a YOLOv8 object detection model, served through an asynchronous FastAPI + Celery pipeline, backed by PostgreSQL, and brokered via Redis. The system supports user authentication, per-user detection history, and a fully connected browser-based frontend — all containerised with Docker Compose.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [System Design](#system-design)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Frontend](#frontend)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [Rebuild Behaviour](#rebuild-behaviour)

---

## Architecture Overview

```
Browser
  │
  ▼
FastAPI (port 8000)          ← serves HTML pages + REST API
  │
  ├── POST /detect           ← accepts image upload
  │       │
  │       └──► Celery Task ──► Redis (broker) ──► Celery Worker
  │                                                     │
  │                                               YOLOv8 inference
  │                                               (best.pt model)
  │                                                     │
  │                                               PostgreSQL write
  │
  ├── GET /result/{task_id}  ← frontend polls until SUCCESS
  │
  └── GET /users/me/history  ← returns completed detections for user
```

The detection pipeline is fully asynchronous. The API accepts an image, enqueues a Celery task, and immediately returns a `task_id`. The frontend polls `/result/{task_id}` every 3 seconds until the worker completes inference and writes the result to PostgreSQL.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI 0.111 |
| ASGI server | Uvicorn 0.29 with WatchFiles hot-reload |
| Task queue | Celery 5.6.2 |
| Message broker / result backend | Redis 7 |
| Object detection model | YOLOv8 via Ultralytics 8.2.18 |
| Deep learning runtime | PyTorch 2.5.1 + TorchVision 0.20.1 |
| Database | PostgreSQL 15 |
| DB driver | psycopg2-binary 2.9.9 |
| Authentication | Custom HMAC-SHA256 signed tokens (JWT-compatible structure, zero extra deps) |
| Frontend | Vanilla HTML + Tailwind CSS (CDN) + ES Modules |
| Containerisation | Docker + Docker Compose v2 |

---

## System Design

### Async Detection Pipeline

1. Client `POST /detect` with `multipart/form-data` image
2. FastAPI writes file to `/shared` volume (shared between API and worker containers)
3. `detect_plant_task.delay(file_path, user_id)` enqueues task to Redis
4. API returns `{ "task_id": "<uuid>" }` immediately
5. Celery worker picks up task, loads YOLOv8 model (kept in memory across tasks), runs inference
6. Worker writes `status=SUCCESS` + JSON result to `plant_tasks` table
7. Frontend polls `GET /result/{task_id}` — returns `{ status, result }` from Celery's Redis backend
8. On `SUCCESS`, result is rendered in the browser

### Authentication Flow

- Passwords hashed with HMAC-SHA256 + 16-byte random salt, stored as base64
- Tokens are `base64url(header).base64url(payload).base64url(HMAC-SHA256-signature)`
- Token payload: `{ sub: user_id, email, exp: unix_timestamp }`
- Token lifetime: 7 days
- All protected endpoints read `Authorization: Bearer <token>` header
- `/detect` accepts optional auth — anonymous detections are allowed but not saved to history

### Container Networking

All services communicate over Docker's internal bridge network by container name:
- API → DB: `plant_db:5432`
- API → Redis: `plant_redis:6379`
- Worker → DB: `plant_db:5432`
- Worker → Redis: `plant_redis:6379`

The `/shared` named volume is mounted in both `api` and `worker` containers so uploaded images are accessible to the worker without HTTP transfer.

---

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI app, all routes, dependency injection
│   ├── worker.py        # Celery app + detect_plant_task task definition
│   ├── detection.py     # PlantDetector class wrapping YOLOv8
│   ├── auth.py          # Password hashing, token creation/verification
│   ├── database.py      # psycopg2 connection factory, RealDictCursor helper
│   └── __init__.py
├── frontend_dist/       # Served directly by FastAPI (no build step)
│   ├── index.html       # Plant identification page (requires auth)
│   ├── login.html       # Sign-in page (served at /)
│   ├── signup.html      # Registration page
│   ├── history.html     # Per-user detection history
│   ├── profile.html     # Profile management
│   └── api.js           # ES module: token management + all fetch wrappers
├── db_init/
│   └── init.sql         # PostgreSQL schema, auto-run on first container start
├── frontend/            # Original static design mockups (reference only)
├── best.pt              # YOLOv8 trained weights (not committed — add manually)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Database Schema

```sql
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    full_name     TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    phone         TEXT,
    bio           TEXT,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE plant_tasks (
    task_id        TEXT PRIMARY KEY,       -- Celery task UUID
    user_id        INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status         TEXT NOT NULL DEFAULT 'PENDING',
    input_file_path TEXT,
    result         TEXT,                   -- JSON-encoded detection result
    created_at     TIMESTAMPTZ DEFAULT NOW()
);
```

Detection results stored in `result` column follow this structure:

```json
{ "detections": [{ "class": "rose", "confidence": 0.943 }] }
// or
{ "status": "No plant is detected" }
```

---

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | None | Create account, returns token |
| `POST` | `/auth/login` | None | Authenticate, returns token |
| `GET` | `/auth/me` | Required | Fetch current user profile |

**Register / Login response:**
```json
{
  "token": "<signed-token>",
  "user": { "id": 1, "full_name": "Jane Smith", "email": "jane@example.com" }
}
```

### User

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `PUT` | `/users/me` | Required | Update full_name, phone, bio |
| `GET` | `/users/me/history` | Required | Last 50 successful detections |

### Detection

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/detect` | Optional | Upload image, returns task_id |
| `GET` | `/result/{task_id}` | None | Poll task status and result |

**Detect request:** `multipart/form-data` with field `file`

**Result response:**
```json
{
  "task_id": "f46b2ea8-56ec-...",
  "status": "SUCCESS",
  "result": { "detections": [{ "class": "sunflower", "confidence": 0.981 }] }
}
```

### Pages

| Method | Endpoint | Serves |
|---|---|---|
| `GET` | `/` | `login.html` |
| `GET` | `/login` | `login.html` |
| `GET` | `/signup` | `signup.html` |
| `GET` | `/identify` | `index.html` (auth-gated client-side) |
| `GET` | `/history` | `history.html` |
| `GET` | `/profile` | `profile.html` |
| `GET` | `/api.js` | ES module shared by all pages |

---

## Authentication

Token format (no external JWT library):

```
base64url({"alg":"HS256","typ":"JWT"})
  .base64url({"sub":<id>,"email":"...","exp":<unix>})
  .base64url(HMAC-SHA256(header.body, SECRET_KEY))
```

The frontend stores the token in `localStorage` under key `ob_token`. Every API request attaches it as `Authorization: Bearer <token>`. A 401 response from any endpoint triggers an automatic logout and redirect to `/login`.

---

## Frontend

All pages are plain HTML files with no build toolchain. Tailwind CSS is loaded from CDN. JavaScript uses native ES Modules (`type="module"`), so `api.js` is imported directly in each page:

```js
import { login, isLoggedIn, fetchHistory } from '/api.js';
```

`api.js` exports:
- `getToken / setToken / removeToken` — localStorage token management
- `getUser / setUser / removeUser` — cached user object
- `isLoggedIn()` — boolean check
- `logout()` — clears storage, redirects to `/login`
- `register(full_name, email, password, phone)` — POST /auth/register
- `login(email, password)` — POST /auth/login
- `fetchMe()` — GET /auth/me
- `updateProfile(payload)` — PUT /users/me
- `detect(file)` — POST /detect with FormData
- `pollResult(taskId, maxAttempts=60, intervalMs=3000)` — polls /result/:id
- `fetchHistory()` — GET /users/me/history

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@plant_db:5432/plants` | PostgreSQL connection string |
| `REDIS_URL` | `redis://plant_redis:6379/0` | Redis broker + backend URL |
| `SECRET_KEY` | `change-me-in-production-...` | HMAC key for token signing — **change this** |

Set in `docker-compose.yml` under each service's `environment` block.

---

## Running Locally

**Prerequisites:** Docker Desktop, `best.pt` model file in project root.

```bash
# First run (builds images, ~10 min due to PyTorch download)
docker-compose up --build

# Subsequent runs (uses cached layers, ~5 sec)
docker-compose up
```

Open **http://localhost:8000**

### Useful commands

```bash
# View live logs
docker logs plant_api -f
docker logs plant_worker -f

# Restart only the API (picks up Python file changes)
docker restart plant_api

# Open a shell inside the API container
docker exec -it plant_api bash

# Connect to PostgreSQL directly
docker exec -it plant_db psql -U postgres -d plants
```

---

## Rebuild Behaviour

| Change made | Action required | Speed |
|---|---|---|
| `app/*.py` | None — uvicorn `--reload` auto-detects | Instant |
| `frontend_dist/*.html` / `api.js` | Hard refresh browser (Ctrl+Shift+R) | Instant |
| `requirements.txt` | `docker-compose up --build` | Slow (pip reinstall) |
| `Dockerfile` | `docker-compose up --build` | Slow |
| `docker-compose.yml` | `docker-compose up` | Fast |

The pip install layer is Docker-cached — it only re-runs when `requirements.txt` changes. PyTorch (~800 MB) is the dominant download on first build.

Frontend Frames:
<img width="1894" height="904" alt="Screenshot 2026-05-01 195030" src="https://github.com/user-attachments/assets/bc59d18f-fa28-4752-aedb-8da848343e2d" />
<img width="1885" height="913" alt="Screenshot 2026-05-01 195125" src="https://github.com/user-attachments/assets/6c224aff-0c80-4828-b571-501be8812ea0" />
<img width="1886" height="893" alt="Screenshot 2026-05-01 195136" src="https://github.com/user-attachments/assets/a4512a71-7ad5-4b96-ae6e-00df21fce75a" />
<img width="1838" height="892" alt="Screenshot 2026-05-01 195151" src="https://github.com/user-attachments/assets/d26a5bbf-f198-4576-8823-c19ffb24bf71" />



