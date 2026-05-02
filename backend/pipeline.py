import os
import cv2
from PyPDF2 import PdfReader

# FACE DETECTOR
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def is_selfie(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        return len(faces) > 0

    except:
        return False


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except:
        return ""


def is_resume(text, filename=""):
    text = text.lower()
    filename = filename.lower()

    keywords = [
        "resume", "cv", "education", "skills",
        "experience", "projects", "internship"
    ]

    if "resume" in filename or "cv" in filename:
        return True

    score = sum(1 for word in keywords if word in text)
    return score >= 2


# ✅ ONLY RETURNS RESULT (NO MOVING FILES)
def process_single_file(file_path):

    filename = os.path.basename(file_path)

    # DOCUMENT
    if filename.lower().endswith((".pdf", ".txt", ".doc", ".docx")):

        text = ""
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)

        if is_resume(text, filename):
            return "RESUME"
        else:
            return "OTHER DOCUMENT"

    # IMAGE
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):

        if is_selfie(file_path):
            return "SELFIE"
        else:
            return "NON-SELFIE"

    return "UNSUPPORTED FILE"