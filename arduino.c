#include <Servo.h>

// Create servo objects
Servo servo1;
Servo servo2;
Servo servo3;
void moveServo(int motorSelection);

// Pin numbers for the servos
const int servoPin1 = 2;
const int servoPin2 = 3;
const int servoPin3 = 4;

// Pin number for motion sensor
const int motionPin = 5;

void setup() {
  // Attach the servo objects to the pin numbers
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);
  pinMode(8,OUTPUT);

  // Start with all servos at 0 degrees
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);

  moveServo(3);  // Move servo 1, you can change the parameter to 2 or 3
}

void loop() {

}

void moveServo(int motorSelection) {
  switch (motorSelection) {
    case 1:
      // Rotate servo 1 to 90 degrees
      servo1.write(90);
      digitalWrite(8,HIGH);
      delay(5000);
      digitalWrite(8,LOW);
      // Rotate back to 0 degrees
      servo1.write(0);
      break;
    case 2:
      // Rotate servo 2 to 90 degrees
      servo2.write(90);
      digitalWrite(8,HIGH);
      delay(5000);
       digitalWrite(8,LOW);
      // Rotate back to 0 degrees
      servo2.write(0);
      break;
    case 3:
      // Rotate servo 3 to 90 degrees
      servo3.write(90);
      digitalWrite(8,HIGH);

      delay(5000);
      digitalWrite(8,LOW);

      // Rotate back to 0 degrees
      servo3.write(0);
      break;
    default:
      // If the motorSelection variable is not 1, 2, or 3, do nothing
      break;
  }
}

