import cv2
import pandas as pd
import os
from .detector import detect_objects, YOLO_LOADED     # ← dot . is important
from .ocr_engine import extract_text_from_crop
from .config import TRAIN_IMAGES, TEST_IMAGES, OUTPUT_DIR
import pytesseract
import cv2

def run_custom_ocr(image_paths):
    all_results = []

    for path in image_paths if isinstance(image_paths, list) else [image_paths]:
        if not os.path.exists(path):
            print(f"File missing: {path}")
            continue

        print(f"→ {os.path.basename(path)}")
        img = cv2.imread(path)
        if img is None:
            continue

        detections = detect_objects(img)

        page_results = []
        if YOLO_LOADED and detections:
            for det in detections:
                x, y, w, h = det["box"]
                label = det["label"]
                crop = img[y:y+h, x:x+w]
                text = extract_text_from_crop(crop)
                page_results.append({
                    "Field": label,
                    "Value": text,
                    "Method": "YOLO crop",
                    "Image": os.path.basename(path)
                })
        else:
            # fallback full page
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(thresh, config=r'--oem 3 --psm 6')
            page_results.append({
                "Field": "Full Page Text",
                "Value": text[:500] + " ...",
                "Method": "Full page OCR",
                "Image": os.path.basename(path)
            })

        all_results.extend(page_results)

    if all_results:
        df = pd.DataFrame(all_results)
        csv_path = os.path.join(OUTPUT_DIR, "results.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"Saved → {csv_path}")
        return df
    return pd.DataFrame()