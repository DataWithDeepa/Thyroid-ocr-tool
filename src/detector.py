import cv2
import numpy as np
from .config import YOLO_WEIGHTS, YOLO_CFG, YOLO_CLASSES   # note the dot .

YOLO_LOADED = False
net = None
classes = []

try:
    net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
    with open(YOLO_CLASSES, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    YOLO_LOADED = True
    print("YOLO model loaded successfully")
except Exception as e:
    print("YOLO could not load → using full-page OCR fallback")
    print("Reason:", str(e))

def detect_objects(image, conf_threshold=0.5, nms_threshold=0.4):
    if not YOLO_LOADED or net is None:
        return []

    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())

    boxes, confidences, class_ids = [], [], []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(np.argmax(scores))
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    detections = []
    for i in indices.flatten():
        detections.append({
            "label": classes[class_ids[i]],
            "box": boxes[i],
            "confidence": confidences[i]
        })
    return detections