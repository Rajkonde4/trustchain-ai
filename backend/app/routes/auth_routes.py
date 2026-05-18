from fastapi import APIRouter

from app.utils.auth_utils import (

    hash_password,

    verify_password,

    create_access_token
)

from app.utils.response_handler import (

    success_response,

    error_response
)

from app.models.auth_models import (

    SignupRequest,

    LoginRequest
)

from app.models.response_models import (
    StandardResponse
)

router = APIRouter()

# =========================
# INJECTED COLLECTION
# =========================

users_collection = None

# =========================
# SIGNUP
# =========================

@router.post(
    "/signup",
    response_model=StandardResponse
)
def signup(data: SignupRequest):

    existing_user = users_collection.find_one({

        "email": data.email
    })

    # USER EXISTS
    if existing_user:

        return error_response(
            "User already exists"
        )

    # HASH PASSWORD
    hashed_password = hash_password(
        data.password
    )

    # USER DATA
    user_data = {

        "name": data["name"],

        "email": data["email"],

        "password": hashed_password
    }

    # SAVE USER
    users_collection.insert_one(
        user_data
    )

    return success_response(
        "Signup successful"
    )

# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=StandardResponse
)
def login(data: LoginRequest):

    user = users_collection.find_one({

        "email": data.email
    })

    # INVALID EMAIL
    if not user:

        return error_response(
            "Invalid Email"
        )

    # VERIFY PASSWORD
    valid_password = verify_password(

        data.password,

        user["password"]
    )

    # INVALID PASSWORD
    if not valid_password:

        return error_response(
            "Invalid Password"
        )

    # CREATE TOKEN
    token = create_access_token({

        "email": user["email"],

        "name": user["name"]
    })

    # SUCCESS RESPONSE
    return success_response(

        "Login successful",

        {

            "access_token": token,

            "user": {

                "id": str(user["_id"]),

                "name": user["name"],

                "email": user["email"]
            }
        }
    )