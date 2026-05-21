import re

# =========================
# FRAUD ANALYSIS ENGINE
# =========================

def analyze_document(

    extracted_text,

    metadata,

    document_category,

    pan_number,

    aadhaar_number,

    name,

    dob,

    invoice_number,

    total_amount,

    blur_score,

    quality_status
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
    # OCR QUALITY ANALYSIS
    # =========================

    text_length = len(
        extracted_text.strip()
    )

    word_count = len(
        extracted_text.split()
    )

    # VERY LOW TEXT

    if text_length < 50:

        risk_score += 25

        reasons.append(
            "Very low OCR text extracted"
        )

    # LOW WORD COUNT

    if word_count < 10:

        risk_score += 15

        reasons.append(
            "Low readable content detected"
        )

    # SUSPICIOUS OCR QUALITY

    if (

        text_length > 0

        and word_count > 0

        and text_length / word_count < 3
    ):

        risk_score += 10

        reasons.append(
            "Poor OCR readability detected"
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
    # EXTRACTION COMPLETENESS
    # =========================

    missing_fields = 0

    important_fields = [

        name,

        pan_number,

        aadhaar_number,

        dob
    ]

    for field in important_fields:

        if (

            field == "Not Found"

            or field == "Not Extracted"
        ):

            missing_fields += 1

    # TOO MANY MISSING FIELDS

    if missing_fields >= 3:

        risk_score += 20

        reasons.append(
            "Multiple important fields missing"
        )

    elif missing_fields >= 1:

        risk_score += 10

        reasons.append(
            "Some important fields missing"
        )

        # =========================
    # PAN FORMAT VALIDATION
    # =========================

    if document_category == "PAN Card":

        valid_pan = re.match(

            r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$",

            pan_number
        )

        if not valid_pan:

            risk_score += 25

            reasons.append(
                "Invalid PAN format detected"
            )

    # =========================
    # AADHAAR VALIDATION
    # =========================

    if document_category == "Aadhaar Card":

        valid_aadhaar = re.match(

            r"^\d{4}\s\d{4}\s\d{4}$",

            aadhaar_number
        )

        if not valid_aadhaar:

            risk_score += 25

            reasons.append(
                "Invalid Aadhaar format detected"
            )

    # =========================
    # SUSPICIOUS NAME CHECK
    # =========================

    suspicious_names = [

        "TEST",

        "SAMPLE",

        "DEMO",

        "UNKNOWN"
    ]

    for suspicious in suspicious_names:

        if suspicious in name.upper():

            risk_score += 15

            reasons.append(
                "Suspicious placeholder name detected"
            )

    # =========================
    # IMAGE QUALITY VALIDATION
    # =========================

    if quality_status == "Very Blurry":

        risk_score += 30

        reasons.append(
            "Very blurry image detected"
        )

    elif quality_status == "Blurry":

        risk_score += 15

        reasons.append(
            "Blurry image quality detected"
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