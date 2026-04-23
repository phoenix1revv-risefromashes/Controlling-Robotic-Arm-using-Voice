import RPi.GPIO as GPIO
import time
import RT_IK as IK
import IK_angle_eval_with_clamper as SC


# Set GPIO pins
TRIG_PIN = 15
ECHO_PIN = 14

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Set TRIG_PIN to LOW for 2 microseconds
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.02)
    
    # Send a pulse signal on TRIG_PIN
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Measure the time for echo
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    
    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 33200  # Speed of sound in cm/s
    distance = (pulse_duration * speed_of_sound) / 2
    distance = round(distance, 2)
    
    return distance

if __name__ == '__main__':
    try:
        setup()
        while True:
            distance = get_distance()
            print("Distance: {} cm".format(distance))
            dof2, dof3, dw_dof3 = IK.kinematics(distance)
            SC.ServoControlling(dof2=dof2, dw_dof3=dw_dof3)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
