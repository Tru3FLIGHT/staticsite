import os
import shutil

from sitegen import copy_static

STATIC_PATH = "/home/zalea/Documents/Projects/bootdev/staticsite/static/"
PUBLIC_PATH = "/home/zalea/Documents/Projects/bootdev/staticsite/public/"

def main() -> None:
    print("Running Static site Generator")
    for path in os.listdir(STATIC_PATH):
        print(path)
    copy_static(STATIC_PATH, PUBLIC_PATH)

if __name__ == "__main__":
    main()
