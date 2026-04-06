import os
import shutil

def copy_static(source: str, destination: str, dest_clear:bool=False):
    if not dest_clear and os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"cleaing {destination}")
    if not os.path.exists(destination):
        os.mkdir(destination)
    dest_clear = True

    if not os.path.exists(source):
        raise OSError(f"Cannot Access {source}, no such file or directory")
    print("copying files")
    for file in os.listdir(source):
        filepath = source + file
        print(f"File: {filepath}")
        if os.path.isfile(filepath):
            shutil.copy(filepath, destination)
            print(f"copying file {filepath}, to {destination}")
        if os.path.isdir(filepath):
            print(f"entering {filepath} directory")
            copy_static(filepath + "/", destination+file+"/", True)
            print(f"exiting {filepath} directory")
