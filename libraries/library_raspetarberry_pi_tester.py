import raspetarberryPiLibDHT11
import raspetarberryPiLibLCD

# raspetarberryPiLibDHT11

tem = raspetarberryPiLibDHT11.getTemperature()
print("Temperature: " + tem + "°C")

hum = raspetarberryPiLibDHT11.getHumidity()
print("Humidity: " + hum + "%")

humid, temp = raspetarberryPiLibDHT11.getBoth()
print("Humidity: " + humid + "%")
print("Temperature: " + temp + "°C")

# raspetarberryPiLibDHT11.printTemperatureAndHumidityForever()

# raspetarberryPiLibLCD

raspetarberryPiLibLCD.displayTest()
