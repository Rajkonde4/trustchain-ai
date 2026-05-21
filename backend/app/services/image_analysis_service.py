import cv2
import numpy as np

# =========================
# IMAGE QUALITY ANALYSIS
# =========================

def analyze_image_quality(image_bytes):

    # CONVERT BYTES TO NUMPY ARRAY
    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    # DECODE IMAGE
    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "blur_score": 0,

            "quality_status": "Invalid Image"
        }

    # CONVERT TO GRAYSCALE
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # BLUR DETECTION
    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    # QUALITY STATUS
    if blur_score < 30:

        quality_status = "Very Blurry"

    elif blur_score < 80:

        quality_status = "Blurry"

    else:

        quality_status = "Clear"

    return {

        "blur_score": round(
            blur_score,
            2
        ),

        "quality_status": quality_status
    }