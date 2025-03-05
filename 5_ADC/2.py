import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=1)


def dec2bin (num):
    ans = [0]*8
    for i in range (0, 8):
        ans[7-i] = num % 2
        num //= 2
    return ans


def adc():
    ans = 0
    check_val = [0]*8
    for i in range(0, 8):
        check_val [i] = 1
        GPIO.output (dac, check_val)
        time.sleep (0.01)
        if (GPIO.input (comp) == 0):
            ans += 2**(7-i)
        else:
            check_val[i] = 0
    return ans




try:

    while True:
        
        results = adc()
        voltage = results* 3.3 / 256

        print(voltage)

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()

