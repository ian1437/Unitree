import cv2
import paramiko
import websocket
import time
from ultralytics import YOLO
import json

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

# WebSocket URI for the Node.js server
uri = "ws://localhost:8080"
ws = websocket.WebSocketApp(uri, on_open=on_open, on_message=on_message, on_close=on_close)

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
        elif "bottle" in detected_text:  # Object identified as 'bottle'
            ws.send("4")  # Trigger good action
    else:
        print("No objects detected.")

# Function to execute YOLO object detection remotely via Paramiko
def execute_yolo_on_remote(nano_ip, username, password, camera_index=0):
    # Set up SSH client using Paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the remote host key
    client.connect(nano_ip, username=username, password=password)

    # Run the YOLO object detection command on the remote Nano
    # Assuming you have YOLO and OpenCV installed remotely
    command = f"python3 /path/to/yolo_detection_script.py"

    # Execute the command remotely and get the output
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8')

    # Close SSH connection
    client.close()

    return output

# Start the WebSocket client
ws.run_forever()

# Establish connection to Nano #1 via Paramiko and run YOLO detection
nano_ip = "192.168.123.13"  # IP address of Nano #1 (change to your Nano's IP)
username = "unitree"  # SSH username
password = "123"  # SSH password

# Continuously stream and detect objects using YOLO
while True:
    # Execute YOLO detection on remote Nano #1
    output = execute_yolo_on_remote(nano_ip, username, password)

    # Parse the output of YOLO detection from the remote machine
    # Here we assume that the output from the remote script contains the detected objects
    try:
        resultDict = json.loads(output)  # Parse the JSON result returned from remote YOLO detection
        print("Detection Results:", resultDict)
        
        # Send the command to the Node.js WebSocket server based on the detected objects
        send_command_for_object_detection(resultDict)
    except json.JSONDecodeError:
        print("Error decoding YOLO output from remote system")
    
    # Sleep to simulate the live object detection flow
    time.sleep(1)  # Adjust the sleep time based on how fast you want the detection cycle to repeat
