import network, time
from config import WIFI_SSID, WIFI_PASSWORD

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        start = time.time()
        while not wlan.isconnected() and (time.time() - start) < 10:
            time.sleep(1)
    return wlan
