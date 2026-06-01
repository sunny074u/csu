"""
Critical Thinking Assignment
Option #2: Morphology Operations for Handwritten Text Enhancement

Input:
    C:path\\sticky_note.jpg

Output:
    C:path\\filter_comparison_output.jpg
"""

import cv2
import numpy as np
import os


INPUT_IMAGE = r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515\sticky_note.jpg"
OUTPUT_IMAGE = r"C:\Users\HP\OneDrive\Desktop\Reports\filter_comparison_output.jpg"


def add_label(image, label):
    """Add a label to the top-left corner of an image."""
    labeled = image.copy()

    if len(labeled.shape) == 2:
        labeled = cv2.cvtColor(labeled, cv2.COLOR_GRAY2BGR)

    cv2.putText(
        labeled,
        label,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        2,
        cv2.LINE_AA
    )

    return labeled


def count_foreground_pixels(image):
    """Count white foreground pixels in a binary image."""
    return int(np.sum(image == 255))


def main():
    # Make sure the output folder exists
    output_folder = os.path.dirname(OUTPUT_IMAGE)
    os.makedirs(output_folder, exist_ok=True)

    # Read image
    original = cv2.imread(INPUT_IMAGE)

    if original is None:
        raise FileNotFoundError(
            f"Could not find the input image at:\n{INPUT_IMAGE}\n\n"
            "Make sure sticky_note.jpg is saved in the correct folder."
        )

    # Convert to grayscale
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Light blur to reduce scanner/camera noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Convert to binary image
    # Inverted threshold makes handwriting/text white and background black
    _, binary = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Structuring elements
    small_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    medium_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operations
    dilation = cv2.dilate(binary, small_kernel, iterations=1)
    erosion = cv2.erode(binary, small_kernel, iterations=1)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, small_kernel)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, medium_kernel)

    # Resize all images for comparison grid
    display_size = (360, 260)

    original_resized = cv2.resize(original, display_size)
    binary_resized = cv2.resize(binary, display_size)
    dilation_resized = cv2.resize(dilation, display_size)
    erosion_resized = cv2.resize(erosion, display_size)
    opening_resized = cv2.resize(opening, display_size)
    closing_resized = cv2.resize(closing, display_size)

    # Add labels
    original_labeled = add_label(original_resized, "Original")
    binary_labeled = add_label(binary_resized, "Binary")
    dilation_labeled = add_label(dilation_resized, "Dilation")
    erosion_labeled = add_label(erosion_resized, "Erosion")
    opening_labeled = add_label(opening_resized, "Opening")
    closing_labeled = add_label(closing_resized, "Closing")

    # Create comparison grid
    top_row = np.hstack([original_labeled, binary_labeled, dilation_labeled])
    bottom_row = np.hstack([erosion_labeled, opening_labeled, closing_labeled])
    comparison_grid = np.vstack([top_row, bottom_row])

    # Save final comparison output
    cv2.imwrite(OUTPUT_IMAGE, comparison_grid)

    print("Morphological processing completed successfully.")
    print(f"Input image:  {INPUT_IMAGE}")
    print(f"Output image: {OUTPUT_IMAGE}")

    print("\nForeground pixel count summary:")
    print("--------------------------------")
    print(f"Binary image: {count_foreground_pixels(binary)}")
    print(f"Dilation:     {count_foreground_pixels(dilation)}")
    print(f"Erosion:      {count_foreground_pixels(erosion)}")
    print(f"Opening:      {count_foreground_pixels(opening)}")
    print(f"Closing:      {count_foreground_pixels(closing)}")


if __name__ == "__main__":
    main()