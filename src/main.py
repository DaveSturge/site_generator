from textnode import TextNode, TextType
import shutil, os

def main():
    copy_static()

def copy_static():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")

    copy_recursive("static", "public")

def copy_recursive(current_dir, destination_dir):

    static_contents = os.listdir(current_dir)

    for content in static_contents:
        current_content_fp = os.path.join(current_dir, content)

        if os.path.isfile(current_content_fp):
            print(f"{content} is a file")

            shutil.copy(current_content_fp, destination_dir)
            

        if os.path.isdir(current_content_fp):
            print(f"{content} is a directory")

            new_destination = os.path.join(destination_dir, content)

            os.mkdir(new_destination)

            copy_recursive(current_content_fp, new_destination)

if __name__ == "__main__":
    main()
