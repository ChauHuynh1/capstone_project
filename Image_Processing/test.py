# import the necessary packages
import numpy as np
import cv2

# open the gray16 image
gray16_image = cv2.imread("preprocessed_data/snap_1_ (1)_cell1.jpg", cv2.IMREAD_ANYDEPTH)

# get the dimensions of the image
height, width = gray16_image.shape

# ensure the coordinates are within the valid range
x = min(max(61, 0), width - 1)
y = min(max(12, 0), height - 1)

# get the pixel value at the specified coordinates
pixel_flame_gray16 = gray16_image[y, x]

# calculate temperature value in ° C
pixel_flame_gray16_celsius = (pixel_flame_gray16 / 100) - 273.15

# convert the gray16 image into a gray8 to show the result
gray8_image = np.zeros((height, width), dtype=np.uint8)
gray8_image = cv2.normalize(gray16_image, gray8_image, 0, 255, cv2.NORM_MINMAX)
gray8_image = np.uint8(gray8_image)

# add a pointer to the gray8 and gray16 images
cv2.circle(gray8_image, (x, y), 2, (0, 0, 0), -1)
cv2.circle(gray16_image, (x, y), 2, (0, 0, 0), -1)

# write the temperature value in Celsius to the images
cv2.putText(gray8_image, "{0:.1f} Celsius".format(pixel_flame_gray16_celsius), (x - 80, y - 15),
            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
cv2.putText(gray16_image, "{0:.1f} Celsius".format(pixel_flame_gray16_celsius), (x - 80, y - 15),
            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

# show the result
cv2.imshow("gray8-celsius", gray8_image)
cv2.imshow("gray16-celsius", gray16_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
