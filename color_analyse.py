from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Load the image
image_path = 'assets/Screenshot 2023-06-14 at 15.54.11.png'
image = Image.open(image_path)

# Resize the image (optional)
# image = image.resize((width, height))

# Convert the image to RGB
image = image.convert('RGB')

# Convert image to numpy array
image_array = np.array(image)

# Flatten the image array to a 2D array
pixels = image_array.reshape(-1, 3)

# Determine the number of dominant colors to extract
num_colors = 5

# Perform K-means clustering on the pixel data
kmeans = KMeans(n_clusters=num_colors)
kmeans.fit(pixels)

# Get the RGB values of the dominant colors
dominant_colors = kmeans.cluster_centers_

# Convert the RGB values to hexadecimal color codes
hex_colors = ['#%02x%02x%02x' % tuple(color.astype(int)) for color in dominant_colors]

# Print the dominant colors
for color in hex_colors:
    print(color)
