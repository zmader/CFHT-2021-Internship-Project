
import astropy
import astroplan
from astroplan import Observer, moon
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
from datetime import datetime, timedelta
from astropy.units.cgs import C
from dateutil import tz

TIMEZONE = tz.gettz('HST') #need this because to_datetime will print UTC without any extra timezone info
CFHT_SITE = Observer.at_site(site_name="cfht", timezone="US/Pacific")


#main

todayDate = input("Enter todays date (YYYY-MM-DD): ")
time = Time('%s 20:00:00' % todayDate) #needs to be daytime in hawaii in UTC to get correct set and rise times for that day
sunSet = CFHT_SITE.sun_set_time(time, which="next")
sunRise = CFHT_SITE.sun_rise_time(time, which="next")
moonRise = CFHT_SITE.moon_rise_time(time, which="next")
moonSet = CFHT_SITE.moon_set_time(time, which="next")
nightLength = sunRise - sunSet

#this section converts the TimeDelta object into 3 ints for hours/minutes/seconds
nightLength = nightLength.datetime.total_seconds()
hours = int(nightLength/3600)
nightLength = nightLength - (hours * 3600)
minutes = int(nightLength/60)
nightLength = nightLength - (minutes * 60)
seconds = int(nightLength)

print("Sun sets at: ", (sunSet.to_datetime(TIMEZONE).time()))
print("Sun rises at: ", (sunRise.to_datetime(TIMEZONE).time()))
print("Night length: %02d:%02d:%02d" % (hours, minutes, seconds)) #need to figure out how to set input to have 0X if single digit
print("Moon rises at: ", moonRise.to_datetime(TIMEZONE).time())
print("Moon sets at: ", moonSet.to_datetime(TIMEZONE).time()) 

#moon phase info??
moonPhase = moon.moon_phase_angle(time)
moonIllu = moon.moon_illumination(time)
print("Moon phase in radians: ", moonPhase)
print("Moon illumination: ", moonIllu)