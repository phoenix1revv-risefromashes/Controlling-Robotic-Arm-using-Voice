from socket import socket, AF_INET, SOCK_STREAM
from gpiozero import Motor, GPIOFactory
from gpiozero.pins.pigpio import PiGPIOFactory
import time

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

# Define motor driver pins
factory = PiGPIOFactory()

left_motor = Motor(17, 27, pin_factory=factory)  # Left motor forward, backward
right_motor = Motor(22, 23, pin_factory=factory)  # Right motor forward, backward

def backward(): 
    left_motor.forward()
    right_motor.forward()
    time.sleep(2)
    left_motor.stop()
    right_motor.stop()

def forward():
    left_motor.backward()
    right_motor.backward()
    time.sleep(2)
    left_motor.stop()
    right_motor.stop()

def left():
    left_motor.stop()
    right_motor.forward()
    time.sleep(2)
    right_motor.stop()

def right():
    left_motor.forward()
    right_motor.stop()
    time.sleep(2)
    left_motor.stop()

def stop():
    left_motor.stop()
    right_motor.stop()


# Socket setup remains the same

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print(f"Listening for connection on {HOST}:{PORT}")
conn, addr = sock.accept()
print(f"Connection from {addr}")

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break

        received_text = data.decode()
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
    conn.close()
