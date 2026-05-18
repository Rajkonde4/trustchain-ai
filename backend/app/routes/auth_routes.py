from fastapi import APIRouter

from app.utils.auth_utils import (
    hash_password,
    verify_password,
    create_access_token
)

from bson import ObjectId

router = APIRouter()

# THESE WILL BE INJECTED
users_collection = None

# =========================
# SIGNUP
# =========================

@router.post("/signup")
def signup(data: dict):

    existing_user = users_collection.find_one({

        "email": data["email"]
    })

    if existing_user:

        return {
            "message": "User already exists"
        }

    hashed_password = hash_password(
        data["password"]
    )

    user_data = {

        "name": data["name"],

        "email": data["email"],

        "password": hashed_password
    }

    users_collection.insert_one(
        user_data
    )

    return {
        "message": "Signup successful"
    }

# =========================
# LOGIN
# =========================

@router.post("/login")
def login(data: dict):

    user = users_collection.find_one({

        "email": data["email"]
    })

    if not user:

        return {
            "message": "Invalid Email"
        }

    valid_password = verify_password(

        data["password"],

        user["password"]
    )

    if not valid_password:

        return {
            "message": "Invalid Password"
        }

    token = create_access_token({

        "email": user["email"],

        "name": user["name"]
    })

    return {

        "message": "Login successful",

        "token": token,

        "user": {

            "id": str(user["_id"]),

            "name": user["name"],

            "email": user["email"]
        }
    }