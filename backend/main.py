from fastapi import Header
from jose import JWTError

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

import qrcode
import hashlib
import re
import io

from pymongo import MongoClient

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pydantic import BaseModel

import pytesseract
from PIL import Image

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage
)

from reportlab.lib.styles import getSampleStyleSheet

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

# =========================
# TESSERACT PATH
# =========================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================
# MONGODB CONNECTION
# =========================

client = MongoClient("mongodb://localhost:27017")

db = client["trustchain_ai"]

reports_collection = db["verification_reports"]

users_collection = db["users"]

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# AUTH HELPERS
# =========================

def hash_password(password):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data):

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# VERIFY JWT TOKEN
def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None

# =========================
# PYDANTIC MODELS
# =========================

class UserSignup(BaseModel):

    name: str

    email: str

    password: str


class UserLogin(BaseModel):

    email: str

    password: str

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "TrustChain AI Backend Running"
    }

# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(user: UserSignup):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if existing_user:

        return {
            "message": "User already exists"
        }

    hashed_password = hash_password(
        user.password
    )

    user_data = {

        "name": user.name,

        "email": user.email,

        "password": hashed_password
    }

    users_collection.insert_one(user_data)

    return {
        "message": "Signup successful"
    }

# =========================
# LOGIN
# =========================

@app.post("/login")
def login(user: UserLogin):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if not existing_user:

        return {
            "message": "User not found"
        }

    password_correct = verify_password(
        user.password,
        existing_user["password"]
    )

    if not password_correct:

        return {
            "message": "Invalid password"
        }

    access_token = create_access_token({

        "email": existing_user["email"]

    })

    return {

        "message": "Login successful",

        "access_token": access_token,

        "user": {

            "name": existing_user["name"],

            "email": existing_user["email"]
        }
    }

# =========================
# UPLOAD DOCUMENT
# =========================
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):

    # CHECK AUTH TOKEN
    if not authorization:

        return {
            "message": "Unauthorized"
        }

    token = authorization.split(" ")[1]

    payload = verify_token(token)
    user_email = payload.get("email")

    if not payload:

        return {
            "message": "Invalid Token"
        }

    contents = await file.read()

    # =========================
    # HASH GENERATION
    # =========================

    document_hash = hashlib.sha256(
        contents
    ).hexdigest()

    existing_document = reports_collection.find_one({
        "document_hash": document_hash
    })

    verification_status = "New Document"

    if existing_document:

        verification_status = (
            "Previously Verified Document"
        )

    # =========================
    # IMAGE PROCESSING
    # =========================

    image = Image.open(
        io.BytesIO(contents)
    )

    # =========================
    # METADATA EXTRACTION
    # =========================

    metadata = {}

    metadata["format"] = image.format

    metadata["mode"] = image.mode

    metadata["size"] = image.size

    exif_data = image.getexif()

    for tag_id, value in exif_data.items():

        metadata[str(tag_id)] = str(value)

    # =========================
    # OCR
    # =========================

    extracted_text = pytesseract.image_to_string(
        image
    )

    upper_text = extracted_text.upper()

    # =========================
    # DOCUMENT CLASSIFICATION
    # =========================

    document_category = "Unknown Document"

    if "INCOME TAX" in upper_text:

        document_category = "PAN Card"

    elif "GOVERNMENT OF INDIA" in upper_text:

        document_category = "Aadhaar Card"

    elif "PASSPORT" in upper_text:

        document_category = "Passport"

    elif "INVOICE" in upper_text:

        document_category = "Invoice"

    elif (
        "RESUME" in upper_text
        or "EDUCATION" in upper_text
    ):

        document_category = "Resume"

    # =========================
    # PAN EXTRACTION
    # =========================

    pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"

    pan_match = re.search(
        pan_pattern,
        extracted_text
    )

    pan_number = (
        pan_match.group()
        if pan_match
        else "Not Found"
    )

    # =========================
    # AADHAAR EXTRACTION
    # =========================

    aadhaar_pattern = r"\d{4}\s\d{4}\s\d{4}"

    aadhaar_match = re.search(
        aadhaar_pattern,
        extracted_text
    )

    aadhaar_number = (
        aadhaar_match.group()
        if aadhaar_match
        else "Not Found"
    )

    # =========================
    # INVOICE NUMBER
    # =========================

    invoice_pattern = (
        r"(?i)(invoice\s*(no|number)?[:\-]?\s*[A-Z0-9\-]+)"
    )

    invoice_match = re.search(
        invoice_pattern,
        extracted_text
    )

    invoice_number = (
        invoice_match.group()
        if invoice_match
        else "Not Found"
    )

    # =========================
    # AMOUNT EXTRACTION
    # =========================

    amount_pattern = r"(₹\s?\d+[,\d]*\.?\d*)"

    amount_match = re.search(
        amount_pattern,
        extracted_text
    )

    total_amount = (
        amount_match.group()
        if amount_match
        else "Not Found"
    )

    # =========================
    # GENDER EXTRACTION
    # =========================

    gender = "Not Found"

    if "MALE" in upper_text:

        gender = "Male"

    elif "FEMALE" in upper_text:

        gender = "Female"

    # =========================
    # DOB EXTRACTION
    # =========================

    dob_pattern = r"\d{2}/\d{2}/\d{4}"

    dob_match = re.search(
        dob_pattern,
        extracted_text
    )

    dob = (
        dob_match.group()
        if dob_match
        else "Not Found"
    )

    # =========================
    # NAME EXTRACTION
    # =========================

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

            and not re.search(
                pan_pattern,
                clean_line
            )
        ):

            name = clean_line

            break

    # =========================
    # FRAUD DETECTION
    # =========================

    text_length = len(extracted_text)

    confidence_score = min(
        95,
        max(60, text_length // 10)
    )

    fraud_risk = "Low"

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

    # =========================
    # SAVE TO DATABASE
    # =========================

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

        "user_email": user_email,
    }

    inserted_report = reports_collection.insert_one(
        report_data
    )

    report_id = str(inserted_report.inserted_id)

    # =========================
    # PDF REPORT
    # =========================

    pdf_file = f"report_{report_id}.pdf"

    verification_url = (
        f"http://localhost:5173/verify/{report_id}"
    )

    qr = qrcode.make(
        verification_url
    )

    qr_path = f"qr_{report_id}.png"

    qr.save(qr_path)

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(
            "TrustChain AI Verification Report",
            styles['Title']
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    report_lines = [

        f"Filename: {file.filename}",

        f"Document Category: {document_category}",

        f"Fraud Risk: {fraud_risk}",

        f"Confidence Score: {confidence_score}%",

        f"Verification Status: {verification_status}",

        f"Name: {name}",

        f"PAN Number: {pan_number}",

        f"Aadhaar Number: {aadhaar_number}",

        f"DOB: {dob}",

        f"Gender: {gender}",

        f"Invoice Number: {invoice_number}",

        f"Total Amount: {total_amount}",

        f"Document Hash: {document_hash}"
    ]

    for line in report_lines:

        elements.append(
            Paragraph(
                line,
                styles['BodyText']
            )
        )

        elements.append(
            Spacer(1, 10)
        )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(

        Paragraph(
            "Scan QR for Public Verification",
            styles['Heading2']
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    qr_image = RLImage(
        qr_path,
        width=150,
        height=150
    )

    elements.append(qr_image)

    doc.build(elements)

    # =========================
    # RESPONSE
    # =========================

    return {

        "report_id": report_id,

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

        "verification_status": verification_status
    }

# =========================
# GET REPORTS
# =========================

@app.get("/reports")
def get_reports(
    authorization: str = Header(None)
):

    # CHECK AUTH TOKEN
    if not authorization:

        return {
            "message": "Unauthorized"
        }

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    if not payload:

        return {
            "message": "Invalid Token"
        }

    user_email = payload.get("email")

    reports = list(

        reports_collection.find(
            {
                "user_email": user_email
            },
            {"extracted_text": 0}
        )
    )

    for report in reports:

        report["_id"] = str(
            report["_id"]
        )

    return reports

# =========================
# DOWNLOAD PDF REPORT
# =========================

@app.get("/download-report/{report_id}")
def download_report(report_id: str):

    pdf_file = f"report_{report_id}.pdf"

    return FileResponse(

        pdf_file,

        media_type='application/pdf',

        filename=pdf_file
    )

# =========================
# VERIFY DOCUMENT
# =========================

@app.get("/verify/{report_id}")
def verify_document(report_id: str):

    from bson import ObjectId

    report = reports_collection.find_one({
        "_id": ObjectId(report_id)
    })

    if not report:

        return {
            "status": "Invalid Verification ID"
        }

    return {

        "verification_status": report.get(
            "verification_status"
        ),

        "document_category": report.get(
            "document_category"
        ),

        "filename": report.get(
            "filename"
        ),

        "fraud_risk": report.get(
            "fraud_risk"
        ),

        "confidence_score": report.get(
            "confidence_score"
        ),

        "document_hash": report.get(
            "document_hash"
        )
    }