import cv2
import torch
import urllib.request
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Download a sample image:
image_path = "../input/test_image.jpg"
#image_url = "https://stolica.bg/wp-content/uploads/2021/07/resize_park2.jpg"
#urllib.request.urlretrieve(image_url, image_path)

# Load YOLO model - first time it runs, it downloads the model:
#model = YOLO("./bin/models/yolov5n.pt")  # Nano (smallest, fastest, lowest accuracy)
#model = YOLO("./bin/models/yolov5s.pt")  # Small (default)
#model = YOLO("./bin/models/yolov5m.pt")  # Medium
#model = YOLO("./bin/models/yolov5l.pt")  # Large
#model = YOLO("./bin/models/yolov5x.pt")  # Extra-large (highest accuracy, slowest)

#model = YOLO("./bin/models/yolov8n.pt")  # Nano
#model = YOLO("./bin/models/yolov8s.pt")  # Small
#model = YOLO("./bin/models/yolov8m.pt")  # Medium
#model = YOLO("./bin/models/yolov8l.pt")  # Large
model = YOLO("./bin/models/yolov8x.pt")  # Extra-large

# Run object detection:
results = model(image_path)

# Display results:
for result in results:
    img = result.plot()  # Get image with detections

# Show the detected objects:
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()