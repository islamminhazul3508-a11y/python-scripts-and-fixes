import os
import shutil

def organize_files(folder_path):
    """
    Automates sorting of files into specific categories based on extension.
    Useful for cleaning messy Downloads or project directories.
    """
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Documents': ['.pdf', '.docx', '.txt', '.csv'],
        'Code': ['.py', '.html', '.css', '.js'],
        'Archives': ['.zip', '.rar', '.tar']
    }

    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_ext = os.path.splitext(item)[1].lower()
            moved = False
            for folder, extensions in categories.items():
                if file_ext in extensions:
                    target_dir = os.path.join(folder_path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(item_path, os.path.join(target_dir, item))
                    print(f"Moved: {item} -> {folder}")
                    moved = True
                    break
            if not moved:
                target_dir = os.path.join(folder_path, 'Others')
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(item_path, os.path.join(target_dir, item))

if __name__ == "__main__":
    target = input("Enter directory path to organize: ")
    organize_files(target)
