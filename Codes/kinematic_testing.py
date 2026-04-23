import math
import numpy as np



deg = 57.29577 # def = rad * (180/pi = 57.29277)

arm = 12 # length of arm in cm
farm = 26.5 # length of forearm in cm
bh = 14 # height of base motor in cm

bc = 7 # 5+2.5 : bc : dist from base to camera
rhc = 12 # rhc: robotic hand working contrained distance from camera
wr = bc + rhc #wr: working radius from basemotor centre to object

def kinematics(d_cm):
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
            print("actual dof3: 180-dof3: ", 180 - dof3)
            #servo3.angle = 180-dof3

dis = float(input("dist: "))
kinematics(dis)