import cv2
import numpy as np
import pytesseract
from templates import templates, mark_templates


def detect_symbol(image, template, threshold=0.7):
    """Detects symbols or marks in the given image using template matching."""
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    # Return list of (x, y) coordinates
    return list(zip(*loc[::-1]))  # (x, y) tuples


def detect_pools_lanes(image, min_area=1000):
    """
    Detects large rectangular areas in the image that likely correspond to pools and lanes.

    Args:
        image (numpy.ndarray): The input image in which to detect pools and lanes.
        min_area (int): Minimum area threshold to filter out small rectangles.

    Returns:
        List of tuples: Each tuple contains the coordinates of the top-left corner,
                        width, and height of the detected pool/lane.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []
    for contour in contours:
        # Approximate the contour to a rectangle
        x, y, w, h = cv2.boundingRect(contour)
        if w * h >= min_area:
            rectangles.append((x, y, w, h))

    return rectangles


def segment_image_with_coordinates(image_path, rows=2, cols=2):
    """
    Segments the image into a grid and returns a list of segments along with their top-left coordinates.

    Args:
        image_path (str): Path to the input image.
        rows (int): Number of rows to divide the image into.
        cols (int): Number of columns to divide the image into.

    Returns:
        List of tuples: Each tuple contains the segmented image and its top-left (x_offset, y_offset) coordinates.
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    segment_height = height // rows
    segment_width = width // cols

    segments = []
    for i in range(rows):
        for j in range(cols):
            y_start = i * segment_height
            y_end = (i + 1) * segment_height if i != rows - 1 else height
            x_start = j * segment_width
            x_end = (j + 1) * segment_width if j != cols - 1 else width

            segment = image[y_start:y_end, x_start:x_end]
            segments.append((segment, x_start, y_start))

    return segments


def extract_text_and_marks_from_segment(segment_image):
    """
    Extracts text, detected symbols, and marks from a given image segment.

    Args:
        segment_image (numpy.ndarray): The image segment to process.

    Returns:
        Tuple: Extracted text (str), detected_symbols (dict), detected_marks (dict)
    """
    gray = cv2.cvtColor(segment_image, cv2.COLOR_BGR2GRAY)

    detected_symbols = {}
    detected_marks = {}

    for symbol_name, template in templates.items():
        locations = detect_symbol(gray, template)
        if locations:
            detected_symbols[symbol_name] = locations

    for mark_name, template in mark_templates.items():
        locations = detect_symbol(gray, template)
        if locations:
            detected_marks[mark_name] = locations

    # Extract text using OCR
    text = pytesseract.image_to_string(segment_image)
    return text, detected_symbols, detected_marks
