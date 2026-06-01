"""
Option #2: Adaptive Thresholding Scheme Accounting for Changes in Illumination

This script segments two images of the same light and dark objects under two different
lighting directions.

Input images:
1. light_from_light_object.jpg
2. light_from_dark_object.jpg

Input folder:
C:\\Users\\HP\\OneDrive\\Documents\\Repo\\csu\\CSC515

Output folder:
C:\\Users\\HP\\OneDrive\\Desktop\\Reports

Before running:
pip install opencv-python numpy matplotlib
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path



# File paths


INPUT_IMAGES = [
    r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515\light_from_light_object.jpg",
    r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515\light_from_dark_object.jpg"
]

OUTPUT_DIR = Path(r"C:\Users\HP\OneDrive\Desktop\Reports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



# Adaptive thresholding settings


# Must be an odd number. Larger values work better for uneven lighting.
BLOCK_SIZE = 51

# Constant subtracted from the local threshold.
C_VALUE = 5

# Morphology kernel size for cleaning small noise.
KERNEL_SIZE = 5

# Minimum area for a contour to be treated as an object.
MIN_CONTOUR_AREA = 500


# Helper functions


def resize_for_display(image, width=900):
    """
    Resize large images to make processing and display easier.
    Aspect ratio is preserved.
    """
    height, current_width = image.shape[:2]

    if current_width <= width:
        return image

    scale = width / current_width
    new_height = int(height * scale)

    return cv2.resize(image, (width, new_height), interpolation=cv2.INTER_AREA)


def correct_illumination(gray_image):
    """
    Correct uneven illumination.

    A heavily blurred copy of the grayscale image is used as an estimate of
    the lighting field. The original grayscale image is divided by this
    lighting field to reduce shadows and uneven brightness.
    """
    background = cv2.GaussianBlur(gray_image, (0, 0), sigmaX=35, sigmaY=35)

    # Avoid division by zero
    background = np.where(background == 0, 1, background)

    corrected = (gray_image.astype(np.float32) / background.astype(np.float32)) * 128
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)

    return corrected


def segment_image(image_path):
    """
    Segment one image using:
    1. grayscale conversion
    2. median blur
    3. illumination correction
    4. adaptive thresholding
    5. morphological cleanup
    6. contour detection
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    image = resize_for_display(image)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce small noise while preserving edges
    denoised = cv2.medianBlur(gray, 5)

    # Correct uneven illumination caused by light direction
    corrected = correct_illumination(denoised)

    # Adaptive Gaussian thresholding
    adaptive_threshold = cv2.adaptiveThreshold(
        corrected,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        BLOCK_SIZE,
        C_VALUE
    )

    # Morphological cleanup
    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

    # Opening removes small foreground noise
    opened = cv2.morphologyEx(adaptive_threshold, cv2.MORPH_OPEN, kernel)

    # Closing fills small gaps inside the segmented object areas
    cleaned_mask = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    # Find contours in the cleaned mask
    contours, _ = cv2.findContours(
        cleaned_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Keep only object-sized contours
    valid_contours = [
        contour for contour in contours
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA
    ]

    # Draw contours on a copy of the original image
    contour_image = image.copy()
    cv2.drawContours(contour_image, valid_contours, -1, (0, 255, 0), 3)

    return {
        "original": image,
        "gray": gray,
        "denoised": denoised,
        "corrected": corrected,
        "adaptive_threshold": adaptive_threshold,
        "cleaned_mask": cleaned_mask,
        "contour_image": contour_image,
        "valid_contour_count": len(valid_contours)
    }


def save_results(results, image_name):
    """
    Save all processing outputs for one image.
    """
    stem = Path(image_name).stem

    output_files = {
        f"{stem}_01_original.jpg": results["original"],
        f"{stem}_02_gray.jpg": results["gray"],
        f"{stem}_03_denoised.jpg": results["denoised"],
        f"{stem}_04_illumination_corrected.jpg": results["corrected"],
        f"{stem}_05_adaptive_threshold.jpg": results["adaptive_threshold"],
        f"{stem}_06_cleaned_mask.jpg": results["cleaned_mask"],
        f"{stem}_07_final_contours.jpg": results["contour_image"]
    }

    for file_name, image in output_files.items():
        save_path = OUTPUT_DIR / file_name
        cv2.imwrite(str(save_path), image)


def show_results(results, title):
    """
    Display the main image processing stages.
    """
    display_images = [
        ("Original", cv2.cvtColor(results["original"], cv2.COLOR_BGR2RGB)),
        ("Grayscale", results["gray"]),
        ("Denoised", results["denoised"]),
        ("Illumination Corrected", results["corrected"]),
        ("Adaptive Threshold", results["adaptive_threshold"]),
        ("Cleaned Mask", results["cleaned_mask"]),
        ("Final Contours", cv2.cvtColor(results["contour_image"], cv2.COLOR_BGR2RGB))
    ]

    plt.figure(figsize=(15, 9))
    plt.suptitle(title, fontsize=15)

    for index, (label, image) in enumerate(display_images):
        plt.subplot(2, 4, index + 1)

        if len(image.shape) == 2:
            plt.imshow(image, cmap="gray")
        else:
            plt.imshow(image)

        plt.title(label)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    """
    Main program execution.
    """
    print("=" * 70)
    print("Option #2: Adaptive Thresholding Scheme Accounting for Changes in Illumination")
    print("=" * 70)

    print(f"\nOutput folder:")
    print(OUTPUT_DIR)

    for image_file in INPUT_IMAGES:
        image_path = Path(image_file)

        print("\n" + "-" * 70)
        print(f"Processing image: {image_path.name}")
        print(f"Input path: {image_path}")

        try:
            results = segment_image(image_path)

            save_results(results, image_path.name)

            print(f"Object-like regions detected: {results['valid_contour_count']}")
            print("Saved output files:")
            print(f"- {image_path.stem}_01_original.jpg")
            print(f"- {image_path.stem}_02_gray.jpg")
            print(f"- {image_path.stem}_03_denoised.jpg")
            print(f"- {image_path.stem}_04_illumination_corrected.jpg")
            print(f"- {image_path.stem}_05_adaptive_threshold.jpg")
            print(f"- {image_path.stem}_06_cleaned_mask.jpg")
            print(f"- {image_path.stem}_07_final_contours.jpg")

            show_results(results, image_path.name)

        except FileNotFoundError as error:
            print("\nERROR:")
            print(error)
            print("\nCheck that your image is saved in this folder:")
            print(r"C:\Users\HP\OneDrive\Documents\Repo\csu\CSC515")

    print("\n" + "=" * 70)
    print("Processing complete.")
    print(f"Check your results here: {OUTPUT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()