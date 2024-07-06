import cv2
import requests
from dotenv import load_dotenv
import os
import time
from gtts import gTTS
from playsound import playsound
import serial

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
# def send_number_to_arduino(message):
#     command = f"{message}\n"  # Append newline character to the command
#     print(f"Sending command: {command.strip()}")
#     ser.write(command.encode())  # Encode the command as bytes and send it
#     time.sleep(1)  # Wait for Arduino to process the command

#     while ser.in_waiting > 0:
#         response = ser.readline().decode().strip()  # Read the response from Arduino
#         print(f"Arduino response: {response}")

def lire_texte_en_francais(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("texte.mp3")
    playsound("texte.mp3")

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

# Variable to count consecutive successful face detections
consecutive_detection_count = 0

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
        
        # Check if both eyes and mouth are detected
        if len(eyes) >= 2 and len(mouth) > 0:
            consecutive_detection_count += 1

            # Save just the face area
            face_image = frame[y:y + h, x:x + w]
            # Path to the image file you want to upload
            image_path = f"data/users/ouail.jpg"
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
                    print("Salut")
                    print(response1.json())
                    # If 10 consecutive detections, read the text
                    username = response1.json()["username"]
                    if consecutive_detection_count >= 10:
                        texte = f"Salut {username}, je suis votre poubelle intelligente Boundif"
                        lire_texte_en_francais(texte)
                        # send_number_to_arduino(1)  # Send command to Arduino
                        consecutive_detection_count = 0  # Reset count after reading text
                    else:
                        texte = f"Salut {username}, je suis votre poubelle intelligente Boundif"
                        # voice with the name of the user
                else:
                    print("No user found")
                    # If 10 consecutive detections, read the text
                    if consecutive_detection_count >= 10:
                        texte = "Salut, je ne vous connais pas, je suis votre poubelle intelligente Boundif, essayez de télécharger l'application pour vous inscrire et gagner des points."
                        lire_texte_en_francais(texte)
                        # send_number_to_arduino(2)  # Send command to Arduino
                        consecutive_detection_count = 0  # Reset count after reading text
                    else:
                        # send_number_to_arduino(2)  # Send command to Arduino
                        texte = "Salut, je ne vous connais pas, je suis votre poubelle intelligente Boundif, essayez de télécharger l'application pour vous inscrire et gagner des points."
                        # voice with Hello, I'm Boundif

            else:
                # Print the error message if the request was not successful
                print(f"Error: {response.status_code}")
                print(response.text)

        break
    
    if faces is None or len(faces) == 0:
        print("No face detected")
        # If 10 consecutive detections, read the text
        if consecutive_detection_count >= 10:
            texte = "Approchez vous de la poubelle pour un littoral propre"
            lire_texte_en_francais(texte)
        # send_number_to_arduino(3)  # Send command to Arduino
        # voice with No face detected
        consecutive_detection_count = 0  # Reset count when no face is detected

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
