import pythoncom
def com_task():
    # Initialize the COM library for the current thread
    pythoncom.CoInitialize()

    try:
        # Perform your COM-related tasks here
        # For example, interacting with a COM object
        print("Performing COM tasks...")

    finally:
        # Uninitialize the COM library for the current thread
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    com_task()