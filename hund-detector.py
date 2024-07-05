import cv2
import numpy as np

# Load a pre-trained hand detection model if available, or use contour/color detection

# Initialize video capture
cap = cv2.VideoCapture(0)  # Adjust the index if you have multiple cameras

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours to find the hand region
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:  # Adjust this area threshold as per your need
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
    
    # Display the frame
    cv2.imshow('Hand Detection', frame)
    
    # Exit on 'q' keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy any OpenCV windows
cap.release()
cv2.destroyAllWindows()
