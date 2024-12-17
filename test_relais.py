"""
* -----------------------------------------------------------------------------------
* Last update :   11/09/2023
* Project Irripi V1
* Test des Relais passage etat bas => haut
* -----------------------------------------------------------------------------------
"""

import RPi.GPIO as GPIO
import time

list_gpio = [4,17,27,22,10,9,11,5,6,13,19,26,21,20,16,12,7,8,25,24,23,18]
#list_gpio = [12,7,8,25]

time.sleep(25)

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
for gpio in list_gpio:
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)

print("Début du test")

for gpio in list_gpio:
    print("Gpio : {0}".format(gpio))
    GPIO.output(gpio, GPIO.LOW)
    time.sleep(2)
    GPIO.output(gpio, GPIO.HIGH)
    time.sleep(2)

print("Fin du test")