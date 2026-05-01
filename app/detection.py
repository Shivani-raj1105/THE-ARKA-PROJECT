import os
from ultralytics import YOLO
class PlantDetector:
    def __init__(self, model_path="best.pt"):
        self.model = YOLO(os.path.abspath(model_path))
    def detect(self, source_path):
        source_path = os.path.abspath(source_path)
        results = self.model(source_path)
        detections = []
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = self.model.names[class_id]
                detections.append({
                    "class": class_name,
                    "confidence": round(confidence, 3)
                })
        if not detections:
            return {"status": "No plant is detected"}
        return {"detections": detections}