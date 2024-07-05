from Arduino import Arduino
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Define the serial port (change this to your specific port)
SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")  # Windows example, for Linux use something like '/dev/ttyUSB0'

# Create a connection to the Arduino board
board = Arduino(SERIAL_PORT)

# Define a pin (Assuming you want to use digital pin 13)
pin = board.get_pin('d:13:o')  # 'd' for digital, '13' for pin number, 'o' for output

# Function to send a command to the Arduino
def send_string_to_arduino(text):
    print(f"Sending command: {text.strip()}")
    command = int(text.strip())
    pin.write(command)
    time.sleep(1)  # Wait to allow Arduino to process the command

# Example usage: send '1' to turn on an LED connected to pin 13, and '0' to turn it off
send_string_to_arduino("1")
time.sleep(2)
send_string_to_arduino("0")

# Close the connection
board.exit()