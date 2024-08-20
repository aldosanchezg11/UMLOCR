import pytesseract
import cv2
import deepl
import win32com.client
# from PIL import Image
import pythoncom


# Step 1: Detect text from image using OCR
def extract_text(image_path):
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    return text


# Step 2: Detect shapes from image
def detect_shapes(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if len(approx) == 3:
            shapes.append("Triangle")
        elif len(approx) == 4:
            shapes.append("Rectangle/Square")
        elif len(approx) > 4:
            shapes.append("Circle/Ellipse")
        # Additional shapes will be added here

    return shapes


# Step 3: Translate text using Deepl API
def translate_text(text, target_lang='ES'):
    auth_key = 'DEEPL_API_KEY'
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text


# Step 4: Create UML Diagram in Visio based on detected shapes
def create_uml_in_visio(translated_text, shapes):
    visio = None
    try:
        pythoncom.CoInitialize()  # Initialize COM libraries

        # Create a Visio application instance
        visio = win32com.client.Dispatch("Visio.Application")
        doc = visio.Documents.Add("")  # Create a new Visio document
        page = visio.ActivePage

        for shape_info in shapes:
            shape = None  # Initialize shape variable

            if shape_info == "Rectangle/Square":
                shape = page.DrawRectangle(1, 1, 3, 3)
            elif shape_info == "Circle/Ellipse":
                shape = page.DrawOval(1, 1, 3, 3)
            # Add other shapes as needed

            if shape:
                shape.Text = translated_text  # Assign the translated text to the shape

        # Save the document
        visio_path = 'translated_uml.vsdx'
        doc.SaveAs(visio_path)
        print(f"Visio file saved as: {visio_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure Visio application is properly closed
        visio.Quit()
        pythoncom.CoUninitialize()


###############################################################################
# Main workflow

image_path = 'my_image_path.jpg'

# Step 1: Extract text from image
original_text = extract_text(image_path)
print(f"Original text: {original_text}")

# Step 2: Detect shapes in the image
shapes_detected = detect_shapes(image_path)
print(f"Detected shapes: {shapes_detected}")

# Step 3: Translate the extracted text
translated_text = translate_text(original_text)
print(f"Translated Text: {translated_text}")

# Step 4: Create UML diagram in Visio
create_uml_in_visio(translated_text, shapes_detected)
