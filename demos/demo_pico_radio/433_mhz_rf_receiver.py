from rpi_rf import RFDevice

rfdevice = RFDevice(27)  # GPIO 27 for RX
rfdevice.enable_rx()

print("Listening for signals...")

while True:
    if rfdevice.rx_code_timestamp:
        print(f"Received: {rfdevice.rx_code}")
        rfdevice.rx_code_timestamp = None