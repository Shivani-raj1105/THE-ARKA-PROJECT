import json
import os
from celery import Celery
from app.detection import PlantDetector
from app.database import get_db_connection, get_cursor

REDIS_URL = os.getenv("REDIS_URL", "redis://plant_redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

detector = PlantDetector("/app/best.pt")


@celery_app.task(name="detect_plant_task", bind=True)
def detect_plant_task(self, file_path: str, user_id: int = None):
    task_id = self.request.id
    conn = get_db_connection()
    try:
        with get_cursor(conn) as cur:
            cur.execute(
                """
                INSERT INTO plant_tasks (task_id, user_id, status, input_file_path)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE
                    SET status = EXCLUDED.status
                """,
                (task_id, user_id, "STARTED", file_path),
            )
            conn.commit()

        result = detector.detect(file_path)

        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE plant_tasks SET status=%s, result=%s WHERE task_id=%s",
                ("SUCCESS", json.dumps(result), task_id),
            )
            conn.commit()
    except Exception as exc:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE plant_tasks SET status=%s, result=%s WHERE task_id=%s",
                ("FAILURE", json.dumps({"error": str(exc)}), task_id),
            )
            conn.commit()
        raise
    finally:
        conn.close()

    return result
