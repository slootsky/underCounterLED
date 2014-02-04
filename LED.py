# from http://learn.adafruit.com/fading-a-rgb-led-on-beaglebone-black/writing-a-program
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

import time
import datetime
import ephem
 
red = "P8_13"
green = "P8_19"
blue = "P9_14"
light_sensor = "P9_40"
 
night_red=float(100)
night_green=float(55)
night_blue=float(15)

day_red=float(100)
day_green=float(75)
day_blue=float(55)

PWM.start(red, 0)
PWM.start(blue, 0)
PWM.start(green, 0)
ADC.setup()

C_DAY = 1
C_NIGHT = 2
last_light_reading = -1
 
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
		light_reading = light_reading * light_reading * light_reading
#		light_reading = light_reading * light_reading 

		if ( last_light_reading == -1 ) :
			last_light_reading = light_reading *2

		light_change = abs( ( last_light_reading - light_reading ) / light_reading)
		if (next_sunrise < next_sunset):
#                       print "currently night"
#                       next_event=next_sunrise
#                       print "light: {} \t red: {}".format(light_reading,night_red*light_reading)
#                       if ( light_change > .1) or ( last_time == C_DAY ) :
			if 1==1 :
				PWM.set_duty_cycle(red,night_red*light_reading)
				PWM.set_duty_cycle(green,night_green*light_reading)
				PWM.set_duty_cycle(blue,night_blue*light_reading)
			last_time = C_NIGHT
		else:
#                       print "currently day"
#                       next_event=next_sunset
#                       if ( light_change > .1) or ( last_time == C_NIGHT ) :
			if 1==1 :
				PWM.set_duty_cycle(red,day_red*light_reading)
				PWM.set_duty_cycle(green,day_green*light_reading)
				PWM.set_duty_cycle(blue,day_blue*light_reading)
			last_time = C_DAY

		# sleep for about 50ms
		time.sleep(50.0/1000.0)
		now=datetime.datetime.now()

