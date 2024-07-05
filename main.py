import cv2
import requests
from dotenv import load_dotenv
import os
import uuid
import time

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "5000")
DEVICE_PATH = os.getenv("DEVICE_PATH", "/dev/video3")

BASE_URL = f"http://{HOST}:{PORT}/api"
print(requests.get(BASE_URL + "/docs"))

# Define the serial port (change this to your specific port)
# SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")  # Linux example, for Windows use something like 'COM3'
# ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# Function to send a number to Arduino
# def send_number_to_arduino(number):
#     ser.write(str(number).encode())  # Convert number to bytes and send it
#     time.sleep(1)  # Optional delay to let Arduino process the number

# Load the Haar Cascades for face, eye, and mouth detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

# Check if the cascades were loaded correctly
if face_cascade.empty():
    raise IOError('Could not load face cascade classifier')
if eye_cascade.empty():
    raise IOError('Could not load eye cascade classifier')
if mouth_cascade.empty():
    raise IOError('Could not load mouth cascade classifier')

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream or file")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check for eyes and mouth in the detected face region
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)
        # Detect mouth
        mouth = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=11, minSize=(30, 30))
        for (mx, my, mw, mh) in mouth:
            my = int(my - 0.15 * mh)  # Adjust mouth position to be more accurate

        # Check if both eyes and mouth are detected
        if len(eyes) >= 2 and len(mouth) > 0:
            # Save just the face area
            face_image = frame[y:y + h, x:x + w]
            # Path to the image file you want to upload
            image_path = f"data/users/{str(uuid.uuid4())}.jpg"
            cv2.imwrite(image_path, face_image)

            # USER RECOGNITION

            # Open the image file in binary mode
            with open(image_path, "rb") as image_file:
                # Define the files parameter to be sent in the request
                files = {"image": image_file}
                # Send a POST request to the API endpoint with the image file
                response = requests.post(f"{BASE_URL}/ai/face-recognition", files=files)

            # Check if the request was successful
            if response.status_code == 200:
                # Assuming response.json() returns a JSON object with a "user_id" key
                user_id = response.json().get("user_id", "")
                if user_id:
                    # Print the response from the API
                    response1 = requests.get(f"{BASE_URL}/users/{user_id}")
                    print(response1.json())
                    # send_number_to_arduino(1)
                    # voice with the name of the user
                else:
                    print("No user found")
                    # send_number_to_arduino(2)
                    # voice with Hello, I'm Boundif

            else:
                # Print the error message if the request was not successful
                print(f"Error: {response.status_code}")
                print(response.text)

            break

    # Object detection logic
    time.sleep(1)
    # Path to the image file you want to upload
    image_path = f"data/garbage/{str(uuid.uuid4())}.jpg"
    cv2.imwrite(image_path, frame)

    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Define the files parameter to be sent in the request
        files = {"image": image_file}

        # Send a POST request to the API endpoint with the image file
        response = requests.post(f"{BASE_URL}/ai/image-of-persone", files=files)
        # Check if the request was successful
        if response.status_code == 200:
            valid_image = response.json().get("valid_image", False)
            if not valid_image:
                response = requests.post(f"{BASE_URL}/ai/garbage-classifier", files=files)
                # Check if the request was successful
                if response.status_code == 200:
                    # paper , plastic , metal
                    class_predicted = response.json().get("class")

                    if class_predicted:
                        # Print the response from the API
                        if class_predicted == "plastic":
                            print("Plastic")
                            # send_number_to_arduino(1)
                        elif class_predicted == "metal":
                            print("Metal")
                            # send_number_to_arduino(2)
                        elif class_predicted == "paper":
                            print("Paper")
                            # send_number_to_arduino(3)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Press 'q' to quit the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()
# Close the serial connection
# ser.close()
