from dotenv import load_dotenv

import os

# LOAD ENV
load_dotenv()

# SECURITY
SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM"
)

# DATABASE
MONGO_URI = os.getenv(
    "MONGO_URI"
)

# FRONTEND
FRONTEND_URL = os.getenv(
    "FRONTEND_URL"
)

# FILE LIMITS
MAX_FILE_SIZE = (
    10 * 1024 * 1024
)

# SUPPORTED FILE TYPES
ALLOWED_FILE_TYPES = [

    "application/pdf",

    "image/png",

    "image/jpeg",

    "image/jpg"
]