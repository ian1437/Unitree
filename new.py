import websocket
import cv2
from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO('yolo11n.pt')  # Assuming this is the path to your trained model

# WebSocket callback function when connected
def on_open(ws):
    print("Connected to WebSocket server")

# WebSocket callback function when receiving a message (not needed in this case)
def on_message(ws, message):
    print("Received message:", message)

# WebSocket callback function when closed
def on_close(ws):
    print("WebSocket connection closed")

# Start the WebSocket client
uri = "ws://localhost:8080"
ws = websocket.WebSocketApp(uri, on_open=on_open, on_message=on_message, on_close=on_close)

# Open WebSocket connection
ws.run_forever()

# Function to send command to the Node.js WebSocket server based on object detected
def send_command_for_object_detection(resultDict):
    if "text" in resultDict and resultDict["text"]:
        detected_text = resultDict["text"].lower()
        print("Detected text:", detected_text)

        # Send WebSocket message based on detected object
        if "person" in detected_text:  # Object identified as 'person'
            ws.send("1")  # Trigger push-up action
        elif "dog" in detected_text:  # Object identified as 'dog'
            ws.send("2")  # Trigger nod action
        elif "car" in detected_text:  # Object identified as 'car'
            ws.send("3")  # Trigger walk action
        elif "ball" in detected_text:  # Object identified as 'ball'
            ws.send("4")  # Trigger good action
    else:
        print("No objects detected.")

# Open webcam for live object detection
cap = cv2.VideoCapture(0)  # Start webcam capture

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Run YOLO object detection on the current frame
    results = model(frame)  # Run object detection on the frame

    # Extract recognized objects
    for result in results:
        detected_objects = result.names  # This gives a list of object names
        print("Detected objects:", detected_objects)

        resultDict = {"text": ""}  # Initialize the dictionary
        if "person" in detected_objects:
            resultDict["text"] = "person"
        elif "car" in detected_objects:
            resultDict["text"] = "car"
        elif "dog" in detected_objects:
            resultDict["text"] = "dog"
        elif "ball" in detected_objects:
            resultDict["text"] = "ball"
        
        # Send a command based on the recognized object
        send_command_for_object_detection(resultDict)

    # Show the frame for debugging
    cv2.imshow("Frame", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
