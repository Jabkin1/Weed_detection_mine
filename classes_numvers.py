import os
import glob
import xml.etree.ElementTree as ET
from collections import Counter

# Path to the folder containing XML files
xml_dir = '/home/jabkin/Desktop/Training_data/papa'  # Replace with your directory

# Initialize a counter for class names
class_counter = Counter()

# Scan through all XML files in the directory
for xml_file in glob.glob(os.path.join(xml_dir, '*.xml')):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Iterate over all objects (bounding boxes) in the XML
    for obj in root.iter('object'):
        class_name = obj.find('name').text  # Extract the class name
        class_counter[class_name] += 1      # Increment the counter for this class

# Number of unique classes
num_classes = len(class_counter)

# Print the results
print(f'Number of unique classes: {num_classes}')
print('Class distribution:')
for class_name, count in class_counter.items():
    print(f'Class "{class_name}": {count} instances')

