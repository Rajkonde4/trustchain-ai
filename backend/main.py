import fitz
from bson import ObjectId

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

from fastapi import Header

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

import qrcode
import hashlib
import re
import io

from app.routes import upload_routes

from app.utils.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

from app.utils.validators import (
    validate_file_type,
    validate_file_size
)

from app.services.ocr_service import (
    extract_text_from_pdf,
    extract_text_from_image
)

from app.services.fraud_service import (
    analyze_document_risk
)

from app.routes import auth_routes


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

app.include_router(
    auth_routes.router
)

app.include_router(
    upload_routes.router
)


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

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["trustchain_ai"]

reports_collection = db["verification_reports"]

users_collection = db["users"]

auth_routes.users_collection = users_collection

upload_routes.reports_collection = reports_collection

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

    except Exception as e:

        print("TOKEN ERROR:", e)

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

    # INVALID TOKEN
    if not payload:

        return {
            "message": "Invalid Token"
        }

    user_email = payload.get("email")

    # =========================
    # FILE VALIDATION
    # =========================

    allowed_types = [

        "application/pdf",

        "image/png",

        "image/jpeg",

        "image/jpg"
    ]

    # INVALID FILE TYPE
    if file.content_type not in allowed_types:

        return {
            "message": "Unsupported File Type"
        }

    contents = await file.read()

    # EMPTY FILE
    if not contents:

        return {
            "message": "Empty File"
        }

    # FILE SIZE LIMIT
    max_size = 10 * 1024 * 1024

    if len(contents) > max_size:

        return {
            "message": "File Too Large"
        }

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
    # FILE PROCESSING
    # =========================

    metadata = {}

    extracted_text = ""

    # =========================
    # PDF SUPPORT
    # =========================

    if file.content_type == "application/pdf":

        pdf_document = fitz.open(
            stream=contents,
            filetype="pdf"
        )

        metadata["pages"] = len(pdf_document)

        for page_number in range(len(pdf_document)):

            page = pdf_document.load_page(
                page_number
            )

            pix = page.get_pixmap()

            image_bytes = pix.tobytes("png")

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            page_text = pytesseract.image_to_string(
                image
            )

            extracted_text += page_text + "\n"

    # =========================
    # IMAGE SUPPORT
    # =========================

    else:

        image = Image.open(
            io.BytesIO(contents)
        )

        metadata["format"] = image.format

        metadata["mode"] = image.mode

        metadata["size"] = image.size

        exif_data = image.getexif()

        for tag_id, value in exif_data.items():

            metadata[str(tag_id)] = str(value)

        extracted_text = pytesseract.image_to_string(
            image
        )

    # =========================
    # NORMALIZED TEXT
    # =========================

    upper_text = extracted_text.upper()

    # =========================
    # DOCUMENT CLASSIFICATION
    # =========================

    document_category = "Unknown Document"

    # PAN CARD
    if (

        "INCOME TAX" in upper_text

        or "PERMANENT ACCOUNT NUMBER" in upper_text

    ):

        document_category = "PAN Card"

    # AADHAAR
    elif (

        "GOVERNMENT OF INDIA" in upper_text

        or "UNIQUE IDENTIFICATION AUTHORITY" in upper_text

        or "AADHAAR" in upper_text

    ):

        document_category = "Aadhaar Card"

    # PASSPORT
    elif (

        "PASSPORT" in upper_text

        or "REPUBLIC OF INDIA" in upper_text

    ):

        document_category = "Passport"

    # INVOICE
    elif (

        "INVOICE" in upper_text

        or "BILL TO" in upper_text

        or "GSTIN" in upper_text

    ):

        document_category = "Invoice"

    # RESUME / CV
    elif (

        "RESUME" in upper_text

        or "CURRICULUM VITAE" in upper_text

        or "EDUCATION" in upper_text

        or "SKILLS" in upper_text

        or "EXPERIENCE" in upper_text

    ):

        document_category = "Resume"

    # DRIVING LICENSE
    elif (

        "DRIVING LICENCE" in upper_text

        or "DRIVING LICENSE" in upper_text

        or "TRANSPORT DEPARTMENT" in upper_text

    ):

        document_category = "Driving License"

    # BANK STATEMENT
    elif (

        "ACCOUNT STATEMENT" in upper_text

        or "BANK STATEMENT" in upper_text

        or "IFSC" in upper_text

        or "ACCOUNT NUMBER" in upper_text

    ):

        document_category = "Bank Statement"

    # ACADEMIC CERTIFICATE
    elif (

        "CERTIFICATE" in upper_text

        or "UNIVERSITY" in upper_text

        or "COLLEGE" in upper_text

        or "GRADE" in upper_text

        or "CGPA" in upper_text

    ):

        document_category = "Academic Certificate"

    # MARKSHEET
    elif (

        "MARKSHEET" in upper_text

        or "MARKS" in upper_text

        or "SEMESTER" in upper_text

        or "RESULT" in upper_text

    ):

        document_category = "Marksheet"

    # VOTER ID
    elif (

        "ELECTION COMMISSION OF INDIA" in upper_text

        or "VOTER ID" in upper_text

        or "ELECTOR" in upper_text

    ):

        document_category = "Voter ID"

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
    # PASSPORT EXTRACTION
    # =========================

    passport_number = "Not Found"

    nationality = "Not Found"

    expiry_date = "Not Found"

    if document_category == "Passport":

        # PASSPORT NUMBER
        passport_pattern = r"[A-Z]{1}[0-9]{7}"

        passport_match = re.search(
            passport_pattern,
            extracted_text
        )

        if passport_match:

            passport_number = passport_match.group()

        # NATIONALITY
        if "INDIAN" in upper_text:

            nationality = "Indian"

        # EXPIRY DATE
        expiry_pattern = r"\d{2}/\d{2}/\d{4}"

        expiry_matches = re.findall(
            expiry_pattern,
            extracted_text
        )

        if len(expiry_matches) >= 2:

            expiry_date = expiry_matches[-1]

    # =========================
    # RESUME EXTRACTION
    # =========================

    resume_email = "Not Found"

    resume_phone = "Not Found"

    skills_found = []

    if document_category == "Resume":

        # EMAIL
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        email_match = re.search(
            email_pattern,
            extracted_text
        )

        if email_match:

            resume_email = email_match.group()

        # PHONE
        phone_pattern = r"\+?\d[\d\s\-]{8,15}"

        phone_match = re.search(
            phone_pattern,
            extracted_text
        )

        if phone_match:

            resume_phone = phone_match.group()

        # SKILLS
        skill_keywords = [

            "PYTHON",
            "JAVA",
            "JAVASCRIPT",
            "REACT",
            "NODE",
            "DJANGO",
            "MONGODB",
            "SQL",
            "HTML",
            "CSS",
            "MACHINE LEARNING",
            "AI",
            "DATA ANALYTICS"

        ]

        for skill in skill_keywords:

            if skill in upper_text:

                skills_found.append(skill)

    # =========================
    # BANK STATEMENT EXTRACTION
    # =========================

    bank_name = "Not Found"

    account_number = "Not Found"

    ifsc_code = "Not Found"

    if document_category == "Bank Statement":

        # ACCOUNT NUMBER
        account_pattern = r"\b\d{9,18}\b"

        account_match = re.search(
            account_pattern,
            extracted_text
        )

        if account_match:

            account_number = account_match.group()

        # IFSC
        ifsc_pattern = r"[A-Z]{4}0[A-Z0-9]{6}"

        ifsc_match = re.search(
            ifsc_pattern,
            extracted_text
        )

        if ifsc_match:

            ifsc_code = ifsc_match.group()

        # BANK NAME
        bank_keywords = [

            "STATE BANK OF INDIA",
            "HDFC BANK",
            "ICICI BANK",
            "AXIS BANK",
            "BANK OF BARODA",
            "PUNJAB NATIONAL BANK"

        ]

        for bank in bank_keywords:

            if bank in upper_text:

                bank_name = bank

    # =========================
    # DRIVING LICENSE EXTRACTION
    # =========================

    license_number = "Not Found"

    if document_category == "Driving License":

        license_pattern = r"[A-Z]{2}\d{2}\s?\d{11}"

        license_match = re.search(
            license_pattern,
            extracted_text
        )

        if license_match:

            license_number = license_match.group()

    # =========================
    # CERTIFICATE EXTRACTION
    # =========================

    university_name = "Not Found"

    cgpa = "Not Found"

    if (

        document_category == "Academic Certificate"

        or document_category == "Marksheet"

    ):

        # UNIVERSITY
        university_keywords = [

            "UNIVERSITY",
            "COLLEGE",
            "INSTITUTE"

        ]

        for line in lines:

            for keyword in university_keywords:

                if keyword in line.upper():

                    university_name = line.strip()

                    break

        # CGPA
        cgpa_pattern = r"\b\d\.\d{1,2}\b"

        cgpa_match = re.search(
            cgpa_pattern,
            extracted_text
        )

        if cgpa_match:

            cgpa = cgpa_match.group()

    # =========================
    # VOTER ID EXTRACTION
    # =========================

    voter_id = "Not Found"

    if document_category == "Voter ID":

        voter_pattern = r"[A-Z]{3}[0-9]{7}"

        voter_match = re.search(
            voter_pattern,
            extracted_text
        )

        if voter_match:

            voter_id = voter_match.group()   

    # =========================
    # FRAUD DETECTION
    # =========================

    text_length = len(extracted_text)

    metadata_string = str(metadata).lower()

    confidence_score = 50

    fraud_risk = "Low"

    # =========================
    # OCR QUALITY
    # =========================

    if text_length > 500:

        confidence_score += 20

    elif text_length > 200:

        confidence_score += 15

    elif text_length > 100:

        confidence_score += 10

    else:

        confidence_score -= 15

    # =========================
    # DOCUMENT FIELD DETECTION
    # =========================

    if pan_number != "Not Found":

        confidence_score += 10

    if aadhaar_number != "Not Found":

        confidence_score += 10

    if invoice_number != "Not Found":

        confidence_score += 8

    if total_amount != "Not Found":

        confidence_score += 5

    if name != "Not Found":

        confidence_score += 7

    if dob != "Not Found":

        confidence_score += 5

    # =========================
    # DOCUMENT CATEGORY BONUS
    # =========================

    if document_category != "Unknown Document":

        confidence_score += 10

    # =========================
    # METADATA TAMPERING CHECK
    # =========================

    if (

        "photoshop" in metadata_string

        or "canva" in metadata_string

        or "editor" in metadata_string

    ):

        fraud_risk = "High"

        confidence_score -= 30

    # =========================
    # LOW OCR QUALITY
    # =========================

    if text_length < 50:

        fraud_risk = "High"

        confidence_score -= 20

    elif text_length < 150:

        if fraud_risk != "High":

            fraud_risk = "Medium"

        confidence_score -= 10

    # =========================
    # NORMALIZE SCORE
    # =========================

    confidence_score = max(
        35,
        min(confidence_score, 98)
    )

    # =========================
    # FINAL RISK ADJUSTMENT
    # =========================

    if confidence_score < 50:

        fraud_risk = "High"

    elif confidence_score < 75:

        if fraud_risk != "High":

            fraud_risk = "Medium"

    else:

        if fraud_risk != "High":

            fraud_risk = "Low"

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
    pdf_file = f"reports/report_{report_id}.pdf"
    

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL"
    )

    verification_url = (
        f"{FRONTEND_URL}/verify/{report_id}"
    )

    qr = qrcode.make(
        verification_url
    )

    qr_path = f"qr_codes/qr_{report_id}.png"

    qr.save(qr_path)

    doc = SimpleDocTemplate(
        pdf_file,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # CUSTOM TITLE STYLE
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563EB")
    )

    # HEADER
    elements.append(

        Paragraph(
            "NEW PROFESSIONAL REPORT",
            title_style
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # SUMMARY TABLE
    summary_data = [

        ["Field", "Value"],

        ["Filename", file.filename],

        ["Document Category", document_category],

        ["Verification Status", verification_status],

        ["Fraud Risk", fraud_risk],

        ["Confidence Score", f"{confidence_score}%"],

        ["Document Hash", document_hash[:40] + "..."]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[180, 300]
    )

    summary_table.setStyle(

        TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563EB")),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('FONTSIZE', (0, 0), (-1, -1), 11),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),

            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
            [colors.whitesmoke, colors.beige]),
        ])
    )

    elements.append(summary_table)

    elements.append(
        Spacer(1, 30)
    )

    # EXTRACTED INFO TITLE
    elements.append(

        Paragraph(
            "Extracted Information",
            styles['Heading2']
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # EXTRACTED INFO TABLE
    info_data = [

        ["Name", name],

        ["PAN Number", pan_number],

        ["Aadhaar Number", aadhaar_number],

        ["DOB", dob],

        ["Gender", gender],

        ["Invoice Number", invoice_number],

        ["Total Amount", total_amount]
    ]

    info_table = Table(
        info_data,
        colWidths=[180, 300]
    )

    info_table.setStyle(

        TableStyle([

            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),

            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),

            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ])
    )

    elements.append(info_table)

    elements.append(
        Spacer(1, 30)
    )

    # FRAUD ANALYSIS
    elements.append(

        Paragraph(
            "Fraud Analysis",
            styles['Heading2']
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    fraud_color = {

        "Low": "green",
        "Medium": "orange",
        "High": "red"

    }.get(fraud_risk, "black")

    fraud_text = f"""
    <b>Risk Level:</b>
    <font color="{fraud_color}">
    {fraud_risk}
    </font>
    """

    elements.append(

        Paragraph(
            fraud_text,
            styles['BodyText']
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    # QR SECTION
    elements.append(

        Paragraph(
            "Public Verification QR",
            styles['Heading2']
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    qr_image = RLImage(
        qr_path,
        width=140,
        height=140
    )

    elements.append(qr_image)

    elements.append(
        Spacer(1, 12)
    )

    elements.append(

        Paragraph(
            verification_url,
            styles['BodyText']
        )
    )

    elements.append(
        Spacer(1, 30)
    )

    # FOOTER
    elements.append(

        Paragraph(
            "Generated securely by TrustChain AI",
            styles['Italic']
        )
    )

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

        "verification_status": verification_status,

        "passport_number": passport_number,
        "nationality": nationality,
        "expiry_date": expiry_date,

        "resume_email": resume_email,
        "resume_phone": resume_phone,
        "skills_found": skills_found,

        "bank_name": bank_name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,

        "license_number": license_number,

        "university_name": university_name,
        "cgpa": cgpa,

        "voter_id": voter_id,
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
# GET SINGLE REPORT
# =========================

@app.get("/report/{report_id}")
def get_single_report(
    report_id: str,
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

    report = reports_collection.find_one({

        "_id": ObjectId(report_id),

        "user_email": user_email
    })

    if not report:

        return {
            "message": "Report not found"
        }

    report["_id"] = str(report["_id"])

    return report

# =========================
# DOWNLOAD PDF REPORT
# =========================

@app.get("/download-report/{report_id}")
def download_report(report_id: str):

    pdf_file = f"reports/report_{report_id}.pdf"

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