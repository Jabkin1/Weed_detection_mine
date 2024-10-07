import os

def rename_files(folder_path, remove_substring):
    """
    Rename files in the specified folder by removing a specific substring from their names.

    :param folder_path: The path to the folder where files will be renamed.
    :param remove_substring: The substring to remove from file names.
    """
    # Check if the provided folder path is valid
    if not os.path.isdir(folder_path):
        print(f"The directory {folder_path} does not exist.")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the substring is in the filename
        if remove_substring in filename:
            # Construct the new filename
            new_filename = filename.replace(remove_substring, '')
            # Define full paths for the old and new filenames
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            try:
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
            except Exception as e:
                print(f"Error renaming file {old_file_path}: {e}")

# Example usage
if __name__ == "__main__":
    # Replace these with your folder path and the substring to remove
    folder = '/home/jabkin/Desktop/Training_data/fused_run/images/im'
    substring_to_remove = '_fused'
    rename_files(folder, substring_to_remove)
