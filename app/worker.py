from celery import Celery
from app.detection import PlantDetector
import psycopg2

# ----------------------------
# Redis for Celery
# ----------------------------
REDIS_URL = "redis://plant_redis:6379/0"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# ----------------------------
# PostgreSQL inside Docker
# ----------------------------
DATABASE_URL = "postgresql://postgres:postgres@plant_db:5432/plants"
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# ----------------------------
# Plant Detector
# ----------------------------
detector = PlantDetector("/app/best.pt")

# ----------------------------
# Celery task
# ----------------------------
@celery_app.task(name="detect_plant_task", bind=True)
def detect_plant_task(self, file_path):
    task_id = self.request.id

    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO plant_tasks (task_id, status, input_file_path) VALUES (%s, %s, %s)",
            (task_id, "STARTED", file_path)
        )
        conn.commit()

    result = detector.detect(file_path)

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE plant_tasks SET status=%s, result_file_path=%s WHERE task_id=%s",
            ("SUCCESS", str(result), task_id)
        )
        conn.commit()

    conn.close()

    return result