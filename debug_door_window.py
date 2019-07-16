"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

def closeMotor(pin):
    #doors
    if(pin == 0):
        kit.servo[pin].angle = 60
    elif(pin == 1):
        kit.servo[pin].angle = 57
    elif(pin == 2):
        kit.servo[pin].angle = 55
    elif(pin == 3):
        kit.servo[pin].angle = 70
    elif(pin == 4):
        kit.servo[pin].angle = 60
    elif(pin == 5):
        kit.servo[pin].angle = 60
    elif(pin == 6):
        kit.servo[pin].angle = 62
    #windows
    elif(pin == 8):
        kit.servo[pin].angle = 65
    elif(pin == 9):
        kit.servo[pin].angle = 56
    elif(pin == 10):
        kit.servo[pin].angle = 69
    elif(pin == 11):
        kit.servo[pin].angle = 60
    elif(pin == 12):
        kit.servo[pin].angle = 47
    elif(pin == 13):
        kit.servo[pin].angle = 56
    elif(pin == 14):
        kit.servo[pin].angle = 60
    elif(pin == 15):
        kit.servo[pin].angle = 46
    else:
        kit.servo[pin].angle = 60

def openMotor(pin):
    #doors
    if(pin == 0):
        kit.servo[pin].angle = 180
    elif(pin == 1):
        kit.servo[pin].angle = 180
    elif(pin == 2):
        kit.servo[pin].angle = 180
    elif(pin == 3):
        kit.servo[pin].angle = 180
    elif(pin == 4):
        kit.servo[pin].angle = 180
    elif(pin == 5):
        kit.servo[pin].angle = 180
    elif(pin == 6):
        kit.servo[pin].angle = 180
    #windows
    elif(pin == 8):
        kit.servo[pin].angle = 180
    elif(pin == 9):
        kit.servo[pin].angle = 180
    elif(pin == 10):
        kit.servo[pin].angle = 180
    elif(pin == 11):
        kit.servo[pin].angle = 170
    elif(pin == 12):
        kit.servo[pin].angle = 180
    elif(pin == 13):
        kit.servo[pin].angle = 165
    elif(pin == 14):
        kit.servo[pin].angle = 180
    elif(pin == 15):
        kit.servo[pin].angle = 159
    else:
        kit.servo[pin].angle = 180

 # Each Pulse Width Modulation (PWM) Pin corresponds to a motor
 # PWM 0 - 6 : doors
 # PWM 8 - 15 : windows
 # 00 : Bedroom 2 - Bathroom
 # 01 : Bedroom 1 - Living Rm
 # 02 : Living Rm - Kitchen
 # 03 : Living Rm - Bathroom
 # 04 : Bedroom 1 - Bathroom
 # 05 : Living Rm - Front Door
 # 06 : Bedroom 1 - Back Door
 
 # 08 : Bedroom 1, 2 ft.
 # 09 : Living Rm, 2 ft.
 # 10 : Bedroom 2, 2 ft
 # 11 : Kitchen, 2 ft.
 # 12 : Bedroom 2, 3 ft.
 # 13 : Living Rm, 3 ft.
 # 14 : Kitchen, 3 ft.
 # 15 : Bedroom 1, 3 ft.

while(True):
  	try:
   		while True:
       		print('Enter desired operation')
           	op = input().lower()
          	words = op.split()
          	if op == 'open all':
              	print("opening all doors and windows")
              	openAll()
        	elif op == 'close all':
          		print("closing all doors and windows")
               	closeAll()
          	elif op == 'open all doors':
       			print("opening all doors")
               	openAllDoors()
          	elif op == 'close all doors':
          		print("closing all doors")
               	closeAllDoors()
           	elif op == 'open all windows':
            	print("opening all windows")
              	openAllWindows()
          	elif op == 'close all windows':
            	print("closing all windows")
              	closeAllWindows()
           	elif words[0] == 'open':
           		#open based on pin number
            	print("opening " + motor_names[int(words[1])])
              	motorOpen(int(words[1]))
          	elif words[0] == 'close':
            	#close based on pin number
              	print("closing " + motor_names[int(words[1])])
               	motorClose(int(words[1]))
           	else:
           		print('Incorrect input.')
    
    except KeyboardInterrupt:
    	print("Keyboard interrupt.")
   	except Exception as e: 
  		print(e)
   	finally:
   		GPIO.cleanup()