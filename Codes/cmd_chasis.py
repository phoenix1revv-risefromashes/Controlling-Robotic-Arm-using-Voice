

# --------------------------------------  piGPIO pins -------------------------------------

from gpiozero import Motor
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Define motor driver pins
motor_factory = PiGPIOFactory()

left_motor = Motor(17, 27, factory=motor_factory)  # Left motor forward, backward
right_motor = Motor(22, 23, factory=motor_factory)  # Right motor forward, backward

def forward():
    left_motor.forward()
    right_motor.forward()
    time.sleep(2)
    left_motor.stop()
    right_motor.stop()

def backward():
    left_motor.backward()
    right_motor.backward()
    time.sleep(2)
    left_motor.stop()
    right_motor.stop()

def right():
    left_motor.stop()
    right_motor.forward()
    time.sleep(2)
    right_motor.stop()

def left():
    left_motor.forward()
    right_motor.stop()
    time.sleep(2)
    left_motor.stop()

def stop():
    left_motor.stop()
    right_motor.stop()

try:
    while True:
        received_text = input("Enter command: ")

        print(f"Received Text:{received_text}")

        if "forward" in received_text:
            print("forward")
            forward()
        elif "backward" in received_text:
            print("backward")
            backward()
        elif "left" in received_text:
            print("left")
            left()
        elif "right" in received_text:
            print("right")
            right()

finally:
    # Ensure motors stop and resources are cleaned up
    stop()


# --------------------------------------- RGPIO pins ------------------------------------
    

import RPi.GPIO as GPIO
import time

HOST ="0.0.0.0"  # Listen on all interfaces
PORT =5000

# Define GPIO pins for motor driver control
in1 = 17  # Left motor forward
in2 = 27  # Left motor backward
in3 = 22  # Right motor forward
in4 = 23  # Right motor backward
enA = 24  # Left motor enable
enB = 25  # Right motor enable



# Define pulse width extremes for servo movement (adjust based on your servo)
open_pulse_width = 1500  # Microseconds for open position
close_pulse_width = 500   # Microseconds for close position

# Set up GPIO
GPIO.setmode(GPIO.BCM)


# Set GPIO pins as output
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)


def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(2)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    

def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


	

def right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(2)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(3)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(2)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


# You can use PWM to control motor speed if needed
pwmA = GPIO.PWM(enA, 100)  # Set PWM frequency to 50 Hz
pwmB = GPIO.PWM(enB, 100)
pwmA.start(100)  # Set initial duty cycle to 50%
pwmB.start(100)


while True:
    received_text = input("Enter command: ")
    print(f"Recieved Text:{received_text}")
    if "forward" in received_text:
        print("actuating: forward")
        forward()
    if "backward" in received_text:
        print("actuating: backward")
        backward()
    if "left" in received_text:
        print("actuating: left")
        left()
    if "right" in received_text:
        print("actuating: right")
        right()
    
GPIO.cleanup()



# corection

1. distance try catch 