import torch
import torchvision
from torchvision.transforms import functional as F
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

# COCO category names (the model's output label indices correspond to these names)
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
    'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
    'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet',
    'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Swap out Faster R-CNN for RetinaNet
model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
model.eval()  # Set the model to evaluation mode

# Load and preprocess the image (update the image path as needed)
image_path = "../input/test_image.jpg"  # Replace with your image file
image = Image.open(image_path).convert("RGB")
image_tensor = F.to_tensor(image)

# Perform object detection on the image
with torch.no_grad():
    predictions = model([image_tensor])

# Extract predictions for the first image in the batch
pred = predictions[0]
boxes = pred['boxes'].numpy()
labels = pred['labels'].numpy()
scores = pred['scores'].numpy()

# Set a threshold to filter out low-confidence detections
threshold = 0.5  # Adjust threshold as needed

# Convert image to OpenCV format for drawing
image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Loop over all detections and draw bounding boxes with labels for those above the threshold
for box, label, score in zip(boxes, labels, scores):
    if score >= threshold:
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label_name = COCO_INSTANCE_CATEGORY_NAMES[label]
        cv2.putText(image_cv, label_name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the final image with detections
plt.figure(figsize=(10, 8))
plt.imshow(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()