# Import all libraries here
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import shutil
import preproc
import georef


# function to show the desired image
def imshow(img_title, img):
    cv.imshow(img_title, img)
    cv.waitKey(0)  # waits until a key is pressed to close the image window
    cv.destroyAllWindows()  # destroys the window showing image

# Image alignment: this function is to align image horizontally to make the visualization more easily
def align_image(img):
    # convert the colored thermal to greyscale
    img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # convert rgb to greyscale
    edges = cv.Canny(img_grey, 50, 150)  # Canny edges detection
    lines = cv.HoughLines(edges, 1, np.pi / 180, 200)  # lines detection using Hough algorithm
    angles = []
    for line in lines:
        for rho, theta in line:
            angles.append(theta)

    # find outliers angle in the angles array
    mean = np.mean(angles)
    standard_deviation = np.std(angles)
    distance_from_mean = abs(angles - mean)
    not_outlier = distance_from_mean < standard_deviation
    for i in sorted(np.where(not_outlier == False)[0], reverse=True):   # delete outlier values
        del angles[i]

    # find angle to align image
    angle = np.mean(angles) * 180 / np.pi
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv.getRotationMatrix2D(center, angle - 90, 1.0)
    img_rotated = cv.warpAffine(src=img, M=M, dsize=(w, h))
    return img_rotated


# function to read, align and show the Thermal image
def read_thermal_image(thermal_img_file):
    return align_image(cv.imread(thermal_img_file))  # return horizontally align Thermal image


'''this function is used for quick visualization. The input include:
    tmax: max temperature
    tmin: min temperature
    output: normal temperature + rgb image assign with colarmap'''
def image_visualization(input_thermal_img, tmax, tmin):
    # rgb to greyscale
    img_grey = cv.cvtColor(input_thermal_img, cv.COLOR_BGR2GRAY)
    # Image contrast Enhencement
    img_grey_equalized = cv.equalizeHist(img_grey)
    # Apply image for visualization
    rgb = cv.applyColorMap(img_grey_equalized, cv.COLORMAP_JET)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    #rgb_final = cv.filter2D(rgb, -1, kernel)

    # Binary thresholding
    threshold_value = 0.5 * img_grey_equalized.mean() # threshold value
    # threshold to extract panel regions only
    img_thresh = cv.threshold(img_grey_equalized, threshold_value, 255, cv.THRESH_BINARY)[1]
    img_temp = img_thresh & img_grey   # image contain panel only: only panel region is of interest
    # temperature of the solar panel only. This is used for the temperature analysis
    temp_from_img = np.delete(img_temp.flatten(), np.where(img_temp.flatten() == 0))
    
    '''define temperature mapping function
    the function used is Linear function--------------------------------------------------'''
    m = (tmax - tmin) / (np.amax(temp_from_img) - np.amin(temp_from_img))  # slope of the line
    b = tmin - m * np.amin(temp_from_img)
    # temperature function for Solar panels
    temp = m * img_grey + b     # temperature function
    norm = np.mean(temp[temp<55]) # Estimate normal temperature

    return norm, rgb, temp      # normal temp, processed thermal img


def draw_histogram(input_img, temp_map, saved_histogram):
    # Histogram showing temperature distribution ---------------
    plt.hist(temp_map)
    plt.hist(temp_map.ravel(), 256, [np.min(temp_map), np.max(temp_map)])
    plt.xlabel('Temperature ($^o$C)')
    plt.ylabel('Frequency')
    plt.title("Temperature histogram")
    plt.show()
    if (saved_histogram == True):
        plt.savefig(f"temp_hist({input_img}).jpg")

# this function is to pinpoint the location of defects
def defect_location(img):
    # Set up the SimpleBlobDetector with default parameters
    params = cv.SimpleBlobDetector_Params()
    # Set the threshold
    params.minThreshold = 0.33*cv.cvtColor(img, cv.COLOR_BGR2GRAY).mean()
    params.maxThreshold = 0.8*cv.cvtColor(img, cv.COLOR_BGR2GRAY).mean()
    # Set the area filter
    params.filterByArea = True
    params.minArea = 4
    params.maxArea = 230
    # Set the circularity filter
    params.filterByCircularity = True
    params.minCircularity = 0.4
    params.maxCircularity = 0.98
    # Set the convexity filter
    params.filterByConvexity = False
    params.minConvexity = 0.4
    params.maxConvexity = 0.98
    # Set the inertia filter
    params.filterByInertia = True
    params.minInertiaRatio = 0.1
    params.maxInertiaRatio = 0.98
    # Create a detector with the parameters
    detector = cv.SimpleBlobDetector_create(params)
    # Detect blobs
    keypoints = detector.detect(img)
    # Draw detected blobs as red circles
    img_with_defect_regions = cv.drawKeypoints(img, keypoints, np.array([]), (255, 0, 0),
                                          cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # process defect coordinates and panel numbers

    return img_with_defect_regions, cv.KeyPoint_convert(keypoints)


def find_panel_number(contours, coordinate):
    for i, cnt in enumerate(contours):
        x, y, w, h = cv.boundingRect(cnt)
        if x <= coordinate[0] <= x + w and y <= coordinate[1] <= y + h:
            return i + 1
    return None


def im_fill(im_th): # filling image with White color
    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:3]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv.floodFill(im_floodfill, mask, (0, 0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv
    return im_out


def get_defected_panel_labeled(img, img_to_label, temp_map, coordinates):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_sharpened = cv.filter2D(img, -1, kernel)    # sharpened thermal rgb image
    # customized greyscal conversion -----------------------------------
    coefficients = [0.2, 0.25, 0.55]  # Gives blue channel all the weight
    # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
    m = np.array(coefficients).reshape((1, 3))
    img_grey = cv.transform(img_sharpened, m)

    # Binary thresholding is to remove panels from background
    # Binary thresholding Stage 1
    thresh1 = cv.threshold(img_grey, 0.95*np.mean(img_grey), 255, cv.THRESH_BINARY)[1]
    '''imshow("Binary thresholded step 1", thresh1)'''

    # get eroded and dilated image: this is to highlight the Solar Panel bounding box-------------
    # this is to make the edge clearer !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    kernel_d = np.ones([2, 3], np.uint8)
    kernel_r = np.ones([3, 4], np.uint8)
    dilation = cv.dilate(~thresh1, kernel_d, iterations=2)
    erosion = cv.erode(dilation, kernel_r, iterations=1)

    # Find contours in the binary image ----------------------------------------------
    contours, _ = cv.findContours(~erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area to exclude small regions
    min_area_threshold = 400
    max_area_threshold = 3000
    filtered_contours = [cnt for cnt in contours if
                         (cv.contourArea(cnt) > min_area_threshold and cv.contourArea(cnt) < max_area_threshold)]

    # Sort filtered contours from left to right and top to bottom
    filtered_contours = sorted(filtered_contours, key=lambda c: cv.boundingRect(c)[1])

    # Create a copy of the original image for drawing purposes
    img_filtered_labeled = img_to_label.copy()

    # Initialize the label counter
    label_counter = 1

    # Draw the filtered contours as green rectangles with labels in the middle of each panel
    for cnt in filtered_contours:
        x, y, w, h = cv.boundingRect(cnt)
        # draw bounding box with GREEN color ----------
        cv.rectangle(img_filtered_labeled, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # Calculate the center coordinates of the contour
        center_x = x + w // 2
        center_y = y + h // 2

        # Determine the size of the label text
        label_size, _ = cv.getTextSize(str(label_counter), cv.FONT_HERSHEY_SIMPLEX, 0.9, 2)

        # Calculate the position to put the label (centered within the panel)
        label_x = int(center_x - label_size[0] // 2.5)
        label_y = int(center_y + label_size[1] // 2)

        # Add label text in the middle of the panel
        cv.putText(img_filtered_labeled, str(label_counter), (label_x, label_y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        label_counter += 1

    panel_number = 0
    failed_panel_filtered_dict = {}
    temp_dict = {}
    centre_dict = {}
    # Get defect coordinates ---------------------------------------------------------
    for coordinate in coordinates:

        prev_panel_number = panel_number

        # Find the panel number corresponding to the entered coordinates
        panel_number = find_panel_number(filtered_contours, coordinate)

        # Check if a valid panel number was found
        if not ( panel_number == 0 or panel_number == None):
            # Get the contour associated with the specified panel number
            panel_contour = filtered_contours[panel_number - 1]

            # Draw a RED outline around the selected panel-------
            x, y, w, h = cv.boundingRect(panel_contour)
            # Calculate the center coordinates of the contour
            centre_x = x + w // 2
            centre_y = y + h // 2
            #cv.rectangle(img_filtered_labeled, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Mark the specified coordinate on the original image -Yellow !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # cv.circle(img, np.int_(coordinate), 5, (0, 255, 255), 1)

            # Check if the specified coordinate belongs to the same panel
            if panel_number == 0:
                print("")
            elif panel_number == prev_panel_number:
                continue
            else:
                failed_panel_filtered_dict[panel_number] = img_to_label[y:y + h, x:x + w]
                temp_dict[panel_number] = temp_map[y:y + h, x:x + w]
                centre_dict[panel_number] = [centre_x, centre_y]

    # Filter outlier panels among faulty panels and draw red boxes around faulty panels after being filtered
    failed_panel_filtered_dict = outlier_filter(failed_panel_filtered_dict)
    for key in list(failed_panel_filtered_dict.keys()):
        panel_contour = filtered_contours[key - 1]
        x, y, w, h = cv.boundingRect(panel_contour)
        cv.rectangle(img_filtered_labeled, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # return img_filtered_labeled, cropped_panel, failed_panel_number
    return img_filtered_labeled, failed_panel_filtered_dict, temp_dict, centre_dict


def get_defected_panel(input_img):
    """1.Read/show Thermal image first"""
    thermal_img = read_thermal_image(input_img)
    # imshow("Thermal image", thermal_img)

    '''2.Visualize processed Thermal image'''
    normal_temp, processed_thermal_img, temp_map = image_visualization(thermal_img, tmax=60, tmin=30)
    print("Normal temperature value of the whole image: ", normal_temp)    # show normal temperature

    '''3. Image analysis: get defected locations'''
    img_with_defect, defect_coords = defect_location(processed_thermal_img)
    #imshow("Image with defect locations detected", img_with_defect)
    #print("There are " + str(defect_coords.shape[0]) + " suspicious defects found !")
    
    '''4. Display number labeled image in a Thermal image
    healthy panels: green,
    failed panels: red '''

    img_panel_label, failed_panel_filtered_dict, _, _ = get_defected_panel_labeled(thermal_img,
                                                                                        processed_thermal_img, temp_map,
                                                                                        defect_coords)

    #list_of_failed_panel = list(failed_panel_filtered_dict.keys())   # list of failed panel number
    # print("Suspicious failed filtered panel numbers: ", list_of_failed_panel)

    return processed_thermal_img, img_panel_label, failed_panel_filtered_dict    # list of defect panel number (sure + unsure!)


def outlier_filter(img_dict):
    def outlier_panel_detect(img):
        img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_thresh = cv.threshold(img_grey, 0.36 * np.mean(img_grey), 255, cv.THRESH_BINARY)[1]  # this function is to detect outlier
        # calculate percentage of outlier pixels in black
        outlier_pixel_percent = (img_thresh.shape[0] * img_thresh.shape[1] - np.count_nonzero(img_thresh)) * 100 /(
                    img_thresh.shape[0] * img_thresh.shape[1])
        return outlier_pixel_percent

    new_defect_panel_dict = {key: val for key, val in img_dict.items() if
                         (outlier_panel_detect(val) > 0.4 and outlier_panel_detect(val) <= 16.6)} # 0.31-0.78-16.6

    return new_defect_panel_dict


def create_dir(parent_dir, output_dir, remove_old_data):
    try:
        if os.path.exists(os.path.join(parent_dir, output_dir)) and (remove_old_data == True):
            shutil.rmtree(os.path.join(parent_dir, output_dir)) # delete all files and directory inside the output directory
            os.makedirs(os.path.join(parent_dir, output_dir), exist_ok=True)

        os.makedirs(os.path.join(parent_dir, output_dir), exist_ok=True)
    except OSError:
        print("Can NOT create directory!")


# this function is to save the process cropped thermal image
def get_snap_number(output_folder):
    snap_number = re.split('(\d+)', output_folder)
    return "".join(snap_number[3:4])

def save_processed_image(filtered_image_dict, input_therm_img, parent_dir):
    snap_number = get_snap_number(output_folder = input_therm_img)    # get the snap number from image file name
    create_dir(parent_dir = parent_dir, output_dir = f"snap({snap_number})", remove_old_data=True)    # create sub-folder to store each panel inside 1 snap
    for keys in list(filtered_image_dict.keys()):
        cv.imwrite(f"./{parent_dir}/snap({snap_number})/panel({keys}).png", cv.resize(filtered_image_dict[keys], (170, 300), cv.INTER_CUBIC))

# Function to compute temperature differences and post-processing parameters
def deltaT_processing(temp_dict, failed_panel_dict):
    panels_dict = {}
    panels_rgb_dict = {}
    for panel_number in list(failed_panel_dict.keys()):
        # Obtain panel temperature information
        temp = temp_dict[panel_number] # Get panel temperature values
        rgb = failed_panel_dict[panel_number] # Get the cropped panel image

        im = cv.cvtColor(rgb, cv.COLOR_BGR2GRAY) # Convert the image to grayscale

        tfilt = temp[temp>0]
        tfilt = tfilt[tfilt<42] # Filter out temperature above 42 degs C
        tnorm = np.mean(tfilt) # Estimate the normal panel temperature
        dT = temp - tnorm # Compute temperature differences

        # Extract faulty spots
        faulty = dT > 17.8
        binf = np.zeros_like(faulty, dtype=np.uint8)
        binf[faulty] = 255
        imFaulty = cv.addWeighted(im, 0.5, binf, 0.5, 0)

        # Calculate percentage of defects
        nPx = binf.shape[0]*binf.shape[1]
        nFaulty = np.sum(binf[:] == 255)
        nPerc = nFaulty/nPx*100

        # Calculate the maximum temperature difference per blob
        count, regions, stats, _ = cv.connectedComponentsWithStats(binf)
        colArr = []
        rowArr = []
        dT_info = {}
        num = 0 # reinitialize defect counters

        for id in range(1,count):
            if stats[id, 4] > 7: # Filter out blobs too small
                # Count number of defects after filtering
                num += 1
                # Extract maximum delta T of the region
                dtemp = dT[regions == id]
                dTmax = np.max(dtemp)

                # Determine defect severity
                if dTmax < 20:
                    severity = 'Medium'
                else:
                    severity = 'Severe'

                # Store the max dT value and its centre location on the image
                row, col = np.where(regions == id)
                index = np.where(dtemp == dTmax)[0]
                colMax = col[index][0]
                rowMax = row[index][0]

                colArr.append(colMax)
                rowArr.append(rowMax)

                cv.putText(rgb, str(num), (colMax-10, rowMax+5), cv.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1)

                # Determine defect types based on their locations and quantity
                if rowMax < binf.shape[0]/6 and colMax > binf.shape[1]/3 and colMax < binf.shape[1]*2/3:
                    type = 'Junction box'
                else:
                    if count-1 > 1:
                        type = 'Connection'
                    else:
                        type = 'Hotspot'

                # Function output: Defective regions' delta T values, severity, and types
                dT_info[num] = [dTmax, severity, type]

        # Draw circles around defects
        j = 0
        for row in rowArr:
            col = colArr[j]
            j += 1
            center = tuple([col, row])
            cv.circle(rgb,center,5,[0,255,255],1)

        # Resize images for visualisation
        #bin = cv.resize(binf, (170, 300), cv.INTER_CUBIC)
        imFaulty = cv.resize(imFaulty, (170, 300), cv.INTER_CUBIC)
        imRgb = cv.resize(rgb, (170, 300), cv.INTER_CUBIC)

        # Function output: panel information
        panel_info = {
            'normal temperature': tnorm,
            'defects percentage': nPerc,
            'defect counts': num
        }

        panels_dict[panel_number] = {
            'dT_info': dT_info,
            'panel_info': panel_info,
            'rgb': rgb
        }

        panels_rgb_dict[panel_number] = imRgb # Dictionary of resized images

    return panels_dict, panels_rgb_dict

def save_deltaT_results(input_img, parent_dir, save_as_csv):
    im = read_thermal_image(input_img)
    _, thermal_im, temp_map = image_visualization(im, tmax=60, tmin=30)
    _, defect_locs = defect_location(thermal_im)
    _, failed_panel_dict, temp_dict, centre_dict = get_defected_panel_labeled(im, thermal_im, temp_map, defect_locs)
    gps_dict = preproc.extractGPS([input_img], parent_dir, clean_data=False, save_as_csv=False) # Extract image's GPS data
    data = gps_dict[input_img]

    # Temperature difference post-processing
    panels_dict, panel_faults_dict = deltaT_processing(temp_dict, failed_panel_dict)

    if save_as_csv == True:
        snap_number = get_snap_number(input_img)
        dest_dir = os.path.join(parent_dir, f'snap({snap_number})')
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        file_path = os.path.join(dest_dir, f'snap({snap_number}).csv')
        with open(file_path, "w") as file:
            # Write the column names in the first line
            file.write("Panel number,Normal temperature,Percentage of defects,Number of defects,Latitude,Longitude")

            # Determine maximum defect counts among panels
            countArr = []
            for panel_number in list(panels_dict.keys()):
                panel_info = panels_dict[panel_number]['panel_info']
                count = panel_info['defect counts']
                countArr.append(count)
            
            maxCount = np.max(countArr)

            # Append column names for defect information in the first line
            for key in range(1,maxCount+1):
                file.write(",Temperature difference "+str(key)+",Severity "+str(key)+",Type "+str(key))

            # Iterate over panel numbers and save delta T processing results
            for panel_number in list(panels_dict.keys()):
                #rgb = panels_dict[panel_number]['rgb']
                dT_info = panels_dict[panel_number]['dT_info']
                panel_info = panels_dict[panel_number]['panel_info']
                panLoc = centre_dict[panel_number]
                lat, long = georef.geoTag(input_img,data[0],data[1],data[2],data[5],panLoc[0],panLoc[1])

                file.write('\n' + str(panel_number) + ',' + ",".join(str(value) for value in panel_info.values()))
                file.write(f',{lat},{long}')

                for key in list(dT_info.keys()):
                    infoArr = [dT_info[key][0], dT_info[key][1], dT_info[key][2]]
                    file.write(',' + ",".join(str(item) for item in infoArr))

    return panels_dict, panel_faults_dict


def save_labeled_thermal_image(input_img):
    snap_number = get_snap_number(output_folder=input_img)
    cv.imwrite(f'./{output_folder}/snap({snap_number})/labeled_snap({snap_number}).png', thermal_img_label)


def show_colorbar(img, tmin, tmax):
    plt.imshow(img[:, :, ::-1], cmap="jet", vmin=tmin, vmax=tmax)
    plt.axis('off')
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    input_imgs = ["snap_1_ (1).jpg","snap_1_ (44).jpg","snap_1_ (60).jpg","snap_1_ (320).jpg"]   # put all testing Thermal image to the list
    output_folder = "output_folder"     # Specify the Folder to store cropped processed image !
    create_dir(parent_dir=os.getcwd(), output_dir=output_folder, remove_old_data=True)  # delete all old data first
    # Extract and save GPS data as a csv file
    img_gps_dict = preproc.extractGPS(input_imgs,f'./{output_folder}/',clean_data=True,save_as_csv=True)

    # for input_img in list(img_gps_dict.keys()):

    #     processed_thermal_image, thermal_img_label, defect_panels_no_pinpoint = get_defected_panel(input_img = input_img)
    #     #show_colorbar(processed_thermal_image, tmax=60, tmin=30)
    #     #show_colorbar(thermal_img_label, tmax=60, tmin=30)

    #     # 1/ Generate a dictionary of panel images with pinpointed defects
    #     panels_dict, defect_panels_pinpointed = save_deltaT_results(input_img, f'./{output_folder}/', save_as_csv=False)

    #     print("List of failed panel number: ", list(defect_panels_no_pinpoint.keys()))

    #     '''create specify directory. 
    #     NOTE: os.getcwd() is to find current working directory'''
    #     create_dir(parent_dir=os.getcwd(), output_dir=output_folder, remove_old_data=False) # DO NOT delete data again, because it's already deleted!
    #     save_processed_image(filtered_image_dict=defect_panels_pinpointed,
    #                          input_therm_img=input_img,
    #                          parent_dir = f'./{output_folder}/')
    #     # save Thermal image
    #     save_labeled_thermal_image(input_img=input_img)

    #     # 2/ Save delta T processing results of defective panels to csv files
    #     _, _ = save_deltaT_results(input_img, f'./{output_folder}/', save_as_csv=True)