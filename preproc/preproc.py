from PIL import Image
import os
import numpy
import cv2

# Function for data cleaning, calculating orientation
# and storing the cleaned images' information in GPSdata.txt
# Input: list of source images and a destination directory
# Output: a data dictionary, new list of images, and GPSdata.csv in the destination directory
def extractGPS(im_list, dest_dir, clean_data, save_as_csv):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # Iterate over image files in the source directory and extract GPS data
    dataArr = numpy.empty((0,4),float)
    imGPS_dict = {}
    lat = 0
    long = 0

    for im in im_list:
        try:
            exif = Image.open(im)._getexif()
            # Rest of your image processing code here
        except Exception as e:
            print(f"Error processing {im}: {e}")
            continue
        lat_prev = lat
        long_prev = long
        lat = float(exif[34853][2][0]+exif[34853][2][1]/60+exif[34853][2][2]/3600)
        long = float(exif[34853][4][0]+exif[34853][4][1]/60+exif[34853][4][2]/3600)
        alt = exif[34853][6]
        if clean_data == True:
            # Only keep images with the altitude less than 34 m
            # Make sure the kept image does not repeat any existing set of latitude and longitude coordinates
            if alt < 34:
                if lat != lat_prev and long != long_prev:
                    #if lat >= 20.002609 and lat <= 20.00321 and long >= 105.62046 and long <= 105.62215:
                    dataArr = numpy.append(dataArr,numpy.array([[im,lat,long,alt]]),axis=0)
        else:
            dataArr = numpy.append(dataArr,numpy.array([[im,lat,long,alt]]),axis=0)

    # Determine the orientation of images in the destination directory
    modeAngleArr = numpy.empty((0,3),int)
    lat = dataArr[0,1]
    for row in dataArr:
        image_file = row[0]

        im = cv2.imread(image_file)
        img = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        bw = cv2.threshold(img,100,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]

        angleArr = numpy.empty((0),int)
        for i, c in enumerate(contours):
            # Calculate the area of each contour
            area = cv2.contourArea(c)
        
            # Ignore contours that are too small or too large
            if area < 1500:
                continue
        
            # cv.minAreaRect returns:
            # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = numpy.intp(box)
        
            # Retrieve the key parameters of the rotated bounding box
            #center = (int(rect[0][0]),int(rect[0][1])) 
            width = int(rect[1][0])
            height = int(rect[1][1])
            angle = int(rect[2])
        
            
            if width < height:
                angle = 90 - angle
            else:
                angle = 180 - angle
            
            angleArr = numpy.append(angleArr,numpy.array([angle]),axis=0)
        # Find the mode value in the angle array
        modeAngle = numpy.argmax(numpy.bincount(angleArr))

        # Calculate camera's yaw angle, camera towards North or South?
        lat_prev = lat
        lat = row[1]

        if lat >= lat_prev: # the latitude increasing indicates a North heading
            if modeAngle >= 90:
                kappa = modeAngle+180
            else:
                kappa = 90-modeAngle
        else: # the latitude decreasing indicates a South heading
            if modeAngle >= 90:
                kappa = modeAngle
            else:
                kappa = modeAngle+180
        #print([modeAngle,kappa])

        # Store orientation data, is the camera nadir? If yes then the pitch angle is not 0.
        modeAngleArr = numpy.append(modeAngleArr,numpy.array([[0.0,0.0,kappa]]),axis=0)

        # Function output: Dictionary of images' GPS and orientation data
        imGPS_dict[image_file] = [lat,row[2],row[3],0.0,0.0,kappa]

    dataArr = numpy.append(dataArr,numpy.array(modeAngleArr),axis=1)

    if save_as_csv == True:
        # Create a text file to store the image info in the destination directory
        file_path = os.path.join(dest_dir,'GPSdata.csv')
        with open(file_path, "w") as file:
            file.write('File,Latitude,Longitude,Altitude,Omega,Phi,Kappa\n')
            for row in dataArr:
                file.write(",".join(str(item) for item in row) + "\n")

    return imGPS_dict # Dictionary of image GPS and orientation

if __name__ == "__main__":
    # Define source directory & create destination directory

    # im_list = ['static/data/Thermal/snap_1_(1).jpg']
    # dest_dir = r'.\output_folder'
    # data_dict = extractGPS(im_list, dest_dir, clean_data=True, save_as_csv=False)
    # for file in list(data_dict.keys()):
    #     print(str(file) + ', ' + ', '.join(str(item) for item in data_dict[file]))

    import os

    folder_path = 'static/data/Thermal'

    # Create an empty list to store the file names including their parent directory
    file_names_with_parent = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            parent_dir_name = "static/data/Thermal"
            file_names_with_parent.append(os.path.join(parent_dir_name, file_name))

    dest_dir = r'.\output_folder'
    data_dict = extractGPS(file_names_with_parent, dest_dir, clean_data=True, save_as_csv=False)
    # for file in list(data_dict.keys()):
    #     print(str(file) + ', ' + ', '.join(str(item) for item in data_dict[file]))

     # Define the path to the output text file
    output_file_path = os.path.join(dest_dir, 'GPSdata.txt')

    # Open the file for writing
    with open("preproc/GPSdata.txt", 'w') as output_file:
        output_file.write('File,Latitude,Longitude,Altitude,Omega,Phi,Kappa\n')
        for file, data in data_dict.items():
            data_str = ','.join(map(str, data))
            output_file.write(f'{file},{data_str}\n')

    print(f'Results saved to {output_file_path}')
    