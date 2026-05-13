import hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import FileResponse
from pymongo import MongoClient

import re
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pytesseract
from PIL import Image
import io

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")

db = client["trustchain_ai"]

reports_collection = db["verification_reports"]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "TrustChain AI Backend Running"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Read uploaded image
    contents = await file.read()

    # Generate SHA-256 Hash
    document_hash = hashlib.sha256(contents).hexdigest()

    # Check Existing Verification Record
    existing_document = reports_collection.find_one({
    "document_hash": document_hash
})

    verification_status = "New Document"

    if existing_document:
        verification_status = "Previously Verified Document"

    # Convert image
    image = Image.open(io.BytesIO(contents))

    # Metadata Extraction
    metadata = {}

    metadata["format"] = image.format
    metadata["mode"] = image.mode
    metadata["size"] = image.size

    # EXIF Metadata
    exif_data = image.getexif()

    for tag_id, value in exif_data.items():

     tag = str(tag_id)

     metadata[tag] = str(value)

    # OCR Extraction
    extracted_text = pytesseract.image_to_string(image)

    # Convert OCR text to uppercase
    upper_text = extracted_text.upper()

    # Document Classification
    document_category = "Unknown Document"

    if "INCOME TAX" in upper_text:
        document_category = "PAN Card"

    elif "GOVERNMENT OF INDIA" in upper_text:
        document_category = "Aadhaar Card"

    elif "PASSPORT" in upper_text:
        document_category = "Passport"

    elif "INVOICE" in upper_text:
        document_category = "Invoice"

    elif "RESUME" in upper_text or "EDUCATION" in upper_text:
        document_category = "Resume"

    # PAN Extraction
    pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
    pan_match = re.search(pan_pattern, extracted_text)

    pan_number = pan_match.group() if pan_match else "Not Found"

    # Aadhaar Number Extraction
    aadhaar_pattern = r"\d{4}\s\d{4}\s\d{4}"
    aadhaar_match = re.search(aadhaar_pattern, extracted_text)

    aadhaar_number = (
        aadhaar_match.group()
        if aadhaar_match
        else "Not Found"
    )
    # Invoice Number Extraction
    invoice_pattern = r"(?i)(invoice\s*(no|number)?[:\-]?\s*[A-Z0-9\-]+)"
    invoice_match = re.search(invoice_pattern, extracted_text)

    invoice_number = (
    invoice_match.group()
    if invoice_match
    else "Not Found"
    )

    # Amount Extraction
    amount_pattern = r"(₹\s?\d+[,\d]*\.?\d*)"
    amount_match = re.search(amount_pattern, extracted_text)

    total_amount = (
    amount_match.group()
    if amount_match
    else "Not Found"
)

    # Gender Extraction
    gender = "Not Found"

    if "MALE" in upper_text:
        gender = "Male"

    elif "FEMALE" in upper_text:
        gender = "Female"

    # DOB Extraction
    dob_pattern = r"\d{2}/\d{2}/\d{4}"
    dob_match = re.search(dob_pattern, extracted_text)

    dob = dob_match.group() if dob_match else "Not Found"

    # Name Extraction
    lines = extracted_text.split("\n")

    name = "Not Found"

    for line in lines:

        clean_line = line.strip()

        if (
            clean_line.isupper()
            and len(clean_line) > 5
            and "INCOME TAX" not in clean_line
            and "GOVERNMENT OF INDIA" not in clean_line
            and "PASSPORT" not in clean_line
            and not re.search(pan_pattern, clean_line)
        ):
            name = clean_line
            break

    # Fake AI Verification Logic
    text_length = len(extracted_text)

    confidence_score = min(95, max(60, text_length // 10))

    fraud_risk = "Low"

    # Metadata-based tampering analysis

    metadata_string = str(metadata).lower()

    if (
    "photoshop" in metadata_string
    or "canva" in metadata_string
    or "editor" in metadata_string
):
        fraud_risk = "High"

    if text_length < 50:
        fraud_risk = "High"

    elif text_length < 150:
        fraud_risk = "Medium"

    report_data = {
    "filename": file.filename,
    "document_type": file.content_type,
    "document_category": document_category,
    "confidence_score": confidence_score,
    "fraud_risk": fraud_risk,
    "name": name,
    "pan_number": pan_number,
    "aadhaar_number": aadhaar_number,
    "gender": gender,
    "dob": dob,
    "invoice_number": invoice_number,
    "total_amount": total_amount,
    "extracted_text": extracted_text,
    "document_hash": document_hash,
    "verification_status": verification_status,
}

    reports_collection.insert_one(report_data)   

    # Final Response
    return {
        "filename": file.filename,
        "document_type": file.content_type,
        "document_category": document_category,
        "confidence_score": confidence_score,
        "fraud_risk": fraud_risk,
        "name": name,
        "pan_number": pan_number,
        "aadhaar_number": aadhaar_number,
        "invoice_number": invoice_number,
        "total_amount": total_amount,
        "gender": gender,
        "dob": dob,
        "extracted_text": extracted_text,
        "metadata": metadata,
        "document_hash": document_hash,
        "verification_status": verification_status,
    }

@app.get("/reports")
def get_reports():

    reports = list(
        reports_collection.find({}, {"extracted_text": 0})
    )

    for report in reports:
        report["_id"] = str(report["_id"])

    return reports

@app.get("/download-report/{report_id}")
def download_report(report_id: str):

    from bson import ObjectId

    report = reports_collection.find_one({
        "_id": ObjectId(report_id)
    })

    if not report:
        return {"error": "Report not found"}

    pdf_file = f"report_{report_id}.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "TrustChain AI Verification Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    report_lines = [

        f"Filename: {report.get('filename')}",

        f"Document Category: {report.get('document_category')}",

        f"Fraud Risk: {report.get('fraud_risk')}",

        f"Confidence Score: {report.get('confidence_score')}%",

        f"Name: {report.get('name')}",

        f"PAN Number: {report.get('pan_number')}",

        f"Aadhaar Number: {report.get('aadhaar_number')}",

        f"DOB: {report.get('dob')}",

        f"Gender: {report.get('gender')}",

        f"Invoice Number: {report.get('invoice_number')}",

        f"Total Amount: {report.get('total_amount')}"

    ]

    for line in report_lines:

        elements.append(
            Paragraph(line, styles['BodyText'])
        )

        elements.append(Spacer(1, 10))

    doc.build(elements)

    return FileResponse(
        pdf_file,
        media_type='application/pdf',
        filename=pdf_file
    )