import os
import uuid
import shutil
import pathlib
import config

def clean_up(dir):
    try:
        for file in os.listdir(dir):
            fpath = os.path.join(dir, file)
            os.remove(fpath)
            print("Cleanup:", file, "removed")
    except FileNotFoundError:
        print("No such directory exists: %s" % dir)


def create_dir(dir) -> str:
    parentPath = '.'
    # path = os.path.join(parentPath, dir)
    path = dir
    try:
        os.mkdir(path)
    except FileExistsError:
        clean_up(path)
    except FileNotFoundError:
        print(FileNotFoundError)
    finally:
        return path


def create_report_folder(filename) -> str:
    fname = filename.split('.')[0]
    # homedir   = pathlib.Path(os.environ["USERPROFILE"])
    # targetdir = pathlib.Path(f'./data/reports/{fname}/')
    targetdir = pathlib.Path(config.REPORTSFOL) / fname
    try:
        os.makedirs(targetdir)
    except:
        clean_up(targetdir)
    return targetdir


def create_raw_folder() -> None:
    # targetdir = f'./data/raw/'
    targetdir = pathlib.Path(config.RAWFOL)
    os.makedirs(targetdir, exist_ok=True)


def upload_to_raw_folder(filepath: str) -> str:
    # function to return the file extension
    targetdir = pathlib.Path(config.RAWFOL)
    sourcefile = pathlib.Path(filepath)
    extension = sourcefile.suffix
    crypticname = str(uuid.uuid1()) + extension
    destfile = targetdir / crypticname
    # destination = os.join(targetdir, str(uuid.uuid1()))

    # source = r"E:\demos\files\reports\profit.txt"
    # destination = r"E:\final\reports\profit.txt"
    # open source file in read mode
    # with open(sourcefile, "r") as inp:
        # open destination path in write mode
        # with open(destfile, "w") as out:
            # copy file
            # shutil.copyfileobj(inp, out)
    shutil.copy2(sourcefile, destfile)
    print("Copied", crypticname, destfile, extension)


    return crypticname