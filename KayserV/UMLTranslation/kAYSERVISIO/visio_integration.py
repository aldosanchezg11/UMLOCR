import win32com.client
import pythoncom


def create_bpmn_in_visio(translated_text, all_detected_symbols, all_detected_marks, pools_lanes):
    """
    Creates a BPMN diagram in Visio based on detected symbols, marks, and pools/lanes,
    and incorporates translated text.

    Args:
        translated_text (str): The translated text to assign to shapes.
        all_detected_symbols (dict): Aggregated detected symbols with their absolute coordinates.
        all_detected_marks (dict): Aggregated detected marks with their absolute coordinates.
        pools_lanes (list): List of detected pools/lanes as rectangles with coordinates.
    """
    visio = None
    try:
        pythoncom.CoInitialize()
        visio = win32com.client.Dispatch("Visio.Application")
        doc = visio.Documents.Add("")
        page = visio.ActivePage

        scale_factor = 0.1  # Example scaling factor to convert image pixels to Visio units

        # Step 1: Draw Pools/Lanes first
        for pool_lane in pools_lanes:
            x, y, width, height = pool_lane
            visio_x = x * scale_factor
            visio_y = y * scale_factor
            visio_width = width * scale_factor
            visio_height = height * scale_factor
            pool_lane_shape = page.DrawRectangle(visio_x, visio_y, visio_x + visio_width, visio_y + visio_height)
            pool_lane_shape.Text = "Pool/Lane"

        # Step 2: Overlay smaller shapes on top of the pools/lanes
        for symbol_name, locations in all_detected_symbols.items():
            for (x, y) in locations:
                visio_x = x * scale_factor
                visio_y = y * scale_factor

                shape = None
                if symbol_name in ["eventoI", "eventoP", "eventoF"]:
                    shape = page.DrawOval(visio_x, visio_y, visio_x + 1, visio_y + 1)
                elif symbol_name in ["decisionx", "decisionm"]:
                    shape = page.DrawRectangle(visio_x, visio_y, visio_x + 2, visio_y + 2)
                elif symbol_name == "proceso":
                    shape = page.DrawRectangle(visio_x, visio_y, visio_x + 3, visio_y + 1.5)
                elif symbol_name == "conector":
                    shape = page.DrawLine(visio_x, visio_y, visio_x + 2, visio_y)

                if shape:
                    shape.Text = translated_text

        # Step 3: Add detected marks
        for mark_name, locations in all_detected_marks.items():
            for (x, y) in locations:
                visio_x = x * scale_factor
                visio_y = y * scale_factor

                mark_shape = None
                if mark_name == "marca de subsección":
                    mark_shape = page.DrawOval(visio_x, visio_y, visio_x + 0.5, visio_y + 0.5)
                elif mark_name == "mensaje":
                    mark_shape = page.DrawRectangle(visio_x, visio_y, visio_x + 1, visio_y + 0.5)
                elif mark_name == "usuario":
                    mark_shape = page.DrawOval(visio_x, visio_y, visio_x + 0.5, visio_y + 0.5)
                elif mark_name == "documento":
                    mark_shape = page.DrawRectangle(visio_x, visio_y, visio_x + 1, visio_y + 1)

                if mark_shape:
                    mark_shape.Text = f"Mark: {mark_name}"
                    # Optional: Add interactive functionality here

        # Save final diagram
        visio_path = 'diagrama_traducido.vsdx'
        doc.SaveAs(visio_path)
        print(f"Diagrama guardado como: {visio_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if visio:
            visio.Quit()
        pythoncom.CoUninitialize()
