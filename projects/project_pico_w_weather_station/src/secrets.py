import ubinascii

SSID = ubinascii.a2b_base64('encoded-base64-SSID').decode()
PASSWORD = ubinascii.a2b_base64('encoded-base64-PASSWORD').decode()