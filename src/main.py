import os
import sys
import shutil
from markdown_blocks import markdown_to_html_node

dir_path_public = "./docs/"
dir_path_static = "./static/"
dir_path_template = "./template.html"
dir_path_content = "./content/"

def main():

    basepath = "/" if len(sys.argv) <= 1 else sys.argv[1]

    clear_directory(dir_path_public)
    copy_tree(dir_path_static, dir_path_public)

    generate_pages_rec(dir_path_content, dir_path_template, dir_path_public, basepath)



def clear_directory(path: str):
    if not os.path.exists(path):
        return

    if not os.path.isdir(path):
        raise Exception(f"not a directory: '{e}'")

    print(f"delete '{path}'")
    shutil.rmtree(path)


def copy_tree(src_dir: str, dst_dir: str):
    if not os.path.exists(src_dir):
        raise Exception(f"path does not exist: '{src_dir}'")

    if not os.path.exists(dst_dir):
        print(f"create '{dst_dir}'")
        os.mkdir(dst_dir)

    for e in os.listdir(src_dir):
        src = os.path.join(src_dir, e)
        dst = os.path.join(dst_dir, e)
        if os.path.isfile(src):
            print(f"copy '{src}' => '{dst}'")
            shutil.copy(src, dst)
        elif os.path.isdir(src):
            copy_tree(src, dst)

def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title found")

def generate_pages_rec(content_path: str, template_path: str, dst_path: str, basepath: str):
    for filename in os.listdir(content_path):
        src = os.path.join(content_path, filename)
        dst = os.path.join(dst_path, filename)
        if filename.endswith(".md") and os.path.isfile(src):
            dst = dst.rstrip(".md") + ".html"
            generate_page(src, template_path, dst, basepath)
        elif os.path.isdir(src):
            os.mkdir(dst)
            generate_pages_rec(src, template_path, dst, basepath)


def generate_page(src_path: str, template_path: str, dst_path: str, basepath: str):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")

    with open(src_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    # content replacements
    generated = template.replace("{{ Title }}", title)
    generated = generated.replace("{{ Content }}", content)
    # link replacements
    generated = generated.replace('href="/', f'href="{basepath}')
    generated = generated.replace('src="/', f'src="{basepath}')

    with open(dst_path, "w") as f:
        f.write(generated)



if __name__ == "__main__":
    main()
