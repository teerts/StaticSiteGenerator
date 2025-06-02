import os
import shutil

def copy_directory_recursive(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"Source directory '{source}' does not exist")
    
    if os.path.exists(destination):
        print(f"Cleaning destination directory: {destination}")
        shutil.rmtree(destination)
    
    os.makedirs(destination)
    print(f"Created destination directory: {destination}")
    
    _copy_contents_recursive(source, destination)

def _copy_contents_recursive(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")
        
        elif os.path.isdir(source_path):
            os.makedirs(destination_path)
            print(f"Created directory: {destination_path}")
            _copy_contents_recursive(source_path, destination_path)

def main():
    print("Starting static site generation...")
    
    source_dir = "static"
    destination_dir = "public"
    
    try:
        print(f"\nCopying static files from '{source_dir}' to '{destination_dir}'...")
        copy_directory_recursive(source_dir, destination_dir)
        print(f"\nSuccessfully copied all contents from '{source_dir}' to '{destination_dir}'")
        print("\nStatic site generation complete!")
    except Exception as e:
        print(f"Error during site generation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())