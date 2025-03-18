import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13


GPIO.setmode(GPIO.BCM)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def decimal_to_binary_list(n):
    return [int(bit) for bit in bin(n)[2:].zfill(8)]

def adc():
    value = 0
    for counter in range(7,-1,-1):  
        value +=2**counter
        GPIO.output(dac, decimal_to_binary_list(value))
        time.sleep(0.01) 
        if GPIO.input(comp) == 1:
            value -=2**counter
    return value

def Leds_func(voltage):
    numled= int(voltage/3.3 *8)
    for counter in range(8):
        if counter<numled:
            GPIO.output(leds[counter],1)
        else:
            GPIO.output(leds[counter],0)

try:
    while True:
        value = adc()  
        voltage = (value / 256.0) * 3.3 
        print(f"Voltage =  {voltage:.2f}V")
        Leds_func(voltage)

finally:
    GPIO.output(dac, 0)
    
    GPIO.cleanup()
