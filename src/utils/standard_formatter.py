import datetime
import os


def format_filename(filename):
    return filename.format(str(datetime.datetime.now()).replace(':', '').replace(" ", '-').replace(".", "-"))


def ip_files_cleanup():
    bashCommand = "rm ip_old.txt ip_new.txt"
    os.system(bashCommand)
