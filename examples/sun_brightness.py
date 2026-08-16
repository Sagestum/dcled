#!/usr/bin/env python3
# Prints "1" during the day and "0" at night (before sunrise / after sunset),
# for use as a dcled --brightness value. Pure stdlib, no internet/network
# access, no external packages required.
#
# Sunrise equation: https://en.wikipedia.org/wiki/Sunrise_equation

import math
from datetime import datetime, timezone

# Standort: Bad Salzuflen - fuer euren Standort anpassen.
LAT = 52.0833
LON = 8.7667


def sun_times_utc(now_utc):
    y, m, d = now_utc.year, now_utc.month, now_utc.day
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    jdn = d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045
    n = jdn - 2451545.0 + 0.0008

    j_star = n - LON / 360.0
    mean_anomaly = math.radians((357.5291 + 0.98560028 * j_star) % 360)
    center = (1.9148 * math.sin(mean_anomaly)
              + 0.0200 * math.sin(2 * mean_anomaly)
              + 0.0003 * math.sin(3 * mean_anomaly))
    ecliptic_lon = math.radians((math.degrees(mean_anomaly) + 102.9372 + center + 180) % 360)
    j_transit = (2451545.0 + j_star
                 + 0.0053 * math.sin(mean_anomaly)
                 - 0.0069 * math.sin(2 * ecliptic_lon))

    sin_dec = math.sin(ecliptic_lon) * math.sin(math.radians(23.4397))
    phi = math.radians(LAT)
    cos_hour_angle = ((math.sin(math.radians(-0.833)) - math.sin(phi) * sin_dec)
                       / (math.cos(phi) * math.sqrt(1 - sin_dec ** 2)))
    cos_hour_angle = max(-1.0, min(1.0, cos_hour_angle))
    hour_angle = math.degrees(math.acos(cos_hour_angle))

    return (_jd_to_datetime(j_transit - hour_angle / 360.0),
            _jd_to_datetime(j_transit + hour_angle / 360.0))


def _jd_to_datetime(jd):
    jd2 = jd + 0.5
    z = int(jd2)
    f = jd2 - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day_frac = b - d - int(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    day = int(day_frac)
    hours = (day_frac - day) * 24
    hour = int(hours)
    minutes = (hours - hour) * 60
    minute = int(minutes)
    second = int(round((minutes - minute) * 60))
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    sunrise, sunset = sun_times_utc(now)
    print(0 if (now < sunrise or now > sunset) else 1)
