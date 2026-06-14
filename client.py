# This is client code to receive video frames over UDP
import cv2, socket
import numpy as np
import time
import base64
import subprocess
from ultralytics import YOLO
import threading

executing = False
aframe = np.zeros((480, 640, 3), dtype=np.uint8)
boxes = []

def introduction():
    print("Welcome to our project!\nPlease select what you would like to detect from the menu below: \n")

    while(True):
        choice = input("1: Person\n2: Bottle\n3: Tracking\n\n")

        if choice in {'1', '2', '3'}:
            return choice
        else:
            print("Invalid choice, please select from the menu.")

# def walking():
#     global executing
#     executing = True
#     try:
#         print("Starting walk.mjs...")
#         subprocess.run(["node", "walk.mjs"], check=True, timeout=10)  # Timeout after 10 seconds
#         print("walk.js finished execution.")
#     except subprocess.TimeoutExpired:
#         print("walk.js timed out. Resuming detection...")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running walk.mjs: {e}")
#     except Exception as e:
#         print(f"Unexpected error running walk.mjs: {e}")
#     finally:
#         executing = False  # Reset flag when done 

# def pushup():
# 	global executing
# 	executing = True		
# 	try:
# 		print("Starting pushup.js...")
# 		# Use a subprocess call with a timeout to prevent blocking
# 		subprocess.run(["node", "pushup.mjs"], check=True, timeout=10)  # Timeout after 10 seconds
# 	except subprocess.TimeoutExpired:
# 		print("pushup.js timed out. Resuming detection...")
# 	except subprocess.CalledProcessError as e:
# 		print(f"Error running pushup.js: {e}")
# 	except Exception as e:
# 		print(f"Unexpected error running pushup.js: {e}")
# 		print("Resuming YOLO detection...")
# 	finally:
# 		executing = False  # Reset flag when done

def following():
	global executing, boxes
	executing = True		
	img_width = aframe.shape[1] #Width of camera feed
	if boxes:  # Ensure boxes is not empty
		for box in boxes:
			print(f"image width = {img_width}")
			img_min = img_width // 6
			img_max = img_width - img_width // 6
			x_min = box.xyxy[0][0]
			x_max = box.xyxy[0][2]

		#center_x = (x_min + x_max) / 2

		if x_min <= img_min :
			try:
				# Use a subprocess call with a timeout to prevent blocking
				print("HEYYYY IM MOVING LEFT")
				subprocess.run(["node", "follow.mjs", "L"], check=True, timeout=1)  # Timeout after 2 seconds
			except subprocess.TimeoutExpired:
				print("walk.js timed out. Resuming detection...")
			except subprocess.CalledProcessError as e:
				print(f"Error running follow.js: {e}")
			except Exception as e:
				print(f"Unexpected error running follow.js: {e}")
				print("Resuming YOLO detection...")
			#continue
			finally:
				executing = False  # Reset flag when done
		if x_max >= img_max:
			try:
				# Use a subprocess call with a timeout to prevent blocking
				print("HEYYYY IM MOVING RIGHT")
				subprocess.run(["node", "follow.mjs", "R"], check=True, timeout=1)  # Timeout after 2 seconds
			except subprocess.TimeoutExpired:
				print("follow.js timed out. Resuming detection...")
			except subprocess.CalledProcessError as e:
				print(f"Error running follow.js: {e}")
			except Exception as e:
				print(f"Unexpected error running follow.js: {e}")
				print("Resuming YOLO detection...")
			finally:
				executing = False  # Reset flag when done
			#continue
		#else:
			#continue
	#time.sleep(0.01)

def get_feed():
	BUFF_SIZE = 65507

	client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
	host_name = socket.gethostname()
	host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
	print("Receiving video from :",host_ip , "...\n")
	port = 5000
	message = b'Hello'
	client_socket.sendto(message,(host_ip,port))

	model = YOLO("yolo11n.pt") 

	choice = introduction()

	while True:
		packet,_ = client_socket.recvfrom(BUFF_SIZE)
		data = base64.b64decode(packet,' /')
		npdata = np.frombuffer(data,dtype=np.uint8)
		frame = cv2.imdecode(npdata,1) 
		#frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2,cv2.LINE_AA)
		results = model.track(source=frame, imgsz=32*12, conf=0.6, classes=[0,39], stream=True, persist=True)
		#results = model(frame, conf=0.65, imgsz=32*12, classes = [0,39], stream=True) 
		
		for res in results:
		# 	if i > 0:
		# 		temp = res [i-1]
			#if res != temp:
			aframe = res.plot()
					#cv2.putText(aframe, f"Total: {print(results)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
			cv2.imshow("RECEIVING VIDEO",aframe)
			
		# Extract bounding boxes and other information
			boxes = res.boxes  # Access bounding boxes
			detected_keywords = []
        
			if boxes:  # Check if there are any detections
				class_ids = boxes.cls.numpy()  # Extract class IDs as a numpy array
				detected_keywords.extend(class_ids.tolist())  # Convert to list
				
			print("Detected keywords:", detected_keywords)

			key = cv2.waitKey(1) & 0xFF
			#contains_flag = (detected_keywords[0] == flag.any())

		if choice == '1' and 0 in detected_keywords:  # If choice is 'person' and a person is detected
			if not executing:  # Ensure no other instance is running
				print("Walking...")
				walk_thread = threading.Thread(target=walking)
				walk_thread.start()  # Start the thread to execute walk.js
		elif choice == '2' and 39 in detected_keywords:  # If choice is 'person' and a person is detected
			if not executing:  # Ensure no other instance is running
				print("Working out...")
				pushup_thread = threading.Thread(target=pushup)
				pushup_thread.start()  # Start the thread to execute pushup.js
		elif choice == '3' and 0 in detected_keywords: 
			if not executing:  # Ensure no other instance is running
				print("Tracking...")
				follow_thread = threading.Thread(target=following)
				follow_thread.start()  # Start the thread to execute follow.js


		
		# cv2.putText(aframe, f"Total: {print(results)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
		if key == ord('q'):
			client_socket.close()
			break
		# if cnt == frames_to_count:
		# 	try:
		# 		fps = round(frames_to_count/(time.time()-st))
		# 		st=time.time()
		# 		cnt=0
		# 	except:
		# 		pass
		# cnt+=1


def auto():
	
	get_feed()

def main():
	auto()
	#cap.release()
	#sock.close()

if __name__ =="__main__":
	main()
