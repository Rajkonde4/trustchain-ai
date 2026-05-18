from pydantic import BaseModel

from typing import Optional

from typing import Any

# =========================
# STANDARD RESPONSE
# =========================

class StandardResponse(BaseModel):

    success: bool

    message: str

    data: Optional[Any] = None