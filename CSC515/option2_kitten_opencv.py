"""
Option #2: Kitten Image Multi-Scale Representation in OpenCV

This program:
1. Loads a kitten image from the specified folder.
2. Splits the color image into three separate 2D channel matrices.
3. Merges the channels back into the original color image.
4. Creates another merged image using GRB channel order.
5. Displays and saves all resulting images.

Author: Sunday E.
"""

import cv2
from pathlib import Path
import sys



# PATHS

IMAGE_FOLDER = Path(r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515")
OUTPUT_FOLDER = Path(r"C:\Users\HP\OneDrive\Desktop\Reports")

# Exact kitten image
IMAGE_NAME = "shutterstock147979985--250.jpg"

IMAGE_PATH = IMAGE_FOLDER / IMAGE_NAME

# Create output folder if it does not already exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)



# LOAD IMAGE

image = cv2.imread(str(IMAGE_PATH), cv2.IMREAD_COLOR)

if image is None:
    print(f"Error: Could not load image from {IMAGE_PATH}")
    print("Check that the file name is correct and the image exists in the folder.")
    sys.exit(1)

print("Image loaded successfully.")
print("Original image shape:", image.shape)



# SPLIT INTO 2D CHANNEL MATRICES

# OpenCV reads images in BGR order
blue_channel, green_channel, red_channel = cv2.split(image)

print("Blue channel shape:", blue_channel.shape)
print("Green channel shape:", green_channel.shape)
print("Red channel shape:", red_channel.shape)


# Save 2D channel images
cv2.imwrite(str(OUTPUT_FOLDER / "channel_blue.png"), blue_channel)
cv2.imwrite(str(OUTPUT_FOLDER / "channel_green.png"), green_channel)
cv2.imwrite(str(OUTPUT_FOLDER / "channel_red.png"), red_channel)



# MERGE BACK TO ORIGINAL COLOR IMAGE

merged_original = cv2.merge([blue_channel, green_channel, red_channel])
cv2.imwrite(str(OUTPUT_FOLDER / "merged_original.png"), merged_original)



# CREATE GRB VERSION

# Since OpenCV uses BGR order, GRB means:
# New Blue  = green channel
# New Green = red channel
# New Red   = blue channel
merged_grb = cv2.merge([green_channel, red_channel, blue_channel])
cv2.imwrite(str(OUTPUT_FOLDER / "merged_grb.png"), merged_grb)



# DISPLAY RESULTS

cv2.imshow("Original Image", image)
cv2.imshow("Blue Channel", blue_channel)
cv2.imshow("Green Channel", green_channel)
cv2.imshow("Red Channel", red_channel)
cv2.imshow("Merged Original", merged_original)
cv2.imshow("Merged GRB", merged_grb)

print("\nImages saved successfully in:")
print(OUTPUT_FOLDER)
print("- channel_blue.png")
print("- channel_green.png")
print("- channel_red.png")
print("- merged_original.png")
print("- merged_grb.png")

cv2.waitKey(0)
cv2.destroyAllWindows()