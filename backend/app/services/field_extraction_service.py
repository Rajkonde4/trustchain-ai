import re

# =========================
# EXTRACT PAN NUMBER
# =========================

def extract_pan_number(text):

    pattern = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"

    match = re.search(
        pattern,
        text
    )

    return match.group() if match else "Not Found"

# =========================
# EXTRACT AADHAAR NUMBER
# =========================

def extract_aadhaar_number(text):

    pattern = r"\d{4}\s\d{4}\s\d{4}"

    match = re.search(
        pattern,
        text
    )

    return match.group() if match else "Not Found"

# =========================
# EXTRACT DOB
# =========================

def extract_dob(text):

    pattern = r"\d{2}/\d{2}/\d{4}"

    match = re.search(
        pattern,
        text
    )

    return match.group() if match else "Not Found"

# =========================
# EXTRACT INVOICE NUMBER
# =========================

def extract_invoice_number(text):

    patterns = [

        r"Invoice\s*No[:\-]?\s*([A-Z0-9\-]+)",

        r"Invoice\s*#[:\-]?\s*([A-Z0-9\-]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return "Not Found"

# =========================
# EXTRACT TOTAL AMOUNT
# =========================

def extract_total_amount(text):

    patterns = [

        r"Total\s*Amount[:\-]?\s*₹?\s*([0-9,]+)",

        r"Amount\s*Due[:\-]?\s*₹?\s*([0-9,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return "Not Found"

# =========================
# EXTRACT NAME
# =========================

def extract_name(text):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if (

            len(line.split()) >= 2

            and line.isupper()

            and len(line) < 40
        ):

            return line

    return "Not Extracted"