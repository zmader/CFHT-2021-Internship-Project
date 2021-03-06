from multiprocessing import Value
import astropy
import astroplan
import datetime
from astroplan.constraints import Constraint, is_observable
from astroplan import target, observability_table, Observer, moon, AltitudeConstraint, AirmassConstraint, AtNightConstraint
from astroplan.target import FixedTarget
from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
from astropy.table import Table
from datetime import datetime, timedelta, date
from astropy.units.cgs import C
from dateutil import tz
from astroplan.plots import plot_airmass
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import sys

TIMEZONE = tz.gettz() #need this because to_datetime will print UTC without any extra timezone info
CFHT_SITE = Observer.at_site("cfht")
constraints = [AltitudeConstraint(10*u.deg, 80*u.deg), AirmassConstraint(2), AtNightConstraint.twilight_civil()]

# get_start_date()
#
# Description: Prompt for the starting date and do some error checking
#
# Parameters: none
#
# Return: Time (starting observation date)
#
def get_start_date():
    todayDate = None
    try:
        todayDate = sys.argv[1] #this would eventually be able to be changed to a time range for multiple days of viewing
        if not todayDate:
            raise ValueError("empty string")
    except ValueError as e:
        todayDate = datetime.today().strftime('%Y-%m-%d')

    time = Time('%s 19:00:00' % todayDate) #time is 4pm HST which should work as long as the sun doesn't suddenly start setting before then

    return time

# get_end_date()
#
# Description: Prompt for the ending date and do some error checking
#
# Parameters: none
#
# Return: Time (starting observation date)
#
def get_end_date():
    endDate = None

    #needs an error check for dates before the start date
    try:
        endDate = sys.argv[2] #this would eventually be able to be changed to a time range for multiple days of viewing
        if not endDate:
            raise ValueError("empty string")
    except ValueError as e:
        endDate = datetime.today().strftime('%Y-%m-%d')

    time = Time('%s 19:00:00' % endDate) #time is 4pm HST which should work as long as the sun doesn't suddenly start setting before then

    return time

# calculate_time_visible()
#
# Description: calculates the time an object will be visible, for one night
#
# Parameters:   timeStart - time
#               dec - float
#               ra - float
#               target - [FixedTarget]
#
# Return: timeDelta (??) (hours the object is observable)
#
def calculate_time_visible(timeStart, target):
    #find sunset/sunrise
    sunSet = CFHT_SITE.sun_set_time(timeStart, which="next").to_datetime(TIMEZONE)
    sunRise = CFHT_SITE.sun_rise_time(timeStart, which="next").to_datetime(TIMEZONE)
    timeRange=Time([sunSet, sunRise])

    #grab object observability table
    #if observability table is used instead of a function call, some math can be done pretty easily to determine the time observable
    observability = observability_table(constraints, CFHT_SITE, target, time_range=timeRange)
    percentOfTimeVisible = observability[0][3]
    nightLength = sunRise - sunSet
    timeObservable = nightLength * percentOfTimeVisible

    return timeObservable

# calculate_time_over_range()
#
# Description: calculates the time an object will be visible, for a range of nights
#
# Parameters: none
#
# Return: timeDelta (??) (hours the object is observable)
#
def calculate_time_over_range(start, end, dec, ra):
    objectCoords = SkyCoord(ra=(ra*u.deg), dec=(dec*u.deg))
    target = [FixedTarget(coord=objectCoords, name="target1")]
    totalVisibilityTime = calculate_time_visible(start, target)
    #plot_airmass(target, CFHT_SITE, start)
    #plt.show()
    while start < end: #calculate from start to end
        #add one day of time to the start date
        start = start + timedelta(days=1)
        totalVisibilityTime = totalVisibilityTime + calculate_time_visible(start, target)
    return totalVisibilityTime

# get_right_ascension()
#
# Description: Get data for the right ascension of the desired object
#
# Parameters: none
#
# Return: float 
#
def get_right_ascension():
    ra = None
    try:
        ra = float(sys.argv[3])
        if not ra:
            raise ValueError("empty string")
        elif ra > 360 or ra < 0:
            raise ValueError("right ascension out of bounds")
    except ValueError as e:
        ra = 0

    return ra

# get_declination()
#
# Description: Get data for the declination of the desired object
#
# Parameters: none
#
# Return: float 
#
def get_declination():
    dec = None
    try:
        dec = float(sys.argv[4])
        if not dec:
            raise ValueError("empty string")
        elif dec > 90 or dec < -90:
            raise ValueError("declination out of bounds")
    except ValueError as e:
        dec = 0

    return dec

# main()
#
# Description: Main function to calculate the object visibility
#
# Parameters: none
#
# Return: void
#
# WORK TO DO:   Segment main into smaller functions
def main():

    timeStart = get_start_date()
    timeEnd = get_end_date()

    #error check for end earlier than start
    if timeEnd < timeStart:
        timeEnd = timeStart

    rightAscension = get_right_ascension()
    declination = get_declination()

    #can now make a second function that can iterate through a bunch of calculate_time_visible() calls to get longer periods
    timeObservable = calculate_time_over_range(timeStart, timeEnd, declination, rightAscension)

    print("Total time of object observability: ", timeObservable)

    return

main()