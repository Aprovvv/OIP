import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

dt = 0.05

GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT)

#making binary number out of decimal
def dec2bin (num):
    ans = [0]*8
    for i in range (0, 8):
        ans[7-i] = num % 2
        num //= 2
    return ans

#getting voltage from comparator (comp)
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

#lighing leds to show binary number
def leds_on():
    leds_count = int(results * 8 / 255)
    leds_val = [0]*8
    for i in range(0, leds_count):
        leds_val[i] = 1
    GPIO.output (leds, leds_val)

try:
    duration = time.time()
    GPIO.output(troyka, 1)
    time.sleep(dt)

    #waiting for user to press button
    print("Press button!")
    while adc() >= 1:
        time.sleep(dt)

    #starting charging
    measured_data = [adc() / 255 * 3.3]
    print("Button pressed! Starting charging")
    while measured_data[-1] < 0.8 * 3.3:
        measured_data.append(adc() / 255 * 3.3)
        time.sleep(dt)
    
    #starting discharging
    print("U >= 2.64 Volt. Starting discharging")
    GPIO.output(troyka, 0)
    while measured_data[-1] > 0.69 * 3.3:
        measured_data.append(adc() / 255 * 3.3)
        time.sleep(dt)

    #calculating duration
    duration = time.time() - duration
    print("Experiment finished")

    #saving data and settings to file
    measured_data_str = [str(item) for item in measured_data]
    with open("data.txt", "w") as output:
        output.write("\n".join(measured_data_str))
    with open("settings.txt", "w") as output:
        output.write(f"Settings: frequency = {1/dt:.0f}, quantization step = {3.3/255:.2f}")
    print(f"Results: duration = {duration:.1f}, one measure time = {dt:.2f}, frequency = {1/dt:.0f}, quantization step = {3.3/255:.3f}")

    #building plot
    plt.plot (measured_data)
    plt.show ()

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()