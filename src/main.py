import os
import shutil
import re
from markdown_parser import markdown_to_html_node

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

def extract_title(markdown):
    lines = markdown.split('\n')
    
    for line in lines:
        if re.match(r'^#\s+', line):
            return line[1:].strip()
    
    raise ValueError("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)
    
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Page generated successfully: {dest_path}")

def main():
    print("Starting static site generation...")
    
    source_dir = "static"
    destination_dir = "public"
    
    try:
        print(f"\nStep 1: Copying static files from '{source_dir}' to '{destination_dir}'...")
        copy_directory_recursive(source_dir, destination_dir)
        
        print(f"\nStep 2: Generating pages...")
        generate_page(
            from_path="content/index.md",
            template_path="template.html",
            dest_path="public/index.html"
        )
        
        print("\nStatic site generation complete!")
        
    except Exception as e:
        print(f"Error during site generation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())