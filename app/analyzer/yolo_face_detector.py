from ultralytics import YOLO
import cv2

model = YOLO("yolo11n.pt")


def detect_faces(frame_path):
    results = model(frame_path)

    faces = []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()

        for box in boxes:
            x1, y1, x2, y2 = box

            faces.append({
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2)
            })

    return faces