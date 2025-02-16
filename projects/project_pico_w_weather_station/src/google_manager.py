"""
google_manager - Send data to Google Sheets
"""

import urequests
import ujson
import secrets


headers = {'Content-Type': 'application/json'}

test_data = {'pm25': 61.14, 'density': 'Unhealthy!', 'date': '2025-02-15 21:58:16', 'temperature': 23.2, 'humidity': 56.5}

def send_data(data):
    data_sent_successfully = True
    error_msg = ''
    print(data)
    response = urequests.post(secrets.GOOGLE_URL, data=ujson.dumps(data), headers=headers)
    print(response.text)
    if ('after property value in JSON at position' in response.text):
        # Empirically it is known that once we get an error containing the above substring, data does not reach Google Sheets.
        data_sent_successfully = False
        error_msg = '...after property value in JSON at position'
    if ('The server encountered a temporary error and could not complete your request.' in response.text):
        data_sent_successfully = False
        error_msg = 'The server encountered a temporary error and could not complete your request.'
        
    response.close()
    return data_sent_successfully, error_msg

