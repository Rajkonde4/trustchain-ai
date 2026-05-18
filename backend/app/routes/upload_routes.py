from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Header
)

from app.utils.auth_utils import (
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

from app.services.pdf_service import (
    generate_pdf_report
)

import hashlib

from bson import ObjectId

router = APIRouter()

# THESE WILL BE INJECTED
reports_collection = None

# =========================
# UPLOAD DOCUMENT
# =========================

@router.post("/upload")
async def upload_file(

    file: UploadFile = File(...),

    authorization: str = Header(None)
):

    # =========================
    # CHECK AUTH TOKEN
    # =========================

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

    # =========================
    # VALIDATE FILE TYPE
    # =========================

    if not validate_file_type(
        file.content_type
    ):

        return {
            "message": "Unsupported File Type"
        }

    contents = await file.read()

    # =========================
    # VALIDATE FILE SIZE
    # =========================

    if not validate_file_size(
        len(contents)
    ):

        return {
            "message": "File Too Large"
        }

    # =========================
    # OCR EXTRACTION
    # =========================

    if file.content_type == "application/pdf":

        extracted_text, metadata = (
            extract_text_from_pdf(contents)
        )

    else:

        extracted_text, metadata = (
            extract_text_from_image(contents)
        )

    # =========================
    # DOCUMENT HASH
    # =========================

    document_hash = hashlib.sha256(
        contents
    ).hexdigest()

    # =========================
    # BASIC ANALYSIS
    # =========================

    document_category = "Unknown Document"

    verification_status = "Verified"

    fraud_risk = "Low"

    confidence_score = 85

    # =========================
    # CREATE REPORT ID
    # =========================

    report_id = str(ObjectId())

    # =========================
    # VERIFICATION URL
    # =========================

    verification_url = (
        f"http://localhost:5173/verify/{report_id}"
    )

    # =========================
    # GENERATE PDF REPORT
    # =========================

    pdf_file = generate_pdf_report(

        report_id=report_id,

        file=file,

        document_category=document_category,

        verification_status=verification_status,

        fraud_risk=fraud_risk,

        confidence_score=confidence_score,

        document_hash=document_hash,

        name="Not Extracted",

        pan_number="Not Found",

        aadhaar_number="Not Found",

        dob="Not Found",

        gender="Not Found",

        invoice_number="Not Found",

        total_amount="Not Found",

        verification_url=verification_url
    )

    # =========================
    # STORE REPORT
    # =========================

    reports_collection.insert_one({

        "_id": ObjectId(report_id),

        "filename": file.filename,

        "document_category": document_category,

        "verification_status": verification_status,

        "fraud_risk": fraud_risk,

        "confidence_score": confidence_score,

        "document_hash": document_hash,

        "pdf_report": pdf_file
    })

    # =========================
    # RESPONSE
    # =========================

    return {

        "message": "Upload modular architecture working",

        "report_id": report_id,

        "document_hash": document_hash,

        "text_preview": extracted_text[:300]
    }