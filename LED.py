# from http://learn.adafruit.com/fading-a-rgb-led-on-beaglebone-black/writing-a-program
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import math
import time
import datetime
import ephem

DEBUG = 1

C_INIT = 0
C_OFF = 1
C_LOW = 2
C_AUTO = 3
C_HIGH = 4
C_DAY = 11
C_NIGHT = 12
C_DAY_START = C_OFF
C_NIGHT_START = C_AUTO

#C_MIN_LIGHT_READING = 0
C_MIN_LIGHT_READING = 0.05




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

GPIO.setup ( button, GPIO.IN )
GPIO.add_event_detect(button, GPIO.RISING, callback=button_pressed, bouncetime=300)

 
while True:
	o=ephem.Observer()  
	o.long='-75.6919'
	o.lat='45.4214'

	now=datetime.datetime.now()
	s=ephem.Sun()  
	s.compute()  
	next_sunrise=ephem.localtime(o.next_rising(s))  
	next_sunset=ephem.localtime(o.next_setting(s))  
	print "next sunrise: {}".format( next_sunrise )
	print "next sunset: {}".format( next_sunset )
	print "it is now:{}".format(now)

#       next_event=min(next_sunrise,next_sunset)
	print "time to next event:  {}".format(min(next_sunrise,next_sunset)-now)

	while ( (now < next_sunrise)  and (now < next_sunset) ) :
		light_reading = ADC.read(light_sensor)

		# exaggerate the light reading (0-1)
		light_reading = 1.0 - (light_reading + light_reading)
#		light_reading = math.log10(light_reading*100) - 1
#		light_reading = light_reading * light_reading * light_reading
#		light_reading = light_reading * light_reading * light_reading * light_reading
#		light_reading = light_reading * light_reading * light_reading * light_reading * light_reading
#		light_reading = light_reading * light_reading 

		if ( light_reading > 1) :
			light_reading = 1
		if ( light_reading < C_MIN_LIGHT_READING ) :
			light_reading = C_MIN_LIGHT_READING

		if ( last_light_reading == -1 ) :
			last_light_reading = light_reading *2

#		light_change = abs( ( last_light_reading - light_reading ) / light_reading)

		if DEBUG > 1 :
			print "light_reading: {}".format(light_reading)

		if (next_sunrise < next_sunset):
			#
			# NIGHT TIME
			#
			if last_time != C_NIGHT :
				last_time = C_NIGHT
				mode = C_NIGHT_START

#                       print "currently night"
#                       next_event=next_sunrise

#                       if ( light_change > .1) or ( last_time == C_DAY ) :

			if mode == C_INIT :
				mode = C_NIGHT_START

			if mode == C_LOW :
				multiplier = 0.08
			elif mode == C_HIGH :
				multiplier = 1
			else :
				multiplier = light_reading

			if DEBUG > 1 :
				print "light: {} \t muliplier: {} \t red: {}".format(light_reading,multiplier, night_red*multiplier)

			PWM.set_duty_cycle(red,night_red*multiplier)
			PWM.set_duty_cycle(green,night_green*multiplier)
			PWM.set_duty_cycle(blue,night_blue*multiplier)

		else:
			#
			# DAY TIME
			#
			if last_time != C_DAY :
				last_time = C_DAY
				mode = C_DAY_START

#                       print "currently day"
#                       next_event=next_sunset
#                       if ( light_change > .1) or ( last_time == C_NIGHT ) :

			if mode == C_INIT :
				mode = C_DAY_START

			if mode == C_OFF :
				multiplier = 0.0
			elif mode == C_HIGH :
				multiplier = 1.0
			else :
				multiplier = light_reading

			if DEBUG > 1 :
				print "light: {} \t muliplier: {} \t red: {}".format(light_reading,multiplier, night_red*multiplier)

			PWM.set_duty_cycle(red,day_red*multiplier)
			PWM.set_duty_cycle(green,day_green*multiplier)
			PWM.set_duty_cycle(blue,day_blue*multiplier)

		# sleep for about 50ms
		time.sleep(50.0/1000.0)
		now=datetime.datetime.now()


