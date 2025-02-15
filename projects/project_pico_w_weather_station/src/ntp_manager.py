"""
ntp_manager - Set RTC time using NTP Servers
"""

import socket
import struct
import time
import machine


NTP_DELTA = 2208988800  # Difference between NTP epoch and Unix epoch
NTP_SERVER = "pool.ntp.org"
NTP_PORT = 123

BULGARIA_STANDARD_OFFSET = 2 * 3600
BULGARIA_DST_OFFSET = 3 * 3600


def get_ntp_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B  # NTP request header

    addr = socket.getaddrinfo(NTP_SERVER, NTP_PORT)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)

    try:
        s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        ntp_seconds = struct.unpack("!I", msg[40:44])[0]
        epoch_time = ntp_seconds - NTP_DELTA
        return epoch_time
    except Exception as e:
        print(f"NTP request failed: {e}")
        return None
    finally:
        s.close()


def set_pico_rtc():
    epoch_time = get_ntp_time()
    if epoch_time:
        tm = time.localtime(epoch_time)
        rtc = machine.RTC()
        rtc.datetime(
            (
                tm[0],  # year
                tm[1],  # month
                tm[2],  # day
                tm[6],  # weekday (0 = Monday, 6 = Sunday)
                tm[3],  # hour
                tm[4],  # minute
                tm[5],  # second
                0,      # subseconds (not used)
            )
        )
        print("RTC set to:", rtc.datetime())
        return True
    else:
        print("Failed to get time from NTP")
        return False


def is_dst(year, month, day):
    """Return True if date is in DST period in Bulgaria."""
    from time import mktime, localtime
    last_sunday_march = max(
        day for day in range(25, 32)
        if localtime(mktime((year, 3, day, 0, 0, 0, 0, 0)))[6] == 6
    )
    last_sunday_october = max(
        day for day in range(25, 32)
        if localtime(mktime((year, 10, day, 0, 0, 0, 0, 0)))[6] == 6
    )
    dst_start = (year, 3, last_sunday_march)
    dst_end = (year, 10, last_sunday_october)
    current = (year, month, day)

    return dst_start <= current < dst_end


def get_bulgaria_time():
    utc_time = time.time()
    local_time_tuple = time.localtime(utc_time)
    year, month, day = local_time_tuple[0:3]

    if is_dst(year, month, day):
        offset = BULGARIA_DST_OFFSET
    else:
        offset = BULGARIA_STANDARD_OFFSET

    local_time = time.localtime(utc_time + offset)

    # Return formatted string like datetime.strftime("%Y-%m-%d %H:%M:%S")
    date_time_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5]
    )

    return date_time_str