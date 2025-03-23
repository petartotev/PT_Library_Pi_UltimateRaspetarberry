from time import sleep

class LCD1602:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        self._send_command(0x33)  # Initialize LCD
        self._send_command(0x32)  # Set to 4-bit mode
        self._send_command(0x28)  # 2-line, 5x8 dots
        self._send_command(0x0C)  # Display on, cursor off
        self._send_command(0x06)  # Auto increment cursor
        self._send_command(0x01)  # Clear screen
        sleep(0.005)  # Delay for LCD startup

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytearray([data | 0x08]))  # Enable backlight
        self.i2c.writeto(self.addr, bytearray([data | 0x0C]))  # Enable high
        sleep(0.002)
        self.i2c.writeto(self.addr, bytearray([data | 0x08]))  # Enable low

    def _send_command(self, cmd):
        self._write_byte(cmd & 0xF0)
        self._write_byte((cmd << 4) & 0xF0)

    def _send_data(self, data):
        self._write_byte((data & 0xF0) | 0x01)
        self._write_byte(((data << 4) & 0xF0) | 0x01)

    def clear(self):
        self._send_command(0x01)  # Clear display
        sleep(0.005)

    def print(self, text):
        for char in text:
            self._send_data(ord(char))

    def setCursor(self, col, row):
        addr = 0x80 + col + (0x40 * row)
        self._send_command(addr)

