"""
wifi_manager - Connect Raspberry Pico W to Wi-Fi
"""

import network
import secrets
import time


def connect_to_wifi():
    """
    Connects the Raspberry Pi Pico to a Wi-Fi network using credentials from secrets.py.

    Returns:
        bool: True if connected successfully, False otherwise.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    max_attempts = 10
    attempt = 0

    while not wlan.isconnected() and attempt < max_attempts:
        print(f"Attempt {attempt + 1} to connect...")
        attempt += 1
        time.sleep(2)

    return wlan.isconnected()
