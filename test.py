import serial
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Define the serial port (change this to your specific port)
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")  # Windows example, for Linux use something like '/dev/ttyUSB0'

# Create a serial object
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to establish

# Function to send a message to the Arduino and read the response
def send_message_to_arduino(message):
    command = f"{message}\n"  # Append newline character to the command
    print(f"Sending command: {command.strip()}")
    ser.write(command.encode())  # Encode the command as bytes and send it
    time.sleep(1)  # Wait for Arduino to process the command

    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()  # Read the response from Arduino
        print(f"Arduino response: {response}")

# Example usage: send a message 'Hello, Arduino!' to the Arduino
send_message_to_arduino("1")

# Close the serial connection
ser.close()