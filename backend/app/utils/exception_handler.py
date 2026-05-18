from fastapi.responses import JSONResponse

from fastapi.requests import Request

# =========================
# GLOBAL EXCEPTION HANDLER
# =========================

async def global_exception_handler(

    request: Request,

    exc: Exception
):

    print("GLOBAL ERROR:", exc)

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": "Internal Server Error"
        }
    )