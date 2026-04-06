import os
import shutil

from pagegen import generate_page
from sitegen import copy_static

STATIC_PATH = "/home/zalea/Documents/Projects/bootdev/staticsite/static/"
PUBLIC_PATH = "/home/zalea/Documents/Projects/bootdev/staticsite/public/"

def main() -> None:
    print("Running Static site Generator")
    copy_static(STATIC_PATH, PUBLIC_PATH)

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
