import cv2
import subprocess  # To run JavaScript code
from ultralytics import YOLO

print('hi')

# Load YOLO model
print('1')
model = YOLO('yolo11n.pt')  # Ensure the YOLO model is in your working directory
print('2')

# Capture video stream (replace with actual camera capture on Go1)
cap = cv2.VideoCapture(0)  # 0 for default webcam
if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()


while True:
    ret, frame = cap.read()
    if not ret:
        break
    print('4')

    # Perform object detection with YOLO
    results = model.predict(frame, save=False, stream=False)

    # Initialize an empty list for detected classes
    detected_keywords = []

    # Extract bounding boxes and class IDs
    try:
        boxes = results[0].boxes  # YOLO bounding box results
        class_ids = boxes.cls.cpu().numpy()  # Extract class IDs as a NumPy array

        detected_keywords.extend(class_ids)  # Append class IDs to the keywords list

        print("Detected class IDs:", detected_keywords)

        # Check if 'person' (class ID = 0) is detected
        if 0 in detected_keywords:
            print('Person detected! Running Go1 robot script...')

            # Run the JavaScript code via Node.js
            subprocess.run(["node", "walk.js"])
            break  # Exit the loop after running the robot script

    except Exception as e:
        print(f"Error processing results: {e}")
        continue

cap.release()