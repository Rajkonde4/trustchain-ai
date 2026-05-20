# =========================
# FRAUD ANALYSIS ENGINE
# =========================

def analyze_document(

    extracted_text,

    metadata,

    document_category,

    pan_number,

    aadhaar_number,

    name
):

    risk_score = 0

    reasons = []

    # =========================
    # UNKNOWN DOCUMENT
    # =========================

    if document_category == "Unknown Document":

        risk_score += 30

        reasons.append(
            "Document type could not be identified"
        )

    # =========================
    # VERY LOW OCR TEXT
    # =========================

    if len(extracted_text) < 50:

        risk_score += 25

        reasons.append(
            "Very low OCR text extracted"
        )

    # =========================
    # MISSING NAME
    # =========================

    if name == "Not Extracted":

        risk_score += 10

        reasons.append(
            "Name could not be extracted"
        )

    # =========================
    # PAN VALIDATION
    # =========================

    if (

        document_category == "PAN Card"

        and pan_number == "Not Found"
    ):

        risk_score += 25

        reasons.append(
            "PAN number missing"
        )

    # =========================
    # AADHAAR VALIDATION
    # =========================

    if (

        document_category == "Aadhaar Card"

        and aadhaar_number == "Not Found"
    ):

        risk_score += 25

        reasons.append(
            "Aadhaar number missing"
        )

    # =========================
    # METADATA ANALYSIS
    # =========================

    suspicious_tools = [

        "photoshop",

        "canva",

        "illustrator"
    ]

    metadata_string = str(metadata).lower()

    for tool in suspicious_tools:

        if tool in metadata_string:

            risk_score += 20

            reasons.append(
                f"Suspicious editing tool detected: {tool}"
            )

    # =========================
    # FINAL FRAUD RISK
    # =========================

    if risk_score >= 60:

        fraud_risk = "High"

        verification_status = "Suspicious"

    elif risk_score >= 30:

        fraud_risk = "Medium"

        verification_status = "Needs Review"

    else:

        fraud_risk = "Low"

        verification_status = "Verified"

    confidence_score = max(
        100 - risk_score,
        5
    )

    return {

        "fraud_risk": fraud_risk,

        "verification_status": verification_status,

        "confidence_score": confidence_score,

        "risk_score": risk_score,

        "reasons": reasons
    }