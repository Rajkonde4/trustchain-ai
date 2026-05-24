import cv2
import numpy as np

# =========================
# BLUR DETECTION
# =========================

def detect_blur(image_bytes):

    # CONVERT IMAGE BYTES
    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    # INVALID IMAGE
    if image is None:

        return {

            "blur_score": 0,

            "is_blurry": True,

            "reason": "Image could not be processed"
        }

    # CONVERT TO GRAYSCALE
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # LAPLACIAN VARIANCE
    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    # THRESHOLD
    is_blurry = blur_score < 100

    reason = (

        "Image appears blurry"

        if is_blurry

        else "Image quality acceptable"
    )

    return {

        "blur_score": round(
            blur_score,
            2
        ),

        "is_blurry": is_blurry,

        "reason": reason
    }

# =========================
# DOCUMENT CONTOUR DETECTION
# =========================

def detect_document_contour(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "document_detected": False,

            "reason": "Invalid image"
        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edged = cv2.Canny(
        blurred,
        75,
        200
    )

    contours, _ = cv2.findContours(

        edged.copy(),

        cv2.RETR_LIST,

        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(

        contours,

        key=cv2.contourArea,

        reverse=True
    )[:5]

    for contour in contours:

        perimeter = cv2.arcLength(
            contour,
            True
        )

        approx = cv2.approxPolyDP(

            contour,

            0.02 * perimeter,

            True
        )

        # DOCUMENT-like rectangle

        if len(approx) == 4:

            return {

                "document_detected": True,

                "reason": "Document boundary detected"
            }

    return {

        "document_detected": False,

        "reason": "No document boundary detected"
    }

# =========================
# SCREENSHOT DETECTION
# =========================

def detect_screenshot(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "is_screenshot": False,

            "reason": "Invalid image"
        }

    height, width = image.shape[:2]

    # COMMON MOBILE SCREENSHOT RATIOS

    mobile_ratios = [

        19.5 / 9,

        20 / 9,

        16 / 9
    ]

    aspect_ratio = max(
        width,
        height
    ) / min(
        width,
        height
    )

    for ratio in mobile_ratios:

        if abs(aspect_ratio - ratio) < 0.15:

            return {

                "is_screenshot": True,

                "reason": "Possible mobile screenshot detected"
            }

    return {

        "is_screenshot": False,

        "reason": "No screenshot patterns detected"
    }

# =========================
# BRIGHTNESS ANALYSIS
# =========================

def analyze_brightness(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "brightness_score": 0,

            "is_dark": True,

            "reason": "Invalid image"
        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    brightness_score = gray.mean()

    is_dark = brightness_score < 60

    reason = (

        "Image brightness too low"

        if is_dark

        else "Brightness acceptable"
    )

    return {

        "brightness_score": round(
            brightness_score,
            2
        ),

        "is_dark": is_dark,

        "reason": reason
    }

# =========================
# EDGE DENSITY ANALYSIS
# =========================

def analyze_edge_density(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "edge_score": 0,

            "low_edges": True,

            "reason": "Invalid image"
        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_score = np.mean(edges)

    low_edges = edge_score < 8

    reason = (

        "Very low document edge density"

        if low_edges

        else "Document edge density acceptable"
    )

    return {

        "edge_score": round(
            float(edge_score),
            2
        ),

        "low_edges": low_edges,

        "reason": reason
    }

# =========================
# TEXT REGION ANALYSIS
# =========================

def detect_text_regions(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "text_regions_detected": False,

            "reason": "Invalid image"
        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    thresh = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        11,

        2
    )

    contours, _ = cv2.findContours(

        thresh,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE
    )

    text_like_regions = 0

    for contour in contours:

        x, y, w, h = cv2.boundingRect(
            contour
        )

        # TEXT-LIKE BLOCKS

        if (

            w > 20

            and h > 8

            and w > h
        ):

            text_like_regions += 1

    detected = text_like_regions > 15

    reason = (

        "Structured text regions detected"

        if detected

        else "Very few text regions detected"
    )

    return {

        "text_regions_detected": detected,

        "region_count": text_like_regions,

        "reason": reason
    }

# =========================
# SUSPICIOUS CROP DETECTION
# =========================

def detect_suspicious_crop(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {

            "suspicious_crop": True,

            "reason": "Invalid image"
        }

    height, width = image.shape[:2]

    aspect_ratio = width / height

    suspicious = False

    # EXTREME CROPPING

    if (

        aspect_ratio > 3

        or aspect_ratio < 0.3
    ):

        suspicious = True

    # VERY SMALL IMAGE

    if (

        width < 250

        or height < 250
    ):

        suspicious = True

    reason = (

        "Suspicious crop dimensions detected"

        if suspicious

        else "Crop dimensions acceptable"
    )

    return {

        "suspicious_crop": suspicious,

        "reason": reason
    }