

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

TIMEZONE = tz.gettz() #need this because to_datetime will print UTC without any extra timezone info
CFHT_SITE = Observer.at_site("cfht")
constraints = [AltitudeConstraint(10*u.deg, 80*u.deg), AirmassConstraint(5), AtNightConstraint.twilight_civil()]

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
        todayDate = input("Enter todays date (YYYY-MM-DD): ") #this would eventually be able to be changed to a time range for multiple days of viewing
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
        endDate = input("Enter todays date (YYYY-MM-DD): ") #this would eventually be able to be changed to a time range for multiple days of viewing
        if not endDate:
            raise ValueError("empty string")
    except ValueError as e:
        todayDate = datetime.today().strftime('%Y-%m-%d')

    time = Time('%s 19:00:00' % todayDate) #time is 4pm HST which should work as long as the sun doesn't suddenly start setting before then

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
def calculate_time_visible(timeStart, dec, ra, target):
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

    print("Sunset at: ", sunSet)
    print("Sunrise at: ", sunRise)
    print("Length of night: ", nightLength)

    return timeObservable

# calculate_time_over_range()
#
# Description: calculates the time an object will be visible, for a range of nights
#
# Parameters: none
#
# Return: timeDelta (??) (hours the object is observable)
#
def calculate_time_over_range():
    #while start < end
    #add calculate_time_visible() to sum
    #add one day of time to the start date
    return

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
        ra = float(input("Enter the right ascension of the desired object (degrees): "))
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
        dec = float(input("Enter the declination of the desired object (degrees): "))
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
    timeEnd = get_end_date() #not used yet
    rightAscension = get_right_ascension()
    declination = get_declination()

    objectCoords = SkyCoord(ra=(rightAscension*u.deg), dec=(declination*u.deg))
    target = [FixedTarget(coord=objectCoords, name="target1")]

    #can now make a second function that can iterate through a bunch of calculate_time_visible() calls to get longer periods
    timeObservable = calculate_time_visible(timeStart, declination, rightAscension, target)

    print("Length of observability: ", timeObservable)

    return

main()