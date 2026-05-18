from fastapi import (
    APIRouter,
    Header
)

from fastapi.responses import (
    FileResponse
)

from bson import ObjectId

from app.utils.auth_utils import (
    verify_token
)

router = APIRouter()

# INJECTED COLLECTION
reports_collection = None

# =========================
# GET SINGLE REPORT
# =========================

@router.get("/report/{report_id}")
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
# GET ALL REPORTS
# =========================

@router.get("/reports")
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

@router.get("/download-report/{report_id}")
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

@router.get("/verify/{report_id}")
def verify_document(report_id: str):

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