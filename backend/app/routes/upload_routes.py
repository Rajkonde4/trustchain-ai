from app.utils.response_handler import (

    success_response,

    error_response
)


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Header
)

from bson import ObjectId

import hashlib

from app.config.settings import (
    FRONTEND_URL
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

router = APIRouter()

# =========================
# INJECTED COLLECTION
# =========================

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

      return error_response(
    "Unauthorized"
)

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    if not payload:

        return error_response(
    "Invalid Token"
)

    user_email = payload.get("email")

    # =========================
    # VALIDATE FILE TYPE
    # =========================

    if not validate_file_type(
        file.content_type
    ):

        return error_response(
    "Unsupported File Type"
)

    # =========================
    # READ FILE
    # =========================

    contents = await file.read()

    # =========================
    # VALIDATE FILE SIZE
    # =========================

    if not validate_file_size(
        len(contents)
    ):

        return error_response(
    "File Too Large"
)

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

    report_id = str(
        ObjectId()
    )

    # =========================
    # VERIFICATION URL
    # =========================

    verification_url = (
        f"{FRONTEND_URL}/verify/{report_id}"
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

        "pdf_report": pdf_file,

        "extracted_text": extracted_text,

        "metadata": metadata,

        "verification_url": verification_url,

        "user_email": user_email
    })

    # =========================
    # RESPONSE
    # =========================

    return success_response(

        "Upload successful",

        {

            "report_id": report_id,

            "document_hash": document_hash,

            "text_preview": extracted_text[:300]
        }
    )