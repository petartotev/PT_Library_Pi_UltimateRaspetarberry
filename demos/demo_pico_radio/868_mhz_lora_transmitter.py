from ulora import LoRa
from machine import Pin, SPI
import time

# Initialize SPI
spi = SPI(0, baudrate=5000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# Initialize LoRa
lora = LoRa(spi, cs=Pin(17), reset=Pin(21), irq=Pin(20))
lora.set_frequency(868000000)  # Set frequency to 868 MHz

while True:
    message = 'Hello, world'
    lora.send(message)
    print(f'Sent: {message}')
    time.sleep(2)