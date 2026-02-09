import streamlit as st
import os
import pandas as pd
import re
import random
from src.pipeline import run_custom_ocr

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Thyroid AI Lab Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ================= NAVY BLUE HEALTHCARE BACKGROUND =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: 
        linear-gradient(rgba(0, 31, 63, 0.92), rgba(0, 31, 63, 0.92)),
        url("https://images.unsplash.com/photo-1584982751601-97dcc096659c?auto=format&fit=crop&q=80&w=2000");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #f1f5f9 !important;
}

.main-title {
    font-size: 3.8rem !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    text-align: center;
    margin: 2rem 0 0.5rem 0;
    text-shadow: 0 0 20px rgba(96, 165, 250, 0.6);
}

.sub-title {
    text-align: center;
    color: #93c5fd !important;
    font-size: 1.4rem !important;
    margin-bottom: 40px;
    font-weight: 600;
}

.glass-card {
    background: rgba(30, 41, 59, 0.88) !important;
    backdrop-filter: blur(16px);
    border: 1px solid rgba(96, 165, 250, 0.3) !important;
    padding: 32px;
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    margin: 2rem 0;
    color: #f1f5f9 !important;
}

/* REMOVE ALL RECTANGLE BOXES AROUND UPLOAD & DOWNLOAD */
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] > div,
div.stFileUploader,
[data-testid="stDownloadButton"] > button,
button[kind="primary"],
button[kind="secondary"],
.stDownloadButton,
.stButton,
[data-testid="stHorizontalBlock"] > div,
div[data-testid="stHorizontalBlock"],
[data-testid="stMarkdownContainer"] > div,
div.stMarkdown,
[data-testid="stCaptionContainer"],
.stCaption,
[data-testid="stFileUploadDropzone"] > div,
[data-testid="stFileUploadDropzone"] {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    min-height: 0 !important;
}

/* MAKE UPLOAD AREA VISIBLE & CLEAR - THIS FIXES THE BLANK/FAINT ISSUE */
[data-testid="stFileUploadDropzone"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border-radius: 16px !important;
    padding: 35px !important;
    min-height: 180px !important;
    text-align: center !important;
    border: 2px dashed #60a5fa !important;  /* subtle dashed border for visibility */
}

[data-testid="stFileUploader"] button {
    background: #1e40af !important;
    color: white !important;
    border-radius: 50px !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
    padding: 14px 40px !important;
    border: none !important;
    visibility: visible !important;
    opacity: 1 !important;
}

[data-testid="stFileUploader"] button:hover {
    background: #3b82f6 !important;
}

/* DOWNLOAD BUTTON - ALWAYS VISIBLE WHITE FONT + BLUE */
.stDownloadButton > button {
    background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
    color: white !important;
    border-radius: 50px !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
    padding: 14px 40px !important;
    border: none !important;
    box-shadow: 0 8px 25px rgba(30,64,175,0.35) !important;
    visibility: visible !important;
    opacity: 1 !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #1e3a8a, #2563eb) !important;
    transform: translateY(-3px);
}

.upload-label {
    font-size: 1.6rem !important;
    color: #60a5fa !important;
    font-weight: 900 !important;
    text-align: center;
    margin-bottom: 1.5rem;
}

.stDataFrame {
    background: rgba(30,41,59,0.7) !important;
    border-radius: 16px !important;
    padding: 8px;
}

[data-testid="stDataFrame"] table th {
    background: #1e40af !important;
    color: white !important;
}

[data-testid="stDataFrame"] table td {
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ================= IMPROVED EXTRACTION FUNCTIONS =================

def extract_patient_name(full_text):
    text = full_text.upper()
    
    blacklist = [
        "ROAD","STREET","NAGAR","COLONY","SECTOR","BUILDING","FLOOR","AREA","PIN",
        "CITY","STATE","INDIA","LAB","LABORATORY","HOSPITAL","DIAGNOSTIC","CENTER",
        "PATHOLOGY","COLLECTION","THYROCARE","THYROID","TSH","T3","T4","TEST",
        "RESULT","REPORT","ULTRA","SENSITIVE","REF","RANGE","VALUE","AGE","SEX","GENDER"
    ]
    for word in blacklist:
        text = re.sub(rf'\b{word}\b', ' ', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    patterns = [
        r"PATIENT\s*NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]{4,40})",
        r"NAME\s*[:\-]?\s*([A-Z][A-Z\s\.]{4,40})",
        r"(?:MR|MRS|MS|MISS|KUMARI|MASTER)\.?\s+([A-Z][A-Z\s\.]{4,40})",
        r"([A-Z][A-Z\s\.]{5,35})\s*(?:AGE|SEX|GENDER|DOB|DATE)"
    ]
    
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            name = re.sub(r'\s{2,}', ' ', name)
            if len(name.split()) >= 2 or len(name) > 10:
                return name.title()
    
    return "Patient Name Not Detected"

def extract_test_and_value(full_text):
    test_name = "TSH (Ultra-Sensitive)"
    value = "N/A"
    unit = "µIU/mL"
    ref_range = "0.45 - 4.5"
    
    num_match = re.search(r"(\d+\.?\d+)", full_text)
    if num_match:
        value = num_match.group(1)
    
    unit_match = re.search(r"(µIU/mL|mIU/L|uIU/mL|ng/dL)", full_text, re.IGNORECASE)
    if unit_match:
        unit = unit_match.group(1)
    
    ref_match = re.search(r"(\d+\.?\d+)\s*[-–]\s*(\d+\.?\d+)", full_text)
    if ref_match:
        ref_range = f"{ref_match.group(1)} - {ref_match.group(2)}"
    
    return test_name, value, unit, ref_range

def get_thyroid_status(value_str):
    try:
        val = float(re.search(r"[\d.]+", value_str).group())
        if val < 0.45:
            return "Low"
        elif val > 4.5:
            return "High"
        else:
            return "Normal"
    except:
        return "Not Detected"

def get_full_ocr_text(df):
    text_cols = ["Extracted_Text", "Text", "Cleaned_Text", "Field", "Value"]
    combined = []
    for col in text_cols:
        if col in df.columns:
            combined.extend(df[col].astype(str).tolist())
    return " ".join(combined)

# ================= MAIN UI =================

st.markdown('<h1 class="main-title">Thyroid Lab Report OCR</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Data with Deepa - AI-powered extraction of patient details, values, units & thyroid status</p>', unsafe_allow_html=True)

# Visible upload label + clear area
st.markdown('<p class="upload-label">Browse & Upload Thyroid Lab Report Image</p>', unsafe_allow_html=True)

# File uploader - now visible with cloud icon & Browse files button
files = st.file_uploader(
    "",
    type=["jpg","jpeg","png"],
    accept_multiple_files=False,
    label_visibility="collapsed"
)

if files:
    temp_dir = "temp_processing"
    os.makedirs(temp_dir, exist_ok=True)
    path = os.path.join(temp_dir, files.name)
    with open(path, "wb") as b:
        b.write(files.getbuffer())
    
    with st.spinner("Analyzing lab report..."):
        results = run_custom_ocr([path])
    
    if not results.empty:
        full_text = get_full_ocr_text(results)
        patient_name = extract_patient_name(full_text)
        test_name, result_value, unit, ref_range = extract_test_and_value(full_text)
        status = get_thyroid_status(result_value)
        
        df = pd.DataFrame([{
            "Patient Name": patient_name,
            "Test Name": test_name,
            "Result Value": result_value,
            "Unit": unit,
            "Reference Range": ref_range,
            "Thyroid Detected": status
        }])
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Clinical Diagnostic Matrix")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download CSV Report - blue + always visible
        st.download_button(
            label="Download CSV Report",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="Thyroid_Report.csv",
            mime="text/csv"
        )
        
        # Analysis & Guidance AFTER Download button
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col_a, col_g = st.columns(2)
        
        with col_a:
            st.subheader("Analysis")
            st.markdown(f"**Patient:** {patient_name}")
            st.markdown(f"**Health Status:** {status}")
        
        with col_g:
            st.subheader("Guidance")
            if status in ["Low", "High"]:
                st.error("Abnormal thyroid detected. Consult doctor immediately.")
            else:
                st.success("Thyroid appears normal. Continue routine monitoring.")
            st.markdown("""
            • Retest T3/T4 if symptoms persist
            • Follow doctor's prescription strictly
            • Avoid self-medication
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.error("Could not extract text clearly. Please upload a high-resolution image.")

st.markdown(
    "<p style='text-align:center;color:#93c5fd;font-size:0.95rem;margin-top:40px;'>Thyroid Diagnostics AI • Secure • Accurate • Clinical Grade</p>",
    unsafe_allow_html=True
)