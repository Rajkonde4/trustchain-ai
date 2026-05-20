# =========================
# DOCUMENT CLASSIFIER
# =========================

def classify_document(text):

    text = text.upper()

    # =========================
    # PAN CARD
    # =========================

    if (

        "INCOME TAX DEPARTMENT" in text

        or "PERMANENT ACCOUNT NUMBER" in text
    ):

        return "PAN Card"

    # =========================
    # AADHAAR
    # =========================

    elif (

        "GOVERNMENT OF INDIA" in text

        or "AADHAAR" in text
    ):

        return "Aadhaar Card"

    # =========================
    # PASSPORT
    # =========================

    elif (

        "PASSPORT" in text

        or "REPUBLIC OF INDIA" in text
    ):

        return "Passport"

    # =========================
    # INVOICE
    # =========================

    elif (

        "INVOICE" in text

        or "BILL TO" in text

        or "TOTAL AMOUNT" in text
    ):

        return "Invoice"

    # =========================
    # RESUME
    # =========================

    elif (

        "EDUCATION" in text

        and "SKILLS" in text
    ):

        return "Resume"

    # =========================
    # DRIVING LICENSE
    # =========================

    elif (

        "DRIVING LICENCE" in text

        or "DL NO" in text
    ):

        return "Driving License"

    # =========================
    # UNKNOWN
    # =========================

    return "Unknown Document"