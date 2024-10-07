import os
import xml.etree.ElementTree as ET

# Define paths
xml_dir = '/home/jabkin/Desktop/Training_data/papa'  # Directory containing XML files
output_dir = '/home/jabkin/Desktop/VoTT/anotations'  # Directory to save YOLO format labels
classes = [
    'cabbage', 'amare', 'verpe', 'ograss', 'dicot', 'steme', 'capbp', 'solni', 
    'meran', 'chexx', 'matin', 'sagrass', 'sonxx',  
    'thlar'
]

# Default size if <size> is missing
default_size = (2048, 1536)  # Adjust this as needed

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def convert_bbox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x_center = (box[0] + box[1]) / 2.0 - 1
    y_center = (box[2] + box[3]) / 2.0 - 1
    width = box[1] - box[0]
    height = box[3] - box[2]
    return (x_center * dw, y_center * dh, width * dw, height * dh)

for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith('.xml'):
        continue

    # Parse XML
    tree = ET.parse(os.path.join(xml_dir, xml_file))
    root = tree.getroot()

    size = root.find('size')
    if size is None:
        width, height = default_size
        print(f"{xml_file}: <size> element not found. Using default size {default_size}.")
    else:
        width = int(size.find('width').text)
        height = int(size.find('height').text)

    output_file = os.path.join(output_dir, os.path.splitext(xml_file)[0] + '.txt')

    with open(output_file, 'w') as out_file:
        for obj in root.iter('object'):
            class_name = obj.find('name').text
            if class_name not in classes:
                continue

            class_id = classes.index(class_name)
            xml_box = obj.find('bndbox')
            bbox = (float(xml_box.find('xmin').text), float(xml_box.find('xmax').text),
                    float(xml_box.find('ymin').text), float(xml_box.find('ymax').text))
            bbox_converted = convert_bbox((width, height), bbox)
            out_file.write(f"{class_id} " + " ".join([f"{x:.6f}" for x in bbox_converted]) + '\n')

print("Conversion completed.")