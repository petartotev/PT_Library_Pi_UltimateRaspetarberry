from rpi_rf import RFDevice
import time

rfdevice = RFDevice(17)  # GPIO 17 for TX
rfdevice.enable_tx()

numbers = [1, 2, 3, 5, 7, 11, 13]

for num in numbers:
    rfdevice.tx_code(num)  # Transmit the number
    print(f"Sent: {num}")
    time.sleep(1)

rfdevice.cleanup()