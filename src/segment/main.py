import numpy as np
# import torch
import matplotlib.pyplot as plt
from PIL import Image
from lang_sam import LangSAM
import cv2

model = LangSAM()
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))


def change_lens_color_to_white(image_path, output_path):
  
    with Image.open(image_path) as img:
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

      
        data = img.getdata()

       
        new_data = []

       
        lens_color_range = {
            'red': range(190, 256),   
            'green': range(190, 256),
            'blue': range(190, 256)
        }

       
        white_color = (255, 255, 255, 255)

        
        for item in data:
            
            if item[0] in lens_color_range['red'] and item[1] in lens_color_range['green'] and item[2] in lens_color_range['blue']:
                new_data.append(white_color)
            else:
                new_data.append(item)

       
        img.putdata(new_data)

        
        img.save(output_path)


def segment_glass(image_path):
    text_prompt = "spectacles"
    image_pil = Image.open(image_path).convert("RGB")
    masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)
    segmentation_mask = masks[0]
    binary_mask = np.where(segmentation_mask > 0.5, 1, 0)


    white_background = np.ones_like(np.array(image_pil), dtype=np.uint8) * 255
    binary_mask = np.expand_dims(binary_mask, axis=-1)  

    new_image_array = white_background * (1 - binary_mask) + np.array(image_pil) * binary_mask

    new_image = Image.fromarray(new_image_array.astype(np.uint8))
    new_image.save('output_segment.jpg')
    image_path = "output_segment.jpg"
    output_path = "final_output.png"
    change_lens_color_to_white(image_path, output_path)

