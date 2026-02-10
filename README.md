# Thyroid Lab Report OCR Tool

**AI-Powered Custom OCR for Thyroid Lab Reports**

This project extracts key information from thyroid lab reports using **YOLOv3** for region detection + **Tesseract OCR** for text extraction. It identifies patient name, TSH value, unit, reference range, classifies thyroid status (**Low/Hyperthyroid**, **High/Hypothyroid**, **Normal**), provides analysis & medical guidance, and allows CSV download.

Built during **Internship at Nexthikes IT Solution**  
Developed by: **Deepa Pathak**

### Features
- Custom-trained YOLOv3 model for accurate region detection in lab reports
- Preprocessing (resize, grayscale, threshold, Otsu) for better OCR accuracy
- Auto-detects patient name (ignores address/lab text)
- Extracts TSH value, unit, reference range
- Classifies thyroid status with color-coded result
- Professional analysis & doctor consultation guidance (e.g., "Consult doctor immediately" if abnormal)
- One-click CSV export of results

### Tech Stack
- **Frontend/UI**: Streamlit
- **Object Detection**: YOLOv3 (custom trained)
- **OCR Engine**: Tesseract + PyTesseract
- **Image Processing**: OpenCV
- **Data Handling**: Pandas, NumPy, Re (regex)

### How to Run Locally
1. Clone the repo:
2. Install dependencies: 
3. Install Tesseract OCR on your system:
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Linux/Mac: `sudo apt install tesseract-ocr` or `brew install tesseract`

4. Run the app:
   
### Live Demo
(Deploying soon on Streamlit Cloud – link coming!)

### Installation Notes
- Make sure Tesseract is in your PATH (or set path in code if needed)
- Use `opencv-python-headless` for cloud deployment

### Internship Details
**Project Title:** Custom-Object Character Recognition (OCR) for Thyroid Lab Reports  
**Organization:** Nexthikes IT Solution  
**Developed by:** Deepa Pathak

Made with ❤️ during internship

Star ⭐ the repo if you find it useful!
