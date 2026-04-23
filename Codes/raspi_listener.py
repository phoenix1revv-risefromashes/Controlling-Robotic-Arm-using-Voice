import socket
import RPi.GPIO as GPIO
import time
from gpiozero import AngularServo

HOST ="0.0.0.0"  # Listen on all interfaces
PORT =5000

# Define GPIO pins for motor driver control
in1 = 17  # Left motor forward
in2 = 27  # Left motor backward
in3 = 22  # Right motor forward
in4 = 23  # Right motor backward
enA = 24  # Left motor enable
enB = 25  # Right motor enable

# Servos driving
servo2 = AngularServo(16, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023)
servo3 = AngularServo(20, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023)
#servo4 = AngularServo(27, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023)
#clamper = AngularServo(21, min_angle=0, max_angle=90, min_pulse_width=0.0006, max_pulse_width=0.0023)


clamper=21

# Define pulse width extremes for servo movement (adjust based on your servo)
open_pulse_width = 1500  # Microseconds for open position
close_pulse_width = 500   # Microseconds for close position

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(clamper, GPIO.OUT)


# Set GPIO pins as output
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)

# Function to open the gripper slowly
def open_gripper():
  pwm = GPIO.PWM(clamper, 50)  # Set PWM frequency to 50Hz
  pwm.start(0)  # Start PWM with duty cycle of 0 (initial position)

  # Gradually increase duty cycle to open position
  for i in range(0, open_pulse_width, 10):
    pwm.ChangeDutyCycle(i / 10)
    time.sleep(0.01)  # Adjust sleep time for desired speed

  pwm.stop()  # Stop PWM

# Function to close the gripper slowly
def close_gripper():
  pwm = GPIO.PWM(clamper, 50)
  pwm.start(0)

  # Gradually decrease duty cycle to close position
  for i in range(close_pulse_width, 2500, -10):
    pwm.ChangeDutyCycle(i / 10)
    time.sleep(0.01)  # Adjust sleep time for desired speed

  pwm.stop()

# Function to stop the gripper movement
def stop_gripper():
  pwm = GPIO.PWM(clamper, 50)
  pwm.start(0)
  pwm.stop()

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

def picking():
	servo2.angle=83
	servo3.angle=60
	open_gripper()
	time.sleep(2)
	close_gripper()
	time.sleep(2)
	stop_gripper()
	
	

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


sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(1)

print(f"Listening for connection on {HOST}:{PORT}")
conn,addr = sock.accept()
print(f"Connection from {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
        
    received_text=data.decode()
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
    if "pick" in received_text:
        print("actuating: picking")
        picking() 
    
conn.close()
GPIO.cleanup()
