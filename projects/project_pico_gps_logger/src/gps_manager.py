# -*- coding:utf-8 -*-

import time
import math
import hashlib
import l76x
from micropyGPS.micropyGPS import MicropyGPS

# define the UART number and its baudrate , when UARTx is 1 please solder the UART1 0R resistor on Pico-GPS-L76B board
# UARTx = 1
UARTx = 0

# define the rp2040 uart baudrate , the default baudrate is 9600 of L76B 
BAUDRATE = 115200

# make an object of gnss device , the default uart is UART0 and its baudrate is 9600bps
gnss_l76b=l76x.L76X(uartx=UARTx,_baudrate = BAUDRATE)

# exit the backup mode when start
gnss_l76b.l76x_exit_backup_mode()

# enable/disable sync PPS when NMEA output
'''
optional:
SET_SYNC_PPS_NMEA_ON
SET_SYNC_PPS_NMEA_OFF
'''
gnss_l76b.l76x_send_command(gnss_l76b.SET_SYNC_PPS_NMEA_ON)


# make an object of NMEA0183 sentence parser
"""
Setup GPS Object Status Flags, Internal Data Registers, etc
local_offset (int): Timzone Difference to UTC
location_formatting (str): Style For Presenting Longitude/Latitude:
                           Decimal Degree Minute (ddm) - 40° 26.767′ N
                           Degrees Minutes Seconds (dms) - 40° 26′ 46″ N
                           Decimal Degrees (dd) - 40.446° N
"""
parser = MicropyGPS(location_formatting='dd')

sentence = ''

def print_gps_location_forever():
    while True:
        if gnss_l76b.uart_any():
            sentence = parser.update(chr(gnss_l76b.uart_receive_byte()[0]))
            if sentence:
                print('WGS84 Coordinate:Latitude(%c),Longitude(%c) %.9f,%.9f'%(parser.latitude[1],parser.longitude[1],parser.latitude[0],parser.longitude[0]))
                print('copy WGS84 coordinates and paste it on Google map web https://www.google.com/maps')
                
                gnss_l76b.wgs84_to_bd09(parser.longitude[0],parser.latitude[0])
                print('Baidu Coordinate: longitude(%c),latitudes(%c) %.9f,%.9f'%(parser.longitude[1],parser.latitude[1],gnss_l76b.Lon_Baidu,gnss_l76b.Lat_Baidu))
                print('copy Baidu Coordinate and paste it on the baidu map web https://api.map.baidu.com/lbsapi/getpoint/index.html')
                
                print('UTC Timestamp:%d:%d:%d'%(parser.timestamp[0],parser.timestamp[1],parser.timestamp[2]))
            
                # print fix status
                '''
                1 : NO FIX
                2 : FIX 2D
                3 : FIX_3D
                '''
                print('Fix Status:', parser.fix_stat)
                
                print('Altitude:%d m'%(parser.altitude))
                print('Height Above Geoid:', parser.geoid_height)
                print('Horizontal Dilution of Precision:', parser.hdop)
                print('Satellites in Use by Receiver:', parser.satellites_in_use)
                print('')

def get_gps_location():
    latitude = 0
    longitude = 0
    altitude = 0
    while True:
        if gnss_l76b.uart_any():
            sentence = parser.update(chr(gnss_l76b.uart_receive_byte()[0]))
            if sentence:
                str_lat_lon = 'WGS84_Coordinate:Latitude(%c),Longitude(%c) %.9f,%.9f'%(parser.latitude[1],parser.longitude[1],parser.latitude[0],parser.longitude[0])
                str_lat_lon_split = str_lat_lon.split(' ')[1].split(',')
                latitude = str_lat_lon_split[0] + '%c'%(parser.latitude[1])
                longitude = str_lat_lon_split[1] + '%c'%(parser.longitude[1])
                str_altitude = 'Altitude:%d'%(parser.altitude)
                altitude = str_altitude.split(':')[1]
                print(latitude + ", " + longitude + ", " + altitude)
                return latitude, longitude, altitude

#get_gps_location()