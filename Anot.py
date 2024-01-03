import os
import cv2
import numpy as np
import json
from image_processing import get_ndvi_im, noise_reduction

class AutoLabelWeeds:

    def add_images(self):
        # Get all NDVI images in the specified directory
        ndvi_images = os.listdir(self.path)

        # Add each NDVI image to the data dictionary
        for ndvi_image in ndvi_images:
            if ndvi_image.endswith(".png"):
                ndvi_path = os.path.join(self.path, ndvi_image)
                if os.path.exists(ndvi_path):
                    self.data[ndvi_path] = {}

    def __init__(self, path, out_json, naming_convention):
        self.path = path
        assert out_json.endswith(".json"), out_json
        self.out_json = out_json
        self.data = {}
        self.labels = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]
        self.current_label = "0"
        self.thrvalue = 140
        self.naming_convention = naming_convention

        # Call the add_images() method to initialize the data dictionary
        self.add_images()

    def get_visible_elements(self, ndvi_image):
        # Your logic to identify visible elements in the NDVI image goes here
        # This might involve thresholding, contours, or any suitable method for your specific case
        # You would identify and extract elements (e.g., contours, bounding boxes) similar to the manual annotation logic

        # Example logic (replace this with your actual logic):
        _, binary_im = cv2.threshold(ndvi_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_im = noise_reduction(binary_im)
        contours, _ = cv2.findContours(binary_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visible_elements = []

        # Naming convention based on user input
        for index, cnt in enumerate(contours):
            if cv2.contourArea(cnt) > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                kind = f"{self.naming_convention}_{index}"  # Construct the name based on convention
                visible_elements.append({"x": x, "y": y, "w": w, "h": h, "kind": kind})

        return visible_elements

    def annotate_images(self):
        for ndvi_path, info in self.data.items():
            ndvi_image = cv2.imread(ndvi_path, cv2.IMREAD_GRAYSCALE)
            visible_elements = self.get_visible_elements(ndvi_image)
            self.data[ndvi_path]["annotations"] = visible_elements
        self.save_data()

def perform_ndvi(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_list = os.listdir(image_dir)
    for item in sorted(file_list):
        if item.endswith("C.tif"):  # Assuming color images end with "C.tif"
            color_path = os.path.join(image_dir, item)
            nir_path = os.path.join(image_dir, item[:-5] + "N.tif")  # Corresponding NIR image
            if os.path.exists(nir_path):
                color_im = cv2.imread(color_path)
                nir_im = cv2.imread(nir_path, cv2.IMREAD_GRAYSCALE)

                # Perform NDVI
                ndvi_im = get_ndvi_im(color_im, nir_im)
