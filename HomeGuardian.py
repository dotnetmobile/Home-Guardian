"""
    Home guardian by dotnetmobile@gmail.com
    
    Goal: proof of concept taking a picture of an intruder when very close (<=10 cm) to the home.
    
    Material: raspberry pi + Pi camera + ultrasonic sensor + bread board + 2 resistors (1k Ohm + 2 k Ohm)

    Source code available at: https://github.com/dotnetmobile/Home-Guardian

    All credits go to authors of following references:

    References:
        Pi camera
        - https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
        Ultrasonice sensor
        - https://raspberry-lab.fr/Composants/Mesure-de-distance-avec-HC-SR04-Raspberry-Francais/
        - https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
        Raspberry pi GPIO
        - https://www.raspberrypi.org/documentation/usage/gpio/
        

"""

#Libraries
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


class HomeGuardian:
    
    def __init__(self):
        self.camera = PiCamera()
 
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        
        return distance
        
    def takePicture(self, index):
        self.camera.capture('/home/pi/Desktop/intruder_%s.jpg' % index)
        self.camera.stop_preview()

    def watchDog(self, distance, index):
        if distance < 10:
            print("Alert, intruder !")
            self.takePicture(index)
            index = index + 1
        
        return index
        
        
if __name__ == '__main__':
    try:
        guardian = HomeGuardian()
        
        index = 0
        
        while True:
            dist = guardian.distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            
            index = guardian.watchDog(dist, index)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        
