import RPi.GPIO as GPIO

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

try:
    while True:
        num = input ("Type a number from 0 to 255: ")
        try:
            num = int (num)
            if 0 <= num <= 255:
                GPIO.output (dac, dec2bin (num))
                voltage = float (num) / 255.0 * 3.3
                print (f"Output voltage is about {voltage:.4} volt")
            else:
                if num < 0:
                    print ("Number must be >= 0 Try again")
                elif num > 255:
                    print ("Number is out of range [0, 255]. Try again")
        except Exception:
            if num == "q": break
            print ("You have to type a number. Try again")

finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()
    print("EOP")
