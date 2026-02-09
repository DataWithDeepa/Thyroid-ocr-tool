import os

BASE_DIR = r"C:\Users\DEEPA\OneDrive\ドキュメント\DIGICROME CLASS\Internship project\Thyroid_Lab_OCR"

TRAIN_IMAGES = [
    os.path.join(BASE_DIR, "images", "train1.jpg"),
    os.path.join(BASE_DIR, "images", "train2.jpg"),
    os.path.join(BASE_DIR, "images", "train3.jpg"),
    os.path.join(BASE_DIR, "images", "train4.jpg"),
    os.path.join(BASE_DIR, "images", "train5.jpg"),
    os.path.join(BASE_DIR, "images", "train5 (1).jpg"),
]

TEST_IMAGES = [
    os.path.join(BASE_DIR, "images", "train", "test", "test1.txt.jpg"),
    os.path.join(BASE_DIR, "images", "train", "test", "test2.txt.jpg"),
    os.path.join(BASE_DIR, "images", "train", "test", "test3.txt.jpg"),
    os.path.join(BASE_DIR, "images", "train", "test", "test4.txt.jpg"),
]

MODEL_DIR = os.path.join(BASE_DIR, "model")
YOLO_WEIGHTS = os.path.join(MODEL_DIR, "yolov3_custom.weights")
YOLO_CFG     = os.path.join(MODEL_DIR, "yolov3.cfg")
YOLO_CLASSES = os.path.join(MODEL_DIR, "classes.names")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)