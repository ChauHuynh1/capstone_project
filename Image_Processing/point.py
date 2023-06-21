import cv2
import numpy as np

# Define the temperature range of the thermal image
min_temperature = 0  # Minimum temperature in degrees Celsius
max_temperature = 100  # Maximum temperature in degrees Celsius

# Function to map grayscale intensity to temperature
def map_intensity_to_temperature(intensity, min_val, max_val):
    temperature_range = max_val - min_val
    temperature = (intensity / 255) * temperature_range + min_val
    return temperature

# Load the solar panel cell image
cell_image_path = "preprocessed_data/snap_1_ (1)_cell1.jpg"  # Update with the actual path to the cell image
cell_image = cv2.imread(cell_image_path, cv2.IMREAD_GRAYSCALE)

# Convert the grayscale image to a temperature map
temperature_map = map_intensity_to_temperature(cell_image, min_temperature, max_temperature)

# Print the temperature values
for row in temperature_map:
    for temperature in row:
        print(f"{temperature:.2f}°C", end=" ")
    print()
