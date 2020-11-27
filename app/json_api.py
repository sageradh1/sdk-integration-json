from app import app
from flask import request,jsonify,make_response,redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename
from datetime import datetime


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


@app.route('/analyse-video', methods=["POST"])
def analyse_video():
    try:       
        if request.method == 'POST':

            if not request.form.get("API_KEY")=="4tert234htkj45b6j45h":
                message ="Invalid api key"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ),403   

            _videoUploadStartingTime=datetime.utcnow()
            startingdt_string = _videoUploadStartingTime.strftime("%Y%m%d%H%M%S")

            if not request.files:
                message ="No files received "
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ), 400

            if ('video' not in request.files):    
                message ="File with key name video is missing"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ), 400


            video = request.files['video']

            if not isVideoNameAllowed(secure_filename(video.filename)):
                message="Please make sure video file is in valid format.There must be only one dot in the filename"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ), 400

            _newVideoName= startingdt_string+video.filename
            _newBaseName=startingdt_string+_newVideoName.split('.')[0]
            _extension=_newVideoName.split('.')[1]

            _videoPath=os.path.join(app.config["VIDEO_UPLOADS_FOLDER"], _newVideoName)
            print("Video Saving Started ....")
            video.save(_videoPath)
            print("Video Saving Completed ....")

            ###################### Video is saved till now ###########################

            if not isVideoFilesizeAllowed(getFileSize(_videoPath)):
                message="Videosize exceeded maximum limit"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ), 400

            _videoUploadCompletedTime=datetime.utcnow()

           
         
            generatedVideoStartingTime=datetime.utcnow()
            gen_video_dt_string = generatedVideoStartingTime.strftime("%Y%m%d%H%M%S")
            generatedvideoname = gen_video_dt_string+"_generated_"+_newVideoName.split('.')[0]

        message = "Successfully uploaded...."
        print(message)
        return jsonify(
            status="Success",
            message=message
            ), 200

    except Exception as err:
        message = "Problem while uploading....Please upload next video..."
        print(message)
        return jsonify(
            status="Error",
            message=str(err)
            ), 401
