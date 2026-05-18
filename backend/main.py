from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

import pytesseract

from app.config.settings import (
    SECRET_KEY,
    ALGORITHM
)

from app.utils.exception_handler import (
    global_exception_handler
)

# =========================
# TESSERACT PATH
# =========================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="TrustChain AI Backend"
)

app.add_exception_handler(

    Exception,

    global_exception_handler
)

# =========================
# DATABASE
# =========================

from app.database.mongodb import (
    users_collection,
    reports_collection
)

# =========================
# ROUTES
# =========================

from app.routes import (
    auth_routes,
    upload_routes,
    report_routes
)

# =========================
# DEPENDENCY INJECTION
# =========================

auth_routes.users_collection = (
    users_collection
)

upload_routes.reports_collection = (
    reports_collection
)

report_routes.reports_collection = (
    reports_collection
)

# =========================
# REGISTER ROUTES
# =========================

app.include_router(
    auth_routes.router
)

app.include_router(
    upload_routes.router
)

app.include_router(
    report_routes.router
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "TrustChain AI Backend Running"
    }