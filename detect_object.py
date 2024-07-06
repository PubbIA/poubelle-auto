import serial
import cv2
import requests
from dotenv import load_dotenv
import os
import uuid
import time
from predict import predict_class
from collections import Counter
load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "5000")
DEVICE_PATH = os.getenv("DEVICE_PATH", "/dev/video3")

BASE_URL = f"http://{HOST}:{PORT}/api"

# Define the serial port (change this to your specific port)
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")  # Linux example, for Windows use something like 'COM3'
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# Function to send a number to Arduino
def send_number_to_arduino(message):
    command = f"{message}\n"  # Append newline character to the command
    print(f"Sending command: {command.strip()}")
    ser.write(command.encode())  # Encode the command as bytes and send it
    time.sleep(1)  # Wait for Arduino to process the command

    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()  # Read the response from Arduino
        print(f"Arduino response: {response}")

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
i:int=0
predicts=[]
# Mapping class indices to class labels
class_indices = {'cardboard': 0, 'glass': 1, 'metal': 2, 'paper': 3, 'plastic': 4, 'trash': 5}
class_labels = {v: k for k, v in class_indices.items()}
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the frame with rectangles
    cv2.imshow('Camera Feed', frame)

    # Path to the image file you want to upload
    image_path = f"data/garbage/image.jpg"
    cv2.imwrite(image_path, frame)

    # Open the image file in binary mode
    class_predicted = predict_class(image_path)
    predicts.append(class_labels[class_predicted])
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
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    i+=1
    if i==100:
        break
counter=Counter(predicts)
# Get the first element and print it
first_element = counter.most_common(1)[0]
print(first_element)

if first_element[0] == "plastic":
    print("Plastic")
    send_number_to_arduino(1)
elif first_element[0] == "metal":
    print("Metal")
    send_number_to_arduino(2)
elif first_element[0] == "paper":
    print("Paper")
    send_number_to_arduino(3)
elif first_element[0] == "cardboard":
    print("Cardboard")
    send_number_to_arduino(3)
elif first_element[0] == "glass":
    print("Glass")
    send_number_to_arduino(1)
elif first_element[0] == "trash":
    print("TRash")
    send_number_to_arduino(3)

requests.put(f"{BASE_URL}/cashback/add",data={"points":10,"user_id":"4c3a8052-ec8b-4dfc-8e58-cab08cd41bc4"})

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
