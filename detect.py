from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("yolo26n.pt")


def predict_image(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    results = model.predict(image)
    
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "label": model.names[int(box.cls)],
                "confidence": round(float(box.conf), 2),
                "bbox": {
                    "x1": int(box.xyxy[0][0]),
                    "y1": int(box.xyxy[0][1]),
                    "x2": int(box.xyxy[0][2]),
                    "y2": int(box.xyxy[0][3])
                }
            })
    
    return detections