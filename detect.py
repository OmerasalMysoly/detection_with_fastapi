from ultralytics import YOLO
import cv2
import base64
import tempfile
import os

model= YOLO("yolo26n.pt")

def predict_image(image_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    results = model.predict(tmp_path)
    os.remove(tmp_path)

    detections = []
    annotated_image = None
    for result in results:
        annotated_image = result.plot()
        for box in result.boxes:
            detections.append({
                "label": model.names[int(box.cls)],
                "confidence": round(float(box.conf), 2)
            })

    _, buffer = cv2.imencode(".jpg", annotated_image)
    base64_image = base64.b64encode(buffer).decode("utf-8")

    return detections, base64_image