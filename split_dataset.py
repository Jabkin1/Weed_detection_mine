import os
import shutil

# Define paths
base_dir = '/home/jabkin/Desktop/Training_data/fused_run/labels'
output_dirs = {
    'train': {'annotations': 'train/'},
    'val': {'annotations': 'val/'},
    'test': {'annotations': 'test/'}
}

file_lists = {
    'train': {
        'annotations': os.path.join(base_dir, 'train_annotations.txt')
    },
    'val': {

        'annotations': os.path.join(base_dir, 'val_annotations.txt')
    },
    'test': {

        'annotations': os.path.join(base_dir, 'test_annotations.txt')
    },
}

def move_files(split):
    for key in file_lists[split]:
        with open(file_lists[split][key], 'r') as f:
            files = f.read().splitlines()
        
        for file in files:
            if not os.path.isfile(file):
                print(f"File not found: {file}")
                continue
            
            file_name = os.path.basename(file)
            dest_dir = os.path.join(base_dir, output_dirs[split][key])
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy(file, os.path.join(dest_dir, file_name))
            print(f"Copied {file} to {dest_dir}")

# Move files for each split
for split in ['train', 'val', 'test']:
    move_files(split)

print("Files have been moved.")
