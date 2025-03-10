import re
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from google.colab import files

# Upload images
uploaded = files.upload()

char_images = {}

def preprocess_image(image_path, target_size=(50, 50)):
    img = Image.open(image_path).convert("L")
    img = img.resize(target_size)
    img = np.array(img)
    img = 255 - img
    return img

# Extract characters and store images in a dictionary
for filename in uploaded.keys():
    match = re.search(r"([A-Z])", filename)  # Find uppercase letter in filename
    if match:
        char = match.group(1)
        char_images[char] = preprocess_image(filename)
    else:
        print(f"Warning: Could not extract character from filename: {filename}")

def generate_handwritten_text(input_text, char_images, spacing=5, line_spacing=20, img_size=(50, 50)):
    char_width, char_height = img_size
    total_width = sum([char_width + spacing for char in input_text if char in char_images])
    total_height = char_height + 2 * line_spacing

    output_img = np.ones((total_height, total_width)) * 255

    x_offset = 0
    for char in input_text.upper():
        if char in char_images:
            char_img = char_images[char]
            output_img[line_spacing:line_spacing + char_height, x_offset:x_offset + char_width] = char_img
            x_offset += char_width + spacing

    return output_img

# Example usage
input_text = "W"
output_img = generate_handwritten_text(input_text, char_images)

plt.figure(figsize=(12, 5))
plt.imshow(output_img, cmap="gray")
plt.axis("off")
plt.show()