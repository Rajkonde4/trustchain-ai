# =========================
# ALLOWED FILE TYPES
# =========================

ALLOWED_FILE_TYPES = [

    "application/pdf",

    "image/png",

    "image/jpeg",

    "image/jpg"
]

# =========================
# MAX FILE SIZE
# =========================

MAX_FILE_SIZE = 10 * 1024 * 1024

# =========================
# VALIDATE FILE TYPE
# =========================

def validate_file_type(content_type):

    return content_type in ALLOWED_FILE_TYPES

# =========================
# VALIDATE FILE SIZE
# =========================

def validate_file_size(file_size):

    return file_size <= MAX_FILE_SIZE