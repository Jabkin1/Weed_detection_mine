import os
import sys
import skimage.transform as sk_transform
import numpy as np
import imageio.v2 as imageio  # Explicitly import imageio.v2 to suppress deprecation warning

# Define the constant zoom factor
ZOOM_FACTOR = 1.003

# Define cropping values
CROP_TOP = 2
CROP_BOTTOM = 2
CROP_LEFT = 3
CROP_RIGHT = 3

def resize_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        img_path = os.path.join(input_dir, filename)
        # Check if the file is an image file and contains "rgb" in its name
        if os.path.isfile(img_path) and any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']) and 'rgb' in filename.lower():
            img = imageio.imread(img_path)
            height, width = img.shape[:2]
            
            # Compute new height and width
            new_height = int(height * ZOOM_FACTOR)
            new_width = int(width * ZOOM_FACTOR)
            
            # Resize the image
            resized_img = sk_transform.resize(img, (1540, 2054), order= 3 , anti_aliasing=False)
            
            # Crop the resized image to original pixel size
            #cropped_img = resized_img[CROP_TOP:height-CROP_BOTTOM, CROP_LEFT:width-CROP_RIGHT]
            
            # Save the resized and cropped image
            output_path = os.path.join(output_dir, filename)
            imageio.imwrite(output_path, (resized_img * 255).astype(np.uint8))

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 script.py input_directory output_directory")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    resize_images(input_directory, output_directory)
