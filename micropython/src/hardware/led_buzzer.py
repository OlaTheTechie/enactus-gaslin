from machine import Pin
import time

buzzer = Pin(14, Pin.OUT)
green = Pin(12, Pin.OUT)
red = Pin(13, Pin.OUT)

def alert_on():
    red.on()
    green.off()

def alert_off():
    red.off()
    green.on()

def beep(times=5):
    for _ in range(times):
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        time.sleep(0.2)
