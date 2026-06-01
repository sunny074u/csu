"""
Option #2: Adaptive Thresholding Scheme Accounting for Changes in Illumination

Purpose:
This script segments a scene containing one light object and one dark object under two
different lighting directions. It uses adaptive thresholding, illumination correction,
and basic morphological cleanup.

How to use:
1. Save two images in the same folder as this script:
   - light_from_light_object.jpg
   - light_from_dark_object.jpg

2. Install required libraries:
   pip install opencv-python numpy matplotlib

3. Run:
   python adaptive_threshold_illumination.py

4. Output images will be saved in a folder called:
   output_results
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path



# Configuration

IMAGE_FILES = [
    "light_from_light_object.jpg",
    "light_from_dark_object.jpg"
]

OUTPUT_DIR = Path("output_results")
OUTPUT_DIR.mkdir(exist_ok=True)

# Adaptive threshold settings
BLOCK_SIZE = 51  # Must be odd. Larger values handle wider lighting variation.
C_VALUE = 5      # Constant subtracted from local mean/weighted mean.

# Morphology settings
KERNEL_SIZE = 5


def resize_for_display(image, width=900):
    """
    Resize image for easier display while preserving aspect ratio.
    """
    h, w = image.shape[:2]
    if w <= width:
        return image
    ratio = width / w
    new_size = (width, int(h * ratio))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def correct_illumination(gray):
    """
    Estimate uneven background illumination and remove it.

    The idea is simple:
    - A blurred version of the grayscale image acts like an estimate of the lighting field.
    - Dividing the original grayscale image by this lighting field reduces shadows and
      uneven brightness.
    """
    background = cv2.GaussianBlur(gray, (0, 0), sigmaX=35, sigmaY=35)

    # Avoid division by zero
    background = np.where(background == 0, 1, background)

    corrected = (gray.astype(np.float32) / background.astype(np.float32)) * 128
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)

    return corrected


def segment_image(image_path):
    """
    Read an image, preprocess it, apply adaptive thresholding, and clean the result.
    """
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    image = resize_for_display(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    denoised = cv2.medianBlur(gray, 5)

    # Illumination correction
    corrected = correct_illumination(denoised)

    # Adaptive thresholding
    # THRESH_BINARY_INV is used because objects often become foreground against a lighter surface.
    adaptive = cv2.adaptiveThreshold(
        corrected,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        BLOCK_SIZE,
        C_VALUE
    )

    # Morphological cleanup
    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

    # Opening removes small noisy foreground pixels.
    opened = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel)

    # Closing fills small gaps inside segmented object regions.
    cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    # Find contours so we can draw segmented object boundaries.
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_image = image.copy()

    # Keep only reasonably large contours to avoid treating tiny noise as an object.
    min_area = 500
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    cv2.drawContours(contour_image, valid_contours, -1, (0, 255, 0), 3)

    return {
        "original": image,
        "gray": gray,
        "corrected": corrected,
        "adaptive": adaptive,
        "cleaned": cleaned,
        "contours": contour_image,
        "valid_contour_count": len(valid_contours)
    }


def save_results(results, image_name):
    """
    Save output images for one input image.
    """
    stem = Path(image_name).stem

    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_01_original.jpg"), results["original"])
    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_02_gray.jpg"), results["gray"])
    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_03_illumination_corrected.jpg"), results["corrected"])
    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_04_adaptive_threshold.jpg"), results["adaptive"])
    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_05_cleaned_mask.jpg"), results["cleaned"])
    cv2.imwrite(str(OUTPUT_DIR / f"{stem}_06_contours.jpg"), results["contours"])


def show_results(results, title):
    """
    Display the main processing stages.
    """
    images = [
        ("Original", cv2.cvtColor(results["original"], cv2.COLOR_BGR2RGB)),
        ("Grayscale", results["gray"]),
        ("Illumination Corrected", results["corrected"]),
        ("Adaptive Threshold", results["adaptive"]),
        ("Cleaned Mask", results["cleaned"]),
        ("Final Contours", cv2.cvtColor(results["contours"], cv2.COLOR_BGR2RGB))
    ]

    plt.figure(figsize=(14, 9))
    plt.suptitle(title, fontsize=14)

    for i, (label, img) in enumerate(images):
        plt.subplot(2, 3, i + 1)
        if len(img.shape) == 2:
            plt.imshow(img, cmap="gray")
        else:
            plt.imshow(img)
        plt.title(label)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    print("Adaptive Thresholding for Illumination Change")
    print("-" * 55)

    for image_file in IMAGE_FILES:
        image_path = Path(image_file)

        print(f"\nProcessing: {image_file}")

        try:
            results = segment_image(image_path)
            save_results(results, image_file)

            print(f"Valid object-like regions detected: {results['valid_contour_count']}")
            print(f"Saved outputs to: {OUTPUT_DIR.resolve()}")

            show_results(results, image_file)

        except FileNotFoundError as error:
            print(error)
            print("Make sure the image file is saved in the same folder as this script.")


if __name__ == "__main__":
    main()