import sys
from enums import *
from pagegen import gen_content
from sitegen import copy_static

def main() -> None:
    basepath = ""
    if sys.argv:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print("Running Static site Generator")
    copy_static(STATIC_PATH, PUBLIC_PATH)

    gen_content(CONTENT_PATH,TEMPLATE, PUBLIC_PATH, basepath=basepath)

if __name__ == "__main__":
    main()
