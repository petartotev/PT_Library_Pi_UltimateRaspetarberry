from ulora import LoRa
from machine import Pin, SPI
import time

spi = SPI(0, baudrate=5000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

lora = LoRa(spi, cs=Pin(17), reset=Pin(21), irq=Pin(20))
lora.set_frequency(868000000)  # Use 868 MHz

while True:
    # Send a message
    message = "Ping!"
    lora.send(message)
    print(f"Sent: {message}")
    
    # Wait for a response
    time.sleep(1)
    if lora.received_packet():
        response = lora.receive()
        print(f"Received: {response}")
    
    time.sleep(2)