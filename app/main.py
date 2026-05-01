import os
import json
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from celery.result import AsyncResult

from app.worker import detect_plant_task, celery_app
from app.database import get_db_connection, get_cursor
from app.auth import hash_password, verify_password, create_token, decode_token

app = FastAPI(title="Organic Botanist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/shared"
os.makedirs(UPLOAD_DIR, exist_ok=True)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend_dist")


# ── Auth helpers ──────────────────────────────────────────────────────────────

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Extract and validate Bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Like get_current_user but returns None instead of raising."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    return decode_token(token)


# ── Pydantic models ───────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None


# ── Auth endpoints ────────────────────────────────────────────────────────────

@app.post("/auth/register", status_code=201)
def register(body: RegisterRequest):
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (body.email,))
            if cur.fetchone():
                raise HTTPException(status_code=409, detail="Email already registered")
            pw_hash = hash_password(body.password)
            cur.execute(
                "INSERT INTO users (full_name, email, phone, password_hash) VALUES (%s, %s, %s, %s) RETURNING id, full_name, email",
                (body.full_name, body.email, body.phone, pw_hash),
            )
            user = dict(cur.fetchone())
            conn.commit()
    finally:
        conn.close()

    token = create_token(user["id"], user["email"])
    return {"token": token, "user": {"id": user["id"], "full_name": user["full_name"], "email": user["email"]}}


@app.post("/auth/login")
def login(body: LoginRequest):
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute("SELECT id, full_name, email, password_hash FROM users WHERE email = %s", (body.email,))
            row = cur.fetchone()
    finally:
        conn.close()

    if not row or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(row["id"], row["email"])
    return {"token": token, "user": {"id": row["id"], "full_name": row["full_name"], "email": row["email"]}}


@app.get("/auth/me")
def me(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute(
                "SELECT id, full_name, email, phone, bio, created_at FROM users WHERE id = %s",
                (current_user["sub"],),
            )
            user = cur.fetchone()
    finally:
        conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)


# ── Profile endpoint ──────────────────────────────────────────────────────────

@app.put("/users/me")
def update_profile(body: UpdateProfileRequest, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute(
                """
                UPDATE users
                SET full_name = COALESCE(%s, full_name),
                    phone     = COALESCE(%s, phone),
                    bio       = COALESCE(%s, bio)
                WHERE id = %s
                RETURNING id, full_name, email, phone, bio
                """,
                (body.full_name, body.phone, body.bio, current_user["sub"]),
            )
            user = cur.fetchone()
            conn.commit()
    finally:
        conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)


# ── Detection endpoints ───────────────────────────────────────────────────────

@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    current_user: Optional[dict] = Depends(get_optional_user),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    user_id = current_user["sub"] if current_user else None
    task = detect_plant_task.delay(file_path, user_id)
    return {"task_id": task.id}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }


# ── History endpoint ──────────────────────────────────────────────────────────

@app.get("/users/me/history")
def get_history(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute(
                """
                SELECT task_id, status, result, created_at
                FROM plant_tasks
                WHERE user_id = %s AND status = 'SUCCESS'
                ORDER BY created_at DESC
                LIMIT 50
                """,
                (current_user["sub"],),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    history = []
    for row in rows:
        entry = dict(row)
        if entry.get("result"):
            try:
                entry["result"] = json.loads(entry["result"])
            except Exception:
                pass
        history.append(entry)
    return history


# ── Static frontend serving ───────────────────────────────────────────────────

# Serve api.js explicitly so ES module imports work as /api.js
@app.get("/api.js")
def serve_api_js():
    return FileResponse(os.path.join(FRONTEND_DIR, "api.js"), media_type="application/javascript")


def _page(name: str):
    path = os.path.join(FRONTEND_DIR, name)
    if os.path.isfile(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Page not found")


@app.get("/")
def home():
    return _page("login.html")


@app.get("/identify")
def identify_page():
    return _page("index.html")


@app.get("/login")
def login_page():
    return _page("login.html")


@app.get("/signup")
def signup_page():
    return _page("signup.html")


@app.get("/history")
def history_page():
    return _page("history.html")


@app.get("/profile")
def profile_page():
    return _page("profile.html")
