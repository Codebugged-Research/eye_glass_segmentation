import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from lang_sam import LangSAM
import cv2

# Assuming you have a model class called LangSAM for handling predictions
model = LangSAM()

def segment_glass(image_path, output_path):
    text_prompt = "spectacles"
    image_pil = Image.open(image_path).convert("RGB")
    masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)
    segmentation_mask = masks[0]
    binary_mask = np.where(segmentation_mask > 0.5, 1, 0)

    white_background = np.ones_like(np.array(image_pil), dtype=np.uint8) * 255
    binary_mask = np.expand_dims(binary_mask, axis=-1)
    new_image_array = white_background * (1 - binary_mask) + np.array(image_pil) * binary_mask

    new_image = Image.fromarray(new_image_array.astype(np.uint8))
    intermediate_path = 'output_segment.png'
    new_image.save(intermediate_path)
    change_lens_color_to_white(intermediate_path, output_path)

def change_lens_color_to_white(image_path, output_path):
    with Image.open(image_path) as img:
       
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        data = img.getdata()
        new_data = []

       
        lens_color_range = {'red': range(190, 250), 'green': range(190, 250), 'blue': range(190, 250)}
        white_color = (255, 255, 255, 255) 

       
        for item in data:
            if item[0] in lens_color_range['red'] and item[1] in lens_color_range['green'] and item[2] in lens_color_range['blue']:
                new_data.append(white_color)
            else:
                new_data.append(item)

        
        img.putdata(new_data)
        rgb_img = img.convert('RGB')  
        rgb_img.save(output_path)  

