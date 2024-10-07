import os
import xml.etree.ElementTree as ET

# Define the directory containing XML annotation files
xml_dir = '/home/jabkin/Desktop/Training_data/papa'  # Replace with your directory path

def remove_nevim(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find and remove all 'nevim' objects
    for obj in root.findall('object'):
        class_name = obj.find('name').text

        # If the class is 'nevim', remove the entire object element
        if class_name == 'object':
            root.remove(obj)
            print(f"Removed 'object' from {xml_file}")

    # Save the modified XML file
    tree.write(xml_file)

# Iterate through each XML file in the directory
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(xml_dir, xml_file)
        remove_nevim(xml_path)

print("All 'object' annotations have been removed.")
