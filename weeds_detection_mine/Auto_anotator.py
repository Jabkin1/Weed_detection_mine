import os
import cv2
import numpy as np
import json
from image_processing import  noise_reduction

class AutoLabelWeeds:
    def __init__(self, path, out_json):
        self.path = path
        assert out_json.endswith(".json"), out_json
        self.out_json = out_json
        self.data = {}
        self.labels = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]
        self.current_label = "0"
        self.thrvalue = 140
        self.add_images()

    def save_data(self):
        with open(self.out_json, "w") as outfile:
            json.dump(self.data, outfile, indent=4)

    def add_images(self):
        assert os.path.isdir(self.path)
        file_list = os.listdir(self.path)
        for item in sorted(file_list):
            if item.endswith("N.tif"):  # Assuming NDVI images end with "N.tif"
                ndvi_path = os.path.join(self.path, item)
                color_path = os.path.join(self.path, item[:-5]+"C.tif")  # Corresponding color image
                if os.path.exists(color_path):
                    if ndvi_path not in self.data:
                        self.data[ndvi_path] = {"color": color_path, "annotations": []}

    def get_visible_elements(self, ndvi_image):

        _, binary_im = cv2.threshold(ndvi_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_im = noise_reduction(binary_im)
        contours, _ = cv2.findContours(binary_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        visible_elements = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                visible_elements.append({"x": x, "y": y, "w": w, "h": h, "kind": None})
        return visible_elements

    def annotate_images(self):
        for ndvi_path, info in self.data.items():
            ndvi_image = cv2.imread(ndvi_path, cv2.IMREAD_GRAYSCALE)
            visible_elements = self.get_visible_elements(ndvi_image)
            self.data[ndvi_path]["annotations"] = visible_elements
        self.save_data()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='__doc__')
    parser.add_argument('path', help='Path to NDVI image directory.')
    parser.add_argument('--out', help='Specify an annotation file name (.json)', default="annotations.json")

    args = parser.parse_args()
    auto_labeler = AutoLabelWeeds(path=args.path, out_json=args.out)
    auto_labeler.annotate_images()
