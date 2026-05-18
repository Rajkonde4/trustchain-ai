from pydantic import BaseModel

# =========================
# SIGNUP MODEL
# =========================

class SignupRequest(BaseModel):

    name: str

    email: str

    password: str

# =========================
# LOGIN MODEL
# =========================

class LoginRequest(BaseModel):

    email: str

    password: str