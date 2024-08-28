from image_processing import segment_image_with_coordinates, extract_text_and_marks_from_segment, detect_pools_lanes
from translation import translate_text
from visio_integration import create_bpmn_in_visio
import cv2

def main():
    image_path = 'my_image_path.jpg'  # Replace with your actual image path

    # Load the full image for processing
    image = cv2.imread(image_path)

    # Step 1: Detect pools/lanes (big rectangles)
    pools_lanes = detect_pools_lanes(image)
    print(f"Detected {len(pools_lanes)} pools/lanes.")

    # Step 2: Segment the image for smaller shapes
    segments = segment_image_with_coordinates(image_path, rows=2, cols=2)  # Adjust rows and cols as needed

    aggregated_text = ""
    all_detected_symbols = {}
    all_detected_marks = {}

    # Step 3: Process each segment
    for idx, (segment, x_offset, y_offset) in enumerate(segments):
        print(f"Processing segment {idx + 1}/{len(segments)} at offset ({x_offset}, {y_offset})")
        text, detected_symbols, detected_marks = extract_text_and_marks_from_segment(segment)

        # Aggregate text
        aggregated_text += "\n" + text

        # Adjust and aggregate detected symbols
        for symbol, locations in detected_symbols.items():
            adjusted_locations = [(x + x_offset, y + y_offset) for (x, y) in locations]
            if symbol in all_detected_symbols:
                all_detected_symbols[symbol].extend(adjusted_locations)
            else:
                all_detected_symbols[symbol] = adjusted_locations

        # Adjust and aggregate detected marks
        for mark, locations in detected_marks.items():
            adjusted_locations = [(x + x_offset, y + y_offset) for (x, y) in locations]
            if mark in all_detected_marks:
                all_detected_marks[mark].extend(adjusted_locations)
            else:
                all_detected_marks[mark] = adjusted_locations

    print("Aggregated Text:")
    print(aggregated_text)

    # Step 4: Translate the aggregated text
    translated_text = translate_text(aggregated_text)
    print("Translated Text:")
    print(translated_text)

    # Step 5: Create BPMN diagram in Visio with the aggregated data, including pools/lanes
    create_bpmn_in_visio(translated_text, all_detected_symbols, all_detected_marks, pools_lanes)

if __name__ == "__main__":
    main()

