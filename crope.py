import os
import sys
import numpy as np
from PIL import Image

# Define cropping values
CROP_TOP = 2
CROP_BOTTOM = 2
CROP_LEFT = 3
CROP_RIGHT = 3

def crop_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all files in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a TIFF image and contains "rgb" in its name
        if filename.lower().endswith('.tiff') and 'rgb' in filename.lower():
            img_path = os.path.join(input_dir, filename)
            # Open the image
            img = Image.open(img_path)
            
            # Get the current size of the image
            width, height = img.size
            
            # Compute the new dimensions after cropping
            new_width = width - (CROP_LEFT + CROP_RIGHT)
            new_height = height - (CROP_TOP + CROP_BOTTOM)
            
            # Crop the image
            cropped_img = img.crop((CROP_LEFT, CROP_TOP, width - CROP_RIGHT, height - CROP_BOTTOM))
            
            # Save the cropped image
            output_path = os.path.join(output_dir, filename)
            cropped_img.save(output_path)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 script.py input_directory output_directory")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    crop_images(input_directory, output_directory)
