# from http://learn.adafruit.com/fading-a-rgb-led-on-beaglebone-black/writing-a-program
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import math
import time
import datetime
import ephem

DEBUG = 2

C_INIT = 0
C_OFF = 1
C_LOW = 2
C_AUTO = 3
C_HIGH = 4
C_DAY = 11
C_NIGHT = 12
C_DAY_START = C_OFF
C_NIGHT_START = C_AUTO

C_MIN_LIGHT_READING = 0
#C_MIN_LIGHT_READING = 0.05




def button_pressed(value):
	global mode
	global last_time

	if last_time == C_DAY :
		if mode == C_OFF :
			mode = C_AUTO
			if DEBUG > 0 :
				print ("mode: AUTO")
		elif mode == C_AUTO :
			mode = C_HIGH
			if DEBUG > 0 :
				print ("mode: HIGH")
		elif mode == C_HIGH :
			mode = C_OFF
			if DEBUG > 0 :
				print ("mode: OFF")

	elif last_time == C_NIGHT :
		if mode == C_LOW :
			mode = C_AUTO
			if DEBUG > 0 :
				print ("mode: AUTO")
		elif mode == C_AUTO :
			mode = C_HIGH
			if DEBUG > 0 :
				print ("mode: HIGH")
		elif mode == C_HIGH :
			mode = C_LOW
			if DEBUG > 0 :
				print ("mode: LOW")
 
green = "P8_13"
red = "P8_19"
blue = "P9_14"
light_sensor = "AIN0" # "P9_40"
button = "P8_11"
 
night_red=float(100)
night_green=float(55)
night_blue=float(15)

day_red=float(100)
day_green=float(75)
day_blue=float(55)

ADC.setup()

PWM.start(red, 0)
PWM.start(blue, 0)
PWM.start(green, 0)

last_light_reading = -1
mode = C_INIT
last_time = C_INIT

#GPIO.setup ( button, GPIO.IN )
#GPIO.add_event_detect(button, GPIO.RISING, callback=button_pressed, bouncetime=300)

multiplier = 1.0


PWM.set_duty_cycle(red,night_red*multiplier)
PWM.set_duty_cycle(green,night_green*multiplier)
PWM.set_duty_cycle(blue,night_blue*multiplier)



