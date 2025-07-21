from machine import UART
import time

uart = UART(1, baudrate=9600, tx=5, rx=4)

def send_sms(number, message):
    uart.write(b'AT+CMGF=1\r\n')
    time.sleep(1)
    uart.write(f'AT+CMGS="{number}"\r\n'.encode())
    time.sleep(1)
    uart.write(message.encode() + b'\r\n')
    time.sleep(1)
    uart.write(b'\x1A')
    time.sleep(2)
