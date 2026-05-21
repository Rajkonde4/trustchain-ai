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

from app.services.field_extraction_service import (

    extract_name,

    extract_pan_number,

    extract_aadhaar_number,

    extract_dob,

    extract_invoice_number,

    extract_total_amount
)

from app.services.document_classifier_service import (
    classify_document
)

from app.services.fraud_detection_service import (
    analyze_document
)

from app.services.image_analysis_service import (
    analyze_image_quality
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
    # IMAGE QUALITY ANALYSIS
    # =========================

    image_analysis = analyze_image_quality(
        contents
    )

    blur_score = image_analysis["blur_score"]

    quality_status = image_analysis["quality_status"]

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
    # FIELD EXTRACTION
    # =========================

    name = extract_name(
        extracted_text
    )

    pan_number = extract_pan_number(
        extracted_text
    )

    aadhaar_number = extract_aadhaar_number(
        extracted_text
    )

    dob = extract_dob(
        extracted_text
    )

    invoice_number = extract_invoice_number(
        extracted_text
    )

    total_amount = extract_total_amount(
        extracted_text
    )

    # =========================
    # DOCUMENT CLASSIFICATION
    # =========================

    document_category = classify_document(
        extracted_text
    )

    # =========================
    # FRAUD ANALYSIS
    # =========================

    analysis = analyze_document(

        extracted_text=extracted_text,

        metadata=metadata,

        document_category=document_category,

        pan_number=pan_number,

        aadhaar_number=aadhaar_number,

        name=name,

        dob=dob,

        invoice_number=invoice_number,

        total_amount=total_amount,

        blur_score=blur_score,

        quality_status=quality_status,
    )

    fraud_risk = analysis["fraud_risk"]

    verification_status = analysis["verification_status"]

    confidence_score = analysis["confidence_score"]

    fraud_reasons = analysis["reasons"]

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

        name=name,

        pan_number=pan_number,

        aadhaar_number=aadhaar_number,

        dob=dob,

        gender="Not Found",

        invoice_number=invoice_number,

        total_amount=total_amount,

        verification_url=verification_url,

        fraud_reasons=fraud_reasons
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

        "user_email": user_email,

        "name": name,

        "pan_number": pan_number,

        "aadhaar_number": aadhaar_number,

        "dob": dob,

        "invoice_number": invoice_number,

        "total_amount": total_amount,

        "fraud_reasons": fraud_reasons,
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