import cv2
import subprocess
import socket
import json
from ultralytics import YOLO

def run_model(flag):
    model = YOLO('yolo11n.pt')

    # Setup socket for communication
    #robot_ip = 'your.local.machine.ip'
    #robot_port = 12345
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket

    # Capture video stream (replace with actual camera capture on Go1)
    cap = cv2.VideoCapture(0)  # 0 for default webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Perform object detection with YOLO
        results = model(frame)
        detected_keywords = []
        boxes = results[0].boxes

        class_ids = boxes.cls
        detected_keywords.append(class_ids)

        #detected_classes = results.names  # Extract detected class names

        # Get the names of objects detected (as keywords)

        print(detected_keywords)

        contains_flag = (detected_keywords[0] == flag).any()
        if contains_flag:
            p = subprocess.Popen(['node', 'testconsole.js', f'{flag}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Capture stdout and stderr
            stdout, stderr = p.communicate()

            # Decode the output and error messages (they are in bytes)
            print("STDOUT:", stdout.decode())
        else:
            continue

        # Send detected keywords (as a JSON string) to local machine
        #if detected_keywords:
            #message = json.dumps({'objects': detected_keywords})
            #sock.sendto(message.encode(), (robot_ip, robot_port))

    cap.release()
    #sock.close()

print("Welcome to our project!\nPlease select what you would like to detect from the menu below: ")

while(True):
    print("1: Person")
    print("2: Bottle")
    print("3: Dog")
    choice = input("")

    if choice == '1':
        run_model(0)
    elif choice == '2':
        run_model(39)
    elif choice == '3':
        run_model(2)
    else:
        print("Invalid choice, please select from the menu.")