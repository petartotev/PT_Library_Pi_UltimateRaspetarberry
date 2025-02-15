"""
google_manager - Send data to Google Sheets
"""

import urequests
import ujson
import secrets


headers = {'Content-Type': 'application/json'}


def send_data(data):
    print(data)
    response = urequests.post(secrets.GOOGLE_URL, data=ujson.dumps(data), headers=headers)
    print(response.text)
    response.close()
