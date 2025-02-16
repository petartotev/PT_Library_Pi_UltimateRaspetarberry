"""
dust_manager - Dust Sensor Sharp GP2Y1010AU0F
Module reads particulate matter (PM2.5) density and provides air quality evaluation based on EPA AQI standards.
"""

from machine import Pin, ADC
import utime


# Select ADC input 0 (GPIO26)
COV_RATIO     =  0.2 #ug/mmm / mv
NO_DUST_VOLTAGE = 400  #mv
SYS_VOLTAGE = 3300


class Dust:
    """
    Represents the Sharp GP2Y1010AU0F Dust Sensor.
    Handles reading and filtering ADC values for PM2.5 density measurement.
    """
    def __init__(self):
         # Select ADC input 0 (GPIO26)
        self.ADC_ConvertedValue = ADC(0)
        self.DIN = Pin(22,Pin.OUT)
        self.conversion_factor = 3.3 / (65535)
        self.flag_first = 0
        self.buff = [0,0,0,0,0,0,0,0,0,0]
        self.sum1 = 0
    def Filter(self,ad_value):      
        buff_max = 10
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range (buff_max):
                self.buff[i] = ad_value
                self.sum1 = self.sum1+self.buff[i]
            return ad_value
        else:
            self.sum1 = self.sum1-self.buff[0]
            for i in range (buff_max-1):
                self.buff[i] = self.buff[i+1]
            self.buff[9] = ad_value
            self.sum1 = self.sum1 + self.buff[9]
            i = self.sum1 / 10.0
            return i


def get_air_quality_particulate_matter():
    """Function gets particulate matter PM2.5 density value from dust sensor."""
    Dust.DIN.value(1 )
    utime.sleep_us(280) # didn't work with time.sleep(280 / 1_000_000) - resulted in 0 | G(ood)
    AD_value = Dust.ADC_ConvertedValue.read_u16()
    Dust.DIN.value(0)
    AD_value = Dust.Filter(AD_value)
    voltage = (SYS_VOLTAGE / 65536.0) * AD_value * 11
    if voltage >= NO_DUST_VOLTAGE:
        voltage = voltage - NO_DUST_VOLTAGE
        density = voltage * COV_RATIO
    else:
        density = 0     
    utime.sleep(1)
    return density


def get_air_quality_index_evaluation(density):
    """
    Evaluates air quality based on PM2.5 density using EPA AQI standards.

    Args:
        density (float): PM2.5 density in µg/m³.

    Returns:
        str: Air quality description.
    """
    if density is None: # Unknown
        return "?"
    
    density = float(density)
    
    if 0 <= density <= 9.0:
        return "Good"
    if 9.0 < density <= 35.4:
        return "Moderate"
    if 35.4 < density <= 55.4:
        return "Unhealthy for SG" # Unhealthy for Sensitive Groups
    if 55.4 < density <= 125.4:
        return "Unhealthy!"
    if 125.4 < density <= 225.4:
        return "Very Unhealthy!!"
    if 225.4 < density <= 500:
        return "Hazardous!!!"

    return "?"


def get_data_from_dust_sensor():
    """
    Reads PM2.5 density from the dust sensor and evaluates air quality.

    Returns:
        tuple: (density, evaluation) - PM2.5 density (float) and air quality evaluation (str).
    """
    p_m = round(get_air_quality_particulate_matter(), 1)
    evaluation = get_air_quality_index_evaluation(p_m)
    return p_m, evaluation


Dust=Dust()