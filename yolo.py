from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model(source=0, show=True, conf=0.6, save=True)