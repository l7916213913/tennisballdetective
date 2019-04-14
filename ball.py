import numpy as np
import cv2
import imutils
import time
import serial

i=0
timef =15 
##time modulus parameter
tennislower = (29, 86, 6)
tennisupper = (64, 255, 255)
##color scale
vs = cv2.VideoCapture(0)
##catch the pi camera
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
##read Arduino signal from usb hub
while (vs.isOpened()):
    ret, frame = vs.read()
##take 1 picture every 15 frame 
    if (i % timef == 0):
        fn = time.strftime('a')+'.jpg'
        cv2.imwrite(fn,frame)
        img = cv2.imread('a.jpg')
        
        #image prefix (change to single-channel, erode, dilate)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask =cv2.inRange(hsv,tennislower, tennisupper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        #find contours and grab them
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            M = cv2.moments(c)
            x = int (M["m10"]/M["m00"])
            y = int (M["m01"]/M["m00"])        
            print ((x,y))
            if x >= 285 and x <= 365:
                print("Go Straight")
                ser.write(str(1).encode('ascii'))
                time.sleep(1)
            elif x < 285:
                print("turn left for 0.1s")
                ser.write(str(2).encode('ascii'))
                time.sleep(0.5)
            else:
                print("turn right for 0.1s")
                ser.write(str(3).encode('ascii'))
                time.sleep(0.5)
        else:
            print("turn fucking right")
            ser.write(str(3).encode('ascii'))
            time.sleep(0.5)
        #cv2.imshow('img', img)
        #key = cv2.waitKey(1) & 0xFF
       #if key == ord('q'):
        #    break
    i=i+1
vs.release()
cv2.destroyAllWindows()
