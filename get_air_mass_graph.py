import sys
from astroplan.plots import plot_airmass
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from astroplan import target,  Observer, AltitudeConstraint, AirmassConstraint, AtNightConstraint
from datetime import datetime
from astropy.time import Time
import astropy.units as u
from astroplan.target import FixedTarget
from astropy.coordinates import SkyCoord

CFHT_SITE = Observer.at_site("cfht")
constraints = [AltitudeConstraint(10*u.deg, 80*u.deg), AirmassConstraint(2), AtNightConstraint.twilight_civil()]

def get_date():
    todayDate = None
    try:
        todayDate = sys.argv[1]
        if not todayDate:
            raise ValueError("empty string")
    except ValueError as e:
        todayDate = datetime.today().strftime('%Y-%m-%d')

    time = Time('%s 19:00:00' % todayDate) #time is 4pm HST which should work as long as the sun doesn't suddenly start setting before then

    return time

date = get_date()
ra = float(sys.argv[2])
dec = float(sys.argv[3])
objectCoords = SkyCoord(ra=(ra*u.deg), dec=(dec*u.deg))
target = [FixedTarget(coord=objectCoords, name="target1")]
plot_airmass(target, CFHT_SITE, date)
plt.show()
