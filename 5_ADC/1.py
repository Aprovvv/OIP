import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

def dec2bin (num):
    ans = [0]*8
    for i in range (0, 8):
        ans[7-i] = num % 2
        num //= 2
    return ans

def adc ():
    for value in range(0, 256):
        GPIO.output (dac, dec2bin (value))
        time.sleep(0.01)

        compValue = GPIO.input (comp)
        if (compValue == 1):
            return value

    return 256

try:
    while True:
        voltage = adc () * 3.3 / 256
        print (voltage)

finally:
    GPIO.output (dac, 0)
    GPIO.output (troyka, 0)
    GPIO.cleanup()