from machine import ADC

sensor = ADC(0)

def read_gas_level():
    return sensor.read()  # return 0-1023
