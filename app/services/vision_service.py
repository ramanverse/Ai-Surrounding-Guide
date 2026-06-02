import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 nano model
model = YOLO("yolov8s.pt")

def get_spatial_info(x1, y1, x2, y2, img_width, img_height):
    """
    Calculates relative direction and proximity based on bounding box geometry.
    """
    # 1. Calculate Direction
    box_center_x = (x1 + x2) / 2
    
    if box_center_x < (img_width * 0.33):
        direction = "left"
    elif box_center_x > (img_width * 0.66):
        direction = "right"
    else:
        direction = "center"

    # 2. Calculate Proximity (Area of box vs Area of image)
    box_area = (x2 - x1) * (y2 - y1)
    img_area = img_width * img_height
    coverage_ratio = box_area / img_area

    if coverage_ratio > 0.30:  # Takes up more than 30% of the frame
        proximity = "close"
    elif coverage_ratio < 0.05: # Takes up less than 5% of the frame
        proximity = "far"
    else:
        proximity = "mid-range"

    return direction, proximity


async def process_image(image_bytes: bytes) -> list:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image.")

    # Get image dimensions for our spatial math
    img_height, img_width = img.shape[:2]

    # iou=0.4 means "if two boxes overlap by 40% or more, delete the lower score"
    results = model(img, verbose=False, agnostic_nms=True, iou=0.4)
    detected_objects = []
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_id = int(box.cls[0].item())
            class_name = model.names[class_id]
            confidence = round(box.conf[0].item(), 2)
            
            if confidence > 0.50: 
                direction, proximity = get_spatial_info(
                    x1, y1, x2, y2, img_width, img_height
                )
                
                detected_objects.append({
                    "label": class_name,
                    "confidence": confidence,
                    "spatial_context": {
                        "direction": direction,
                        "proximity": proximity
                    },
                    "box": {
                        "x1": int(x1), "y1": int(y1), 
                        "x2": int(x2), "y2": int(y2)
                    }
                })
            
    return detected_objects