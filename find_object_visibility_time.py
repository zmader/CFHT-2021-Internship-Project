

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

# main()
#
# Description: Main function to calculate the object visibility
#
# Parameters: none
#
# Return: void
#
def main():
    #grab object coordinates and date
    todayDate = None
    try:
        todayDate = input("Enter todays date (YYYY-MM-DD): ") #this would eventually be able to be changed to a time range for multiple days of viewing
        if not todayDate:
            raise ValueError("empty string")
    except ValueError as e:
        todayDate = datetime.today().strftime('%Y-%m-%d')

    time = Time('%s 19:00:00' % todayDate) #time is 4pm HST which should work as long as the sun doesn't suddenly start setting before then

    #add checks for these so that if empty, just asks again
    rightAscension = float(input("Enter the right ascension of the desired object (degrees): ")) #for now to be read in degrees
    declination = float(input("Enter the declination of the desired object: "))

    objectCoords = SkyCoord(ra=(rightAscension*u.deg), dec=(declination*u.deg))
    target = [FixedTarget(coord=objectCoords, name="target1")]

    #find sunset/sunrise
    sunSet = CFHT_SITE.sun_set_time(time, which="next").to_datetime(TIMEZONE)
    sunRise = CFHT_SITE.sun_rise_time(time, which="next").to_datetime(TIMEZONE)
    timeRange=Time([sunSet, sunRise])

    #grab object observability table
    #if observability table is used instead of a function call, some math can be done pretty easily to determine the time observable
    observability = observability_table(constraints, CFHT_SITE, target, time_range=timeRange)
    percentOfTimeVisible = observability[0][3]
    nightLength = sunRise - sunSet
    timeObservable = nightLength * percentOfTimeVisible

    #since observability is type ndarray, [x] is needed to access the specific target
    #print(observability)

    print("Sunset at: ", sunSet)
    print("Sunrise at: ", sunRise)
    print("Length of night: ", nightLength)
    #print moon rise, set, brightness. Can pull from determine_sun_moon_time
    print("Length of observability: ", timeObservable)

    #can create a visibility table by evaluating is_observable over a time range(will reduce speed by a lot though)
    
    #eventually to return relevant info as some type of structure
    return

main()