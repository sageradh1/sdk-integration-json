import os
from app import app

def isVideoNameAllowedWithExtension(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    counter = filename.count('.')

    if counter == 1: 
        # Split the extension from the filename
        ext = filename.rsplit(".", 1)[1]
        # Check if the extension is in ALLOWED_VIDEO_EXTENSIONS
    else:
        temp = filename.split(".")
        ext = temp[counter]

    if ext.lower() in app.config["ALLOWED_VIDEO_EXTENSIONS"]:
        return True,ext
    else:
        return False,ext

def isVideoNameAllowed(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False

    counter = filename.count('.')
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    if counter == 1: 
        if ext.lower() in app.config["ALLOWED_VIDEO_EXTENSIONS"]:
            return True
        else:
            return False
    else:
        return False

def getFileSize(filePath):
    return os.stat(filePath).st_size

def isVideoFilesizeAllowed(videosize):
    if int(videosize) <= app.config["MAX_VIDEO_FILESIZE"]:
        return True
    else:
        return False
