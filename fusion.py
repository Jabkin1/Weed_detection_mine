from PIL import Image
import numpy as np
import os
import tifffile as tiff

def fuse_rgb_nir_images(rgb_dir, nir_dir, output_dir, file_extension=".tiff"):
    os.makedirs(output_dir, exist_ok=True)

    rgb_files = [f for f in os.listdir(rgb_dir) if f.endswith(file_extension)]
    
    for rgb_file in rgb_files:
        base_name = os.path.splitext(rgb_file)[0].replace('_rgb', '')
        nir_file = base_name + '_nir' + file_extension
        
        rgb_path = os.path.join(rgb_dir, rgb_file)
        nir_path = os.path.join(nir_dir, nir_file)
        
        if os.path.exists(nir_path):
            print(f"Processing {rgb_file} and {nir_file}")
            
            rgb_image = Image.open(rgb_path).convert('RGB')
            nir_image = Image.open(nir_path).convert('L')
            
            rgb_array = np.array(rgb_image)
            nir_array = np.array(nir_image)
            
            fused_image = np.dstack((rgb_array, nir_array))
            fused_image = np.ascontiguousarray(fused_image)  # Ensure array is contiguous in memory
            
            # Save the fused image using tifffile
            output_path = os.path.join(output_dir, base_name + '_fused.tiff')
            tiff.imwrite(output_path, fused_image)
            
            print(f"Saved fused image to {output_path}")
        else:
            print(f"NIR file for {rgb_file} not found, skipping...")

# Example usage
rgb_dir = '/home/jabkin/Desktop/VoTT/val/rgb'
nir_dir = '/home/jabkin/Desktop/VoTT/val/nir'
output_dir = '/home/jabkin/Desktop/Training_data/fused_run/images/im'
fuse_rgb_nir_images(rgb_dir, nir_dir, output_dir)
