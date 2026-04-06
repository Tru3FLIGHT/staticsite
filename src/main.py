import os
import shutil

from pagegen import generate_page
from sitegen import copy_static

STATIC_PATH = "static/"
PUBLIC_PATH = "public/"
CONTENT_PATH = "content/"
TEMPLATE = "template.html"

def main() -> None:
    print("Running Static site Generator")
    copy_static(STATIC_PATH, PUBLIC_PATH)

    gen_content(CONTENT_PATH, PUBLIC_PATH)

def gen_content(content_dir:str, destination:str):
    for file in os.listdir(content_dir):
        fullpath = content_dir + file
        print(fullpath)
        if os.path.isdir(fullpath):
            gen_content(content_dir+file+"/", destination+file+"/")
        if file == "index.md":
            generate_page(fullpath, TEMPLATE, destination+"index.html")

if __name__ == "__main__":
    main()
