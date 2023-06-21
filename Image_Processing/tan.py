from PIL import Image, ImageFilter, ImageDraw, ImageFont

# open the image file
img = Image.open("data/Thermal/snap_1_ (412).jpg")

# convert the image to grayscale
gray_img = img.convert('L')

# apply binary filter with threshold of 128
binary_img = gray_img.point(lambda x: 0 if x < 128 else 255, '1')

# apply binary filter with threshold of 128
binary_img = gray_img.point(lambda x: 0 if x < 128 else 255, '1')

# convert binary image to RGB mode
binary_img = binary_img.convert('RGB')

# apply averaging filter with radius of 2 pixels
avg_img = binary_img.filter(ImageFilter.BoxBlur(2))


# create a color mask for thermal imaging
color_mask = Image.open("data/Thermal/snap_1_ (412).jpg").convert('RGBA')

# resize the color mask to match the size of the averaged image
color_mask = color_mask.resize(avg_img.size)

# paste the color mask onto the averaged image
result_img = Image.alpha_composite(avg_img.convert('RGBA'), color_mask)

# create a blank image for the color bar and draw a gradient on it
color_bar = Image.new('RGB', (100, result_img.height), (255, 255, 255))
draw = ImageDraw.Draw(color_bar)
gradient = [(255 - i, 0, i) for i in range(256)]

# Adjust the range to match the height of the result_img
for i in range(result_img.height):
    index = int(i / result_img.height * 255)
    draw.line((0, i, 100, i), fill=gradient[index], width=1)


# add text labels to the color bar indicating temperature
font = ImageFont.truetype("Arial.ttf", 12)
draw.text((10, 5), "Hotter", font=font, fill=(0, 0, 0))
draw.text((10, result_img.height - 20), "Colder", font=font, fill=(0, 0, 0))

# concatenate the result image and color bar side by side
final_img = Image.new('RGB', (result_img.width + color_bar.width, result_img.height))
final_img.paste(result_img, (0, 0))
final_img.paste(color_bar, (result_img.width, 0))

# save the final image
final_img.save("final_image.jpg")