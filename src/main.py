import os
import sys
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    # Replace href="/ and src="/ with basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Page generated successfully: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"\nScanning directory: {dir_path_content}")
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item_path.endswith('.md'):
            relative_path = os.path.relpath(item_path, dir_path_content)
            if os.path.basename(relative_path) == 'index.md':
                dest_path = os.path.join(dest_dir_path, relative_path)
                dest_path = dest_path.replace('.md', '.html')
            else:
                path_without_ext = relative_path[:-3]
                dest_path = os.path.join(dest_dir_path, path_without_ext, 'index.html')
            print(f"Processing: {item_path} -> {dest_path}")
            generate_page(item_path, template_path, dest_path, basepath)
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)

def main():
    print("Starting static site generation...")
    import sys
    # Get basepath from CLI argument, default to '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # Ensure basepath starts and ends with a slash
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    source_dir = "static"
    destination_dir = "docs"  # For GitHub Pages
    content_dir = "content"
    template_path = "template.html"
    try:
        print(f"\nStep 1: Copying static files from '{source_dir}' to '{destination_dir}'...")
        copy_directory_recursive(source_dir, destination_dir)
        print(f"\nStep 2: Generating pages from '{content_dir}'...")
        generate_pages_recursive(content_dir, template_path, destination_dir, basepath)
        print("\nStatic site generation complete!")
    except Exception as e:
        print(f"Error during site generation: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
