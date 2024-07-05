import cv2

# List all available video capture devices
def list_camera_devices():
    index = 0
    while True:
        capture = cv2.VideoCapture(index)
        if capture.isOpened():
            print(f"Device {index}: {capture.get(cv2.CAP_PROP_FRAME_WIDTH)}x{capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
            capture.release()
        else:
            break
        index += 1

# Call the function to list available devices
list_camera_devices()
