"""
Portfolio Milestone Assignment
Option #1: Drawing Functions in OpenCV

This program captures a frontal image using the webcam, detects the face and eyes,
draws a green circle around the face, draws red bounding boxes around the eyes,
adds the text "this is me", and saves the final image.

Author: Sunday
"""

import cv2
from pathlib import Path



# Set output folder and output image name

output_folder = Path(r"C:\Users\HP\OneDrive\Desktop\Reports")
output_folder.mkdir(parents=True, exist_ok=True)

output_image_path = output_folder / "portfolio_milestone_this_is_me.jpg"



# Load OpenCV Haar cascade files for face and eye detection

face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
eye_cascade_path = cv2.data.haarcascades + "haarcascade_eye.xml"

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

if face_cascade.empty():
    raise FileNotFoundError("The face cascade file could not be loaded.")

if eye_cascade.empty():
    raise FileNotFoundError("The eye cascade file could not be loaded.")



# Open the webcam

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("The webcam could not be opened. Check that your camera is connected and not being used by another app.")


print("Camera is open.")
print("Face the camera directly.")
print("Press SPACE to capture your image.")
print("Press ESC to exit without saving.")


captured_frame = None

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read from the camera.")
        break

    # Show live camera preview
    cv2.imshow("Camera Preview - Press SPACE to Capture", frame)

    key = cv2.waitKey(1)

    # ESC key
    if key == 27:
        print("Image capture cancelled.")
        break

    # SPACE key
    if key == 32:
        captured_frame = frame.copy()
        print("Image captured.")
        break


# Release the camera after capture
camera.release()
cv2.destroyAllWindows()



# Detect face and eyes, then draw on the image

if captured_frame is None:
    print("No image was captured. Program ended.")
else:
    image = captured_frame.copy()

    # Convert to grayscale because Haar cascade detection works better on grayscale images
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        print("No face was detected. Try again with better lighting and face the camera directly.")
    else:
        # Use the largest detected face in case more than one face appears
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face

        # Draw a green circle around the face
        center_x = x + w // 2
        center_y = y + h // 2
        radius = max(w, h) // 2

        green = (0, 255, 0)
        red = (0, 0, 255)
        black = (0, 0, 0)

        cv2.circle(
            image,
            (center_x, center_y),
            radius,
            green,
            3
        )

        # Detect eyes only inside the face area
        face_region_gray = gray_image[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(
            face_region_gray,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(20, 20)
        )

        # Sort eyes from left to right and draw only the first two likely eye detections
        eyes = sorted(eyes, key=lambda eye: eye[0])[:2]

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(
                image,
                (x + ex, y + ey),
                (x + ex + ew, y + ey + eh),
                red,
                3
            )

        # Add text label
        cv2.putText(
            image,
            "this is me",
            (x, max(y - 15, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            black,
            3,
            cv2.LINE_AA
        )

        # Save final output image
        cv2.imwrite(str(output_image_path), image)

        print(f"Final image saved here: {output_image_path}")

        # Show the final image
        cv2.imshow("Final Image - Portfolio Milestone", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()