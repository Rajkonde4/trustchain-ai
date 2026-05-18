# =========================
# FRAUD ANALYSIS
# =========================

def analyze_document_risk(

    extracted_text,

    metadata,

    document_category,

    pan_number,

    aadhaar_number,

    invoice_number,

    total_amount,

    name,

    dob
):

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

    return {

        "confidence_score": confidence_score,

        "fraud_risk": fraud_risk
    }