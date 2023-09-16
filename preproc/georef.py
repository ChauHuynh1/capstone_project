from math import atan2, atan, asin, tan, cos, sin, sqrt, pi, radians
import cv2
import numpy
import re

# Function for geo-tagging
# Input: image name, image's latitude, longitude, and altitude;
# image's orientation i.e., kappa angle, & pixel coordinates for geo-tagging (row, column)
# Output: GPS coordinates at the specified pixel
def geoTag(file,lat,long,alt,kappa,row,column):
    # Read image file
    #file = 'snap_1_ (44).jpg'
    im = cv2.imread(file)
    width = im.shape[1]
    height = im.shape[0]
    #exif = Image.open(file)._getexif()

    # Extract GPS data
    #lat = float(exif[34853][2][0]+exif[34853][2][1]/60+exif[34853][2][2]/3600)
    #long = float(exif[34853][4][0]+exif[34853][4][1]/60+exif[34853][4][2]/3600)
    #alt = exif[34853][6]

    # Calculate camera's parameter and pixel size
    f = 35 # focal length in mm
    res = 96 # horizontal and vertical resolution in dpi
    mpd = 1/res*25.4 # mm per pixel
    Sw = mpd*width # Thermal sensor's width in mm
    Sh = mpd*height # Thermal sensor's height in mm
    S = sqrt(Sw**2+Sh**2) # Thermal sensor's diagonal size in mm
    FOV = 2*atan(S/(2*f)) # Field of view of the camera in rads
    landDiag = 2*alt*tan(FOV/2) # diagonal distance of the land area captured by the camera in metres
    pxSize = landDiag/(sqrt(width**2+height**2)*sqrt(2)) # pixel size in m per px

    # Geo-referencing calculation
    imCentre = numpy.array([height/2,width/2])
    pxPos = numpy.array([row,column]) # [row, column]
    v = imCentre - pxPos # vector between image centre and pixel position
    d = sqrt(v[1]**2+v[0]**2)*pxSize # estimation of distance on land between two points in metres
    R = 6371000 # Earth's radius in m

    if d != 0:
        theta = atan(v[0]/v[1]) # vector direction

        if theta > 0:
            if v[0] > 0:
                if kappa <= 90 or kappa >= 270: # kappa outside the range 90-270 indicates a North heading
                    bearing = theta + 3*pi/2
                else: # # kappa within the range 90-270 indicates a South heading
                    bearing = theta + pi/2
            else:
                if kappa <= 90 or kappa >= 270:
                    bearing = theta + pi/2
                else:
                    bearing = theta + 3*pi/2
        else:
            if v[0] > 0:
                if kappa <= 90 or kappa >= 270:
                    bearing = pi/2 + theta
                else:
                    bearing = 3*pi/2 +theta
            else:
                if kappa <= 90 or kappa >= 270:
                    bearing = 3*pi/2 + theta
                else:
                    bearing = pi/2+ theta
    else:
        bearing = 0

    #print([lat,long])
    lat = radians(lat)
    long = radians(long)
    lat2 = asin(sin(lat)*cos(d/R)+cos(lat)*sin(d/R)*cos(bearing))
    long2 = long + atan2(sin(bearing)*sin(d/R)*cos(lat),cos(d/R)-sin(lat)*sin(lat2))

    return lat2*180/pi, long2*180/pi

# Function to extract image geolocation and orientation from GPSdata.txt
# Input: path to GPSdata.txt & image name e.g., snap_1_ (44).jpg
# Output: array of information, array[0] is latitude, array[1] is longitude;
# array[2] is altitude, array[5] is kappa
def extractData(file, imageName):  
    # imageName = 'static/data/Thermal' + imageName
    with open(file, 'r') as f:
        data = numpy.empty((0), float)
        for _, line in enumerate(f):
            print(f"Found image name: {imageName}")
            if imageName in line:
                print(f"Found image name: {imageName}")
                nums = re.findall(r'\d+\.\d+', line)
                for num in nums:
                    data = numpy.append(data, numpy.array([float(num)]), axis=0)
                break
    return data


