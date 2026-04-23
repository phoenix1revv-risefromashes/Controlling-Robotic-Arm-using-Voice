# -------------------------------------------- import libaries -----------------------------------------------
from gpiozero import DistanceSensor,Servo,AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import socket
import time
import math
import numpy as np


# -------------------------------------------- Pigpio setup -------------------------------------------------

#  ---------- Chasis motor --------------
# Define GPIO pins for motor driver control
in1 = 17  # Left motor forward
in2 = 27  # Left motor backward
in3 = 22  # Right motor forward
in4 = 23  # Right motor backward
enA = 24  # Left motor enable
enB = 25  # Right motor enable

#  -----------Ultrasonic ----------
TRIG_PIN = 15  # GPIO pin for trigger
ECHO_PIN = 14  # GPIO pin for echo

#  ----------- Servos  -----------
SERVO1_PIN = 26
SERVO2_PIN = 16
SERVO3_PIN = 20
SERVO4_PIN = 21 #clamper

# --------- pin factory -----------
factory = PiGPIOFactory()

# -------------------------------------------- ultilities ---------------------------------------------------


# -------------------------------------------- Distance -----------------------------------------------------

def measureDistance():
    print("-------------------------- Distance Discovery -------------------------")
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, pin_factory=factory)
    distance = sensor.distance * 100  # Convert distance to centimeters
    distance = round(distance, 2)
    print("---> returned: ", distance, " cm")
    return distance


# -------------------------------------------- Kinematics ---------------------------------------------------

deg = 57.29577 # def = rad * (180/pi = 57.29277)

arm = 12 # length of arm in cm
farm = 26.5 # length of forearm in cm
bh = 3 #14 # height of base motor in cm

bc = 7 # 5+2.5 : bc : dist from base to camera
rhc = 12 # rhc: robotic hand working contrained distance from camera
wr = bc + rhc #wr: working radius from basemotor centre to object

def kinematics(d_cm):
    print("------------------------------ Kinematics ------------------------------")
    d_cm -= 3
    d_cm += bc

    if d_cm > wr:
      # d_pix = np.sqrt((x**2-2**2)+(y**2-4**2)) # distance in pixel coordinate
      # d_pixInc = d_pix/ppi # convert to inch
      # Distance from base motor centre to object  in cm
      
      d_sl = np.sqrt((d_cm**2)+(bh**2))  # slated distance from top of base motor to position of object
      print("\nDist from base-cam-obj: ", d_cm ," cm")

      #------------ dof1 ----------------
      # dof1 = (math.atan2(y, x))*deg
      # print("dof1: ", dof1)
      
      
      #------------ dof2 ----------------
      cos_dof2 = (arm**2+d_sl**2 - farm**2)/(2*arm*d_sl)
      print("cos_dof2: ",cos_dof2)
      

      #------------ dof3 ----------------
      # sin_dof3 = D * math.sin(dof2)/f_arm
      cos_dof3  = (arm**2+farm**2-d_sl**2)/(2*arm*farm)
      print("cos_dof3: ",cos_dof3)
      
      dof2_case = (cos_dof2<=1 and cos_dof2>=-1)
      dof3_case = (cos_dof3<=1 and cos_dof3>=-1)
      if(dof2_case and dof3_case):
         
         dof2 = (math.acos(cos_dof2))*deg 
         dof3 = (math.acos(cos_dof3))*deg 
         
         bol_dof2 = dof2>0 and dof2<270
         bol_dof3 = dof3>0 and dof3<270
         if (bol_dof2 and bol_dof3):
            # sin_dof4 = arm * math.sin(dof2)/f_arm
            # cos_dof4 = (D**2 + f_arm**2 - arm**2)/(2*f_arm*D)
            # dof4 = (math.asin(cos_dof4))*deg
            print("\n -------> Applying angles to servos  <---------")
            # time.sleep(2)
            # print("base motor: dof1: ", dof1)
            # servo1.angle = dof1

            # time.sleep(2)
            print("shoulder motor: dof2: ", dof2)
            #servo2.angle = dof2

            # time.sleep(2)
            print("elbow motor: dof3: ", dof3)
            # print("actual dof3: 180-dof3: ", 180 - dof3)
            #servo3.angle = 180-dof3 
            print("dof2:{}, dof3:{}".format(dof2, dof3))
            return dof2, dof3
         else:
             print(" ---X out  of [0,270] dof-range")
             return 0,0
      else:
          print(" ---X out of [-1,1] range")
          return  0,0
      
    else:
        print(" ---X math domain error")
        return 0,0
    
# -------------------------------------------- servo controls -----------------------------------------------
            
def ServoControlling(dof_2, dof_3):
    print("------------------------------ Servo Controlling -------------------------------")
    servo1 = AngularServo(SERVO1_PIN, initial_angle=100, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=factory)
    servo2 = AngularServo(SERVO2_PIN, initial_angle=100, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=factory)
    servo3 = AngularServo(SERVO3_PIN, initial_angle=150, min_angle=0, max_angle=270, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=factory)
    clamper = Servo(SERVO4_PIN, min_pulse_width=0.0006, max_pulse_width=0.002, frame_width=0.09, pin_factory=factory)

    dof2 = dof_2 + 10
    dof3 = dof_3 -10
    pi_dof3 = 300-dof3
    hpi_dof3 = 90+dof3

    # ------------ Clamper ----------------
    clamper_open_time = 2  # Time to keep clamper open (in seconds)
    clamper_close_time = 4  # Time to keep clamper closed (in seconds)

    clamper_open = True  # Flag to indicate whether the clamper is currently open or closed
    clamper_last_toggle_time = time.time()  # Initialize last toggle time

    try:
        for i in range(2):
        
            print("---->Open Clamper")
            clamper.max()
            time.sleep(2)  

            print("---->servo1 ")     
            servo1.angle = 100
            time.sleep(2)

            print("----> servo2 ")
            #dof2 += 5
            servo2.angle = dof2
            time.sleep(2)

            print("\n----->servo3")
            #pi_dof3 += 5
            servo3.angle = pi_dof3
            time.sleep(2)

            current_time = time.time()
            if clamper_open and current_time - clamper_last_toggle_time >= clamper_close_time:
                clamper.max()  # Open clamper
                time.sleep(1)
                clamper_open = True
                clamper_last_toggle_time = current_time
                # clamped = input("Will it clamp? : ")
                time.sleep(2)
                clamper.min() #grap
                time.sleep(2)
                servo3.angle = 100
                time.sleep(2)
                servo2.angle = 100
                time.sleep(2)
                servo1.angle = 20 #dustbin
                time.sleep(2)
                servo3.angle = 170
                time.sleep(2)
                clamper.max() #open clamper
                time.sleep(2)
                print(" In the dustbin Done !!")

                servo3.angle = 0
                time.sleep(1)
                servo1.angle = 100
                time.sleep(1)
                servo2.angle = 20
                time.sleep(1)
                # break
                

            elif clamper_open and current_time - clamper_last_toggle_time >= clamper_open_time:
                clamper.angle = 0  # Close clamper
                clamper_open = False
                clamper_last_toggle_time = current_time
                    
                        
    finally:
        # Cleanup
        servo1.close()
        servo3.close()
        servo2.close()
        clamper.close()


# -------------------------------------------- servo listens ------------------------------------------------

HOST ="0.0.0.0"  # Listen on all interfaces
PORT =5000

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

# You can use PWM to control motor speed if needed
pwmA = GPIO.PWM(enA, 100)  # Set PWM frequency to 50 Hz
pwmB = GPIO.PWM(enB, 100)
pwmA.start(100)  # Set initial duty cycle to 50%
pwmB.start(100)

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
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(2)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
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

def pick_mechanism():
    print("----> pick_mechanism <---")
    discoverd_dist = measureDistance()
    print("-->pm, discoverd_distance: ", discoverd_dist)
    dof2, dof3 = kinematics(discoverd_dist)
    print("-->pm: dof2: {}, dof3: {}".format(dof2, dof3))
    ServoControlling(dof_2=dof2, dof_3=dof3)
    time.sleep(2)
    print("-->  done picking <---")


# -------------------------------------------- operator ----------------------------------------------------
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(1)

print(f"Listening for connection on {HOST}:{PORT}")
conn,addr = sock.accept()
print(f"Connection from {addr}")

while True:
    try:
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
        if "grab" in received_text:
            print("actuating: pick")
            pick_mechanism()
            time.sleep(3)
    finally:
        print("all done!")