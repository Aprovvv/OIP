import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM)
GPIO.setup (20, GPIO.OUT)
GPIO.setup (19, GPIO.IN)

n = 10
p = GPIO.PWM (20, 1000)
p.start(0)

try:
    while True:
        f = int (input())
        p.ChangeDutyCycle(f*3.3/100)
        print (f"excpected: {f*3.3/100:.2}")

finally:
    p.stop()
    GPIO.output(20, 0)
    GPIO.cleanup()