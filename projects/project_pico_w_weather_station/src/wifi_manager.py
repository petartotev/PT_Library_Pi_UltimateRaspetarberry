"""
wifi_manager - Connect Raspberry Pico W to Wi-Fi
"""

import network
import secrets
import time
import socket


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


def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Returns True if the device can connect to the specified host/port, False otherwise.
    Default host is Google's public DNS server.
    """
    try:
        socket.setdefaulttimeout(timeout)
        # Attempt to create a socket connection to the host/port.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except OSError:
        return False

#if is_connected():
#    print("Connected to the Internet")
#else:
#    print("Not connected to the Internet")