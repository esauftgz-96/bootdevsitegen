from textnode import *
from htmlnode import *
from mkd_blocks import *
import shutil
import os
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    static_to_public()
    generate_pages_recursive("content","template.html","docs",basepath)

def copy_recursive(src_path, dst_path):
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)
        
        if os.path.isfile(src_item):
            # Copy the file
            shutil.copy(src_item, dst_item)
            print(f"Copied: {src_item} to {dst_item}")
        else:
            # Create directory if it doesn't exist
            if not os.path.exists(dst_item):
                os.mkdir(dst_item)
            # Recursively copy the subdirectory
            copy_recursive(src_item, dst_item)

def static_to_public():
    # Initialize public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    # Start recursive copy
    copy_recursive("static", "public")

# def generate_page(from_path, template_path, dest_path):
#     print (f"Generating page from {from_path} to {dest_path} using {template_path}.")
#     with open(from_path, 'r') as file:
#         markdown = file.read()
#     with open(template_path, 'r') as file:
#         template = file.read()
#     processed_markdown = markdown_to_html_node (markdown).to_html()
#     title = extract_title(markdown)
#     template = template.replace("{{ Title }}",title)
#     template = template.replace("{{ Content }}",processed_markdown)
#     dir_path = os.path.dirname(dest_path)
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)
#     with open(dest_path, 'w') as file:
#         file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dst_item = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_item) and src_item.endswith(".md"):
            with open(src_item, 'r') as file:
                markdown = file.read()
            with open(template_path, 'r') as file:
                template = file.read()
            processed_markdown = markdown_to_html_node (markdown).to_html()
            title = extract_title(markdown)
            template = template.replace("{{ Title }}",title)
            template = template.replace("{{ Content }}",processed_markdown)
            template = template.replace('href="/',f'href="{basepath}')
            template = template.replace('src="/',f'src="{basepath}')
            dir_path = os.path.dirname(dst_item)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(dst_item.replace(".md",".html"), 'w') as file:
                file.write(template)
        
        else:
            if os.path.isdir(src_item):
                if not os.path.exists(dst_item):
                    os.mkdir(dst_item)
            generate_pages_recursive(src_item,template_path,dst_item,basepath)


    
    
    

    
main()

