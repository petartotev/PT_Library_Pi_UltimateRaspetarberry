"""
secrets - Stores secrets used for Wi-Fi connection etc.
"""

import ubinascii

SSID = ubinascii.a2b_base64('VklWQUNPTV9GaWJlck5ldF8xQTM3').decode()
PASSWORD = ubinascii.a2b_base64('bVJ5N1h2YWhYNQ==').decode()
GOOGLE_URL = 'https://script.google.com/macros/s/AKfycbzQUlpGJ-wphiqX3pmNd7lQu4ZoWWU28E1i7LEv3jIOKp7c43NpBhg2SqIANesBV-Oisw/exec'