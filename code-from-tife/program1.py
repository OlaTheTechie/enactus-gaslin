from machine import Pin, ADC, UART
import time
import urequests  # For HTTP requests to CallMeBot
import network    # For Wi-Fi connection

# Wi-Fi setup function
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect("YOUR_SSID", "YOUR_PASSWORD")  # Replace with your hotspot SSID and password
        timeout = 10  # Wait up to 10 seconds
        start = time.time()
        while not wlan.isconnected() and (time.time() - start) < timeout:
            time.sleep(1)
        if wlan.isconnected():
            print("Connected to Wi-Fi:", wlan.ifconfig())
        else:
            print("Wi-Fi connection failed")
    return wlan

# Initial Wi-Fi connection
wlan = connect_wifi()

# Pin setup
mq6 = ADC(0)           # A0 for gas sensor
buzzer = Pin(14, Pin.OUT)  # D5 for buzzer
green_led = Pin(12, Pin.OUT)  # D6
red_led = Pin(13, Pin.OUT)    # D7
uart = UART(1, baudrate=9600, tx=5, rx=4)  # D1 TX, D2 RX for SIM800L

# WhatsApp setup (CallMeBot API)
phone_numbers = ["+1234567890", "+0987654321"]  # Replace with your numbers
api_key = "YOUR_CALLMEBOT_APIKEY"  # Replace with your CallMeBot API key
whatsapp_url = "http://api.callmebot.com/whatsapp.php"

# SMS setup for SIM800L
def send_sms(phone_number, message):
    uart.write(b'AT+CMGF=1\r\n')  # Set SMS text mode
    time.sleep(1)
    uart.write(f'AT+CMGS="{phone_number}"\r\n'.encode())
    time.sleep(1)
    uart.write(message.encode() + b'\r\n')
    time.sleep(1)
    uart.write(b'\x1A')  # Ctrl+Z to send
    time.sleep(2)  # Wait for SMS to send

# WhatsApp notification function
def send_whatsapp(phone_number, message):
    if wlan.isconnected():
        payload = {
            "phone": phone_number,
            "text": message,
            "apikey": api_key
        }
        try:
            response = urequests.get(whatsapp_url, params=payload)
            if response.status_code == 200:
                print(f"WhatsApp sent to {phone_number}")
            else:
                print(f"WhatsApp failed for {phone_number}: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"WhatsApp error: {e}")
    else:
        print(f"Wi-Fi down, skipping WhatsApp for {phone_number}")

# Buzzer alarm function
def trigger_buzzer():
    for _ in range(5):  # Beep 5 times
        buzzer.on()
        time.sleep(0.2)  # 200ms on
        buzzer.off()
        time.sleep(0.2)  # 200ms off

# Main loop
threshold = 300  # Adjust based on your MQ-6 readings
alert_cooldown = 300  # 5-minute cooldown (in seconds)
last_alert = -alert_cooldown  # Allow immediate first alert
wifi_check_interval = 60  # Check Wi-Fi every 60 seconds
last_wifi_check = time.time()

while True:
    # Periodic Wi-Fi check and reconnection
    if (time.time() - last_wifi_check) > wifi_check_interval:
        if not wlan.isconnected():
            print("Wi-Fi disconnected, attempting to reconnect...")
            wlan = connect_wifi()
        last_wifi_check = time.time()

    # Gas monitoring
    gas_level = mq6.read()  # 0-1023 range
    print("Gas level:", gas_level)

    if gas_level > threshold and (time.time() - last_alert) > alert_cooldown:
        # Alert condition met and cooldown elapsed
        green_led.off()
        red_led.on()
        
        # Trigger buzzer
        trigger_buzzer()
        
        # Send WhatsApp to all numbers
        alert_message = "Gas detected! Level: {}".format(gas_level)
        for number in phone_numbers:
            send_whatsapp(number, alert_message)
        
        # Send SMS to all numbers
        for number in phone_numbers:
            send_sms(number, alert_message)
        
        last_alert = time.time()  # Update last alert time
    else:
        # Safe condition
        green_led.on()
        red_led.off()
        buzzer.off()

    time.sleep(1)  # Check every second