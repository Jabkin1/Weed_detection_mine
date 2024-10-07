import os

# Specify the directory you want to scan
directory = '/home/jabkin/Desktop/Training_data/anotace_krok1'

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if "_nir" is in the filename
    if "_nir" in filename:
        file_path = os.path.join(directory, filename)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
