from textnode import TextNode, TextType
from htmlnode import HTMLNode
from block_markdown import markdown_to_html_node
import shutil, os

def main():
    #copy_static()

    from_path="content/index.md"
    template_path="template.html"
    dest_path="./public"
    content_dir="./content"

    #generate_page(from_path, template_path, dest_path)
    generate_pages_recursive(content_dir, template_path, dest_path)

def copy_static():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")

    copy_recursive("./static", "./public")

def copy_recursive(current_dir, destination_dir):

    static_contents = os.listdir(current_dir)

    for content in static_contents:
        current_content_fp = os.path.join(current_dir, content)

        if os.path.isfile(current_content_fp):
            shutil.copy(current_content_fp, destination_dir)
            
        if os.path.isdir(current_content_fp):
            new_destination = os.path.join(destination_dir, content)
            os.mkdir(new_destination)
            copy_recursive(current_content_fp, new_destination)

def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            stripped_line = line.lstrip("#").strip()

            return stripped_line
        
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, mode="r") as markdown_file:
        markdown_text = markdown_file.read()

    with open(template_path, mode="r") as template_file:
        template_text = template_file.read()

    html_string = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(markdown_text)

    final_html = template_text.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    dir_name = os.path.dirname(dest_path)

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    content = os.listdir(dir_path_content)
    os.makedirs(dest_dir_path, exist_ok=True)

    for item in content:

        new_item = item[:-3] + ".html"
        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, dest_path)
        else:            
            if item.endswith("md"):
                new_item = item[:-3] + ".html"
                modified_dest_path = os.path.join(dest_dir_path, new_item)
                generate_page(path, template_path, modified_dest_path)
        
    


if __name__ == "__main__":
    main()
