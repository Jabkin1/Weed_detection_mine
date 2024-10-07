import os
import xml.etree.ElementTree as ET

def find_files_with_annotation(folder_path, search_annotation):
    """
    Locate XML files in the specified folder that contain a specific annotation.

    :param folder_path: The path to the folder containing XML files.
    :param search_annotation: The annotation (e.g., object name) to search for in the XML files.
    :return: A list of file paths containing the specified annotation.
    """
    matching_files = []

    # Check if the provided folder path is valid
    if not os.path.isdir(folder_path):
        print(f"The directory {folder_path} does not exist.")
        return matching_files

    # Iterate over all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Check for the annotation in the XML file
                for obj in root.iter('object'):
                    obj_name = obj.find('name')
                    if obj_name is not None and obj_name.text == search_annotation:
                        matching_files.append(file_path)
                        break
            except ET.ParseError as e:
                print(f"Error parsing file {file_path}: {e}")

    return matching_files

# Example usage
if __name__ == "__main__":
    # Replace these with your folder path and the annotation to search for
    folder = '/home/jabkin/Desktop/Training_data/nope'
    annotation_to_find = 'amare'
    
    # Find files containing the specified annotation
    files_with_annotation = find_files_with_annotation(folder, annotation_to_find)
    
    if files_with_annotation:
        print(f"Files containing '{annotation_to_find}':")
        for file in files_with_annotation:
            print(file)
    else:
        print(f"No files found containing '{annotation_to_find}'.")
