import cv2

# Replace with the correct device file path
device_path = '/dev/video2'
cap = cv2.VideoCapture(device_path)

if not cap.isOpened():
    print(f"Error: Could not open camera with device path {device_path}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Display the resulting frame
    cv2.imshow('External Camera Feed', frame)

    # Press 'q' on the keyboard to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
