from ultralytics import YOLO
import torch
import cv2
from super_image import EdsrModel, ImageLoader
from PIL import Image
import os
from logic.constants import short_entity, plural_rules
async def Bounding_box(image_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = YOLO('yolov8n.pt')
    model.to(device)
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Image not loaded. Check the path: {image_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img_rgb)

    max_conf = 0
    best_box = None

    for result in results:
        boxes = result.boxes.xyxy 
        scores = result.boxes.conf  

        for box, score in zip(boxes, scores):
            if score > max_conf:
                max_conf = score
                best_box = box

    if best_box is not None:
        x1, y1, x2, y2 = map(int, best_box)
        bbox_width = x2 - x1
        bbox_height = y2 - y1

        return bbox_width, bbox_height
    else:
        return 0, 0
    
async def enhance_image(image_path):
    image = Image.open(image_path)
    model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)
    inputs = ImageLoader.load_image(image)
    preds = model(inputs)
    filename = os.path.basename(image_path)
    folder_path = "enhanced_images" 
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, filename)
    ImageLoader.save_image(preds, save_path)
    print("Saved enhanced image to:", save_path)
    return save_path

def format_entity_value(entity_name, entity_value):
    if entity_name in short_entity:
        unit = short_entity[entity_name]
    else:
        unit = entity_name

    if unit in plural_rules:
        unit = plural_rules[unit]
    
    return f"{entity_value} {unit}"