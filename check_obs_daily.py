#using tuples to hold the values for declination, right alignment
from collections import namedtuple
#to use for calculating time since default date
from datetime import date, datetime

#tuples to hold min/max measurements or coordinates
#to change the value of a specific element, use ****._replace(field=val)

#the declination max value will always be +90
declination = namedtuple("declination", "min max")
declinationRange = namedtuple("declinationRange", "upperBound lowerBound") #will hold a declination object for each bound
celestialCoord = namedtuple("celestialCoord", "declination alignment")
skybox = namedtuple("skybox", "pos80 pos60 pos40 pos20 zero neg20 neg40 neg60 neg80")

#some global variables
DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0, 0, None) #will need to edit this once I adjust the skybox to a new default position



# check_valid_coords(celestialObject, visibleArea)
#
# Description: The function compares the coordinates of a celestial object to the
#              visible sky and determines if the given object is visible at that time.
#
# Parameters: celestialObject   - celestialCoord object
#             visibleArea       - skybox object
#
# Return: none
#
def check_valid_coords(celestialObject, visibleArea):
    declinationRange = find_declination_range(celestialObject.declination, visibleArea)
    #print check to see if the ranges are correct
    print(declinationRange.upperBound.min)
    print(declinationRange.upperBound.max)
    print(declinationRange.lowerBound.min)
    print(declinationRange.lowerBound.max)
    #adjust the ranges to estimate a range for the objects specific declination
    adjustedRange = adjust_to_object_declination(celestialObject.declination, declinationRange)
    #check if the right alignment of the object falls within the given range
    isInRange = check_if_in_range(celestialObject.alignment, adjustedRange)
    if isInRange:
        print("The object is in range")
    else:
        print("The object is not in range")


# check_if_in_range(objectAlignment, adjustedRange)
#
# Description: The function takes a celestial objects alignment and compares it
#              to the visible range of alignment at the objects declination.
#
# Parameters: objectAlignment   - float or int
#             adjustedRange     - declination object
#
# Return: boolean (true if in range, false if not)
#
def check_if_in_range(objectAlignment, adjustedRange):
    #needs to be able to check if the min range > max since it goes continuously
    if adjustedRange.min > adjustedRange.max:
        #this only works for max < min. gives incorrect value for max > min
        if objectAlignment >= adjustedRange.min or objectAlignment <= adjustedRange.max:
            return True
        else:
            return False
    else:
        #this returns correct value for max > min
        if objectAlignment >= adjustedRange.min and objectAlignment <= adjustedRange.max:
            return True
        else:
            return False


# adjust_to_object_declination(objDec, estimatedRange)
#
# Description: The function takes an objects declination and determines
#              the visible range for that specific declination by estimating
#              the maximum and minimum right alignment at the objects declination.
#
# Parameters: objDec            - float or int
#             estimatedRange    - declinationRange object
#
# Return: declination object
#
def adjust_to_object_declination(objDec, estimatedRange):
    #do some midpoint stuff between the two mins and maxes to get a better estimate of the visible range
    #determine the length of the max values, will also need to adjust length to account for one value passing 360
    #seems to be working for minimum values
    minRange = estimatedRange.upperBound.min - estimatedRange.lowerBound.min
    minValue = (estimatedRange.lowerBound.min + (minRange * ((objDec%20)/20))) % 360
    print(minRange)
    print(minValue)
    #find the adjustment needed for the max
    #I need to test this a bit more to make sure it works with edge cases
    maxRange = estimatedRange.lowerBound.max - estimatedRange.upperBound.max
    diff = (maxRange * (objDec % 20)) / 20
    maxValue = estimatedRange.upperBound.max + (maxRange - diff)
    print(maxRange)
    print(maxValue)
    adjustedRange = declination(minValue, maxValue)
    
    return adjustedRange

# find_declination_range(objDec, visibleArea)
#
# Description: The function takes the objects declination bounds it by
#              two known declinations.
#
# Parameters: objDec            - float or int
#             visibleArea       - skybox object
#
# Return: declinationRange object
#
def find_declination_range(objDec, visibleArea):
    if objDec > 60:
        decRange = declinationRange(visibleArea.pos80, visibleArea.pos60)
        return decRange
    elif objDec > 40:
        decRange = declinationRange(visibleArea.pos60, visibleArea.pos40)
        return decRange
    elif objDec > 20:
        decRange = declinationRange(visibleArea.pos40, visibleArea.pos20)
        return decRange
    elif objDec > 0:
        decRange = declinationRange(visibleArea.pos20, visibleArea.zero)
        return decRange
    elif objDec > -20:
        decRange = declinationRange(visibleArea.zero, visibleArea.neg20)
        return decRange
    elif objDec > -40:
        decRange = declinationRange(visibleArea.neg20, visibleArea.neg40)
        return decRange
    elif objDec > -60:
        decRange = declinationRange(visibleArea.neg40, visibleArea.neg60)
        return decRange
    else:
        decRange = declinationRange(visibleArea.neg60, visibleArea.neg80)
        return decRange
    
# create_default_skybox()
#
# Description: The function creates the visible area of the sky by creating right
#              alignment ranges for preset declinations. The function also rotates
#              the sky by the modifier, and then normalizes the values to fit on
#              a scale from 0 to 360 degrees
#
# Parameters: modifier  - float or int
#
# Return: skybox object
#
def create_default_skybox(modifier):
    pos80 = declination((0 + modifier) % 360, (360 + modifier) % 360)
    pos60 = declination((318.75 + modifier) % 360, (221.25 + modifier) % 360)
    pos40 = declination((288.75 + modifier) % 360, (251.25 + modifier) % 360)
    pos20 = declination((277.5 + modifier) % 360, (262.5 + modifier) % 360)
    zero = declination((0 + modifier) % 360, (180 + modifier) % 360)
    neg20 = declination((82.5 + modifier) % 360, (97.5 + modifier) % 360)
    neg40 = declination((71.25 + modifier) % 360, (108.75 + modifier) % 360)
    neg60 = declination((48.75 + modifier) % 360, (131.25 + modifier) % 360)
    neg80 = declination(0, 0)
    visibleArea = skybox(pos80, pos60, pos40, pos20, zero, neg20, neg40, neg60, neg80)
    return visibleArea

# get_degree_modifier_from_date(dateEnd)
#
# Description: The function calculates by how much the sky will need to rotate in
#              order for it to accurately mirror the sky at a specific day
#
# Parameters: dateEnd           - datetime object from datetime library
#
# Return: int or float
#
def get_degree_modifier_from_date(dateEnd):
    #use date library
    daysSince = dateEnd - DEFAULT_DATE
    print(daysSince.days)
    #create a modifier that is passed to create_default_skybox() where each degree is shifted up by the modifier then modded
    #for each day, add 1 degree
    #for each extra hour, add 15 degrees
    degreeShift = (daysSince.days * 1) + ((daysSince.seconds / 3600) * 15)
    #return degreeShift (add back in after more testing with the default values)
    return 0


#main
#set up default declination lines which hold the right alignment range
#for now I am using default values that assume that the right alignment of declination 0 is 0 to 180 degrees
celestialObject = celestialCoord(-45, 250)
currentDate = datetime(2000, 1, 2, 0, 0, 0, 0, None)
modifier = get_degree_modifier_from_date(currentDate)
visibleArea = create_default_skybox(modifier)

#will need to adjust for rotation over time, will estimate visible time by checking each hour
check_valid_coords(celestialObject, visibleArea)
