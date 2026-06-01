# Portfolio Milestone Assignment – Option #2: Installing OpenCV 2
# This program loads a shutterstock image, displays it, and saves a copy to the Desktop.

import cv2
from pathlib import Path

# Folder where your assignment files are stored
base_folder = Path(r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515")

# Downloaded image uses
image_path = base_folder / "shutterstock130285649--250.jpg"

# Load the image
image = cv2.imread(str(image_path))

# Check that the image loaded properly
if image is None:
    print(f"Error: Could not load image from: {image_path}")
    print("Make sure the numbers image is inside the CSC515 folder and that the file name matches exactly.")
else:
    # Display the image
    cv2.imshow("shutterstock Image", image)

    # Save a copy of the image to the Desktop
    desktop_path = Path(r"C:\Users\HP\OneDrive\Desktop\Reports")
    output_path = desktop_path / "shutterstock_copy.jpg"

    success = cv2.imwrite(str(output_path), image)

    if success:
        print("Image loaded successfully.")
        print(f"Copy saved to: {output_path}")
    else:
        print("Error: The image could not be saved.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()