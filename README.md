# Thermal Imaging Analysis Application

## Overview
This Python application is designed to analyze thermal images and provide insights into temperature patterns and defect detection. It includes various functions for processing thermal images, visualizing temperature data, and identifying defects in panels. Below are descriptions of the main functions in this application:

### `read_thermal_image(image_path)`
This function reads a thermal image from the specified file path and returns the image as a NumPy array.

### `image_visualization(image, tmax, tmin)`
Given a thermal image, this function visualizes the image by adjusting temperature values within the specified range (`tmax` and `tmin`). It returns the visualized image, the maximum temperature value, and the minimum temperature value.

### `get_defected_panel(input_img)`
This function processes a thermal image to identify defective panels. It returns processed images, thermal image labels, and panels without pinpointed defects.

### `defect_location(processed_thermal_img)`
Given a processed thermal image, this function locates the defects and returns the coordinates of the defects.

### `get_defected_panel_labeled(selected_image, processed_thermal_img, temp_map, defect_coords)`
This function provides additional information about the defective panels, including temperature information and labels. It returns information about all panels, defected panels, and temperature maps.

### `update_table_info(selected_filename, click_data)`
This is a callback function for a Dash web application. It updates the table information displayed on the web page based on user interactions. It includes features like displaying normal temperatures, defect counts, defect types, and recommendations.

## Usage
To use this application, follow these steps:

1. Install the required Python packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
