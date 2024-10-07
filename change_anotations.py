import os
import xml.etree.ElementTree as ET

# Define the directory containing XML annotation files
xml_dir = '/home/jabkin/Desktop/Training_data/papa'  # Replace with your directory path

# Define the mapping of old classes to new classes
class_mapping = {
    'desso': 'dicot',
    'gerxx': 'dicot',
    'paprh': 'dicot',
    'polco': 'dicot',
    'ephxx': 'dicot',
    'gasxx': 'dicot',
    'lampu': 'dicot',
    'fumxx': 'dicot',
    'conar': 'dicot',
    'polav': 'dicot',
    'lamam': 'dicot',
    'porol': 'dicot',
    'vioar': 'dicot',
    'senvu': 'dicot',
    'galap': 'dicot',
    'urtxx': 'dicot',
    'sinar': 'dicot',
    'eroci': 'dicot',
    'grass': 'ograss',
    'sonas': 'sonxx',
    'setvi': 'sagrass',
    'sonol': 'sonxx',
    'cirar': 'dicot',
    'agrre': 'ograss',
    'chehy': 'chexx',
    'urtur': 'dicot',
    'avefa': 'ograss',
    'polla': 'dicot',
    'echcg': 'sagrass',
    'cheal': 'chexx',
    'am': 'amare',
    'lacse': 'dicot',
    'soni': 'solni',
    'verhe': 'dicot',
    'digsa': 'sagrass',
    'cibule': 'dicot',
    'malne': 'dicot',
    'poaan': 'ograss'
    # Add more mappings as needed
}

def replace_annotations(xml_file, class_mapping):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate through each object in the annotation
    for obj in root.findall('object'):
        class_name = obj.find('name').text

        # Check if the class name is in the mapping
        if class_name in class_mapping:
            obj.find('name').text = class_mapping[class_name]  # Replace the class name

    # Save the modified XML file
    tree.write(xml_file)

# Iterate through each XML file in the directory
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(xml_dir, xml_file)
        replace_annotations(xml_path, class_mapping)
        print(f"Processed {xml_file}")

print("Selected annotations have been replaced.")
