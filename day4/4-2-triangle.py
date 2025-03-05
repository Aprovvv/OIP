import RPi.GPIO as GPIO
import time

def dec2bin (num):
    ans = [0]*8
    for i in range (0, 8):
        ans[7-i] = num % 2
        num //= 2
    return ans

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)

inc_flag = 0
t = 0
x = 0
try:
    period = float (input ("Type a period for sygnal: "))
    while True:
        GPIO.output(dac, dec2bin(x))
        print (dec2bin(x))
        if x == 0: 
            inc_flag = 1
        elif x == 225: 
            inc_flag = 0

        if inc_flag == 1:
            x += 1
        else:
            x -= 1
        time.sleep (period/512)
        t += 1

except ValueError:
    print ("value error")

finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()
    print("EOP")