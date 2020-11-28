from app import app
from flask import request, jsonify, make_response, redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename
from datetime import datetime
from .ai.posterinjection.video_parser import extractVideoPosterInjectionData
from .utils.file_validation import *


class CustomException(Exception):
    pass


@app.route('/analyse-video', methods=["POST"])
def analyse_video():
    error_code = 400
    message = ''
    try:
        if request.method == 'POST':
            ########################## Validation ###########################
            if not request.form.get("API_KEY") == "4tert234htkj45b6j45h":
                message = "Invalid api key"
                error_code = 403
                print(message)
                raise CustomException(message)

            _videoUploadStartingTime = datetime.utcnow()
            startingdt_string = _videoUploadStartingTime.strftime("%Y%m%d%H%M%S")

            if not request.files:
                message = "No files received "
                error_code = 400
                print(message)
                raise CustomException(message)

            if 'video' not in request.files:
                message = "File with key name video is missing"
                print(message)
                error_code = 400

            video = request.files['video']

            if not isVideoNameAllowed(secure_filename(video.filename)):
                message = "Please make sure video file is in valid format.There must be only one dot in the filename"
                error_code = 400
                print(message)

            _newVideoName = startingdt_string + video.filename
            _newBaseName = startingdt_string + _newVideoName.split('.')[0]
            _extension = _newVideoName.split('.')[1]

            _videoPath = os.path.join(app.config["VIDEO_POSTER_INJECTION_UPLOADS_FOLDER"], _newVideoName)
            print(f"Video {_newVideoName} Saving Started ....")
            video.save(_videoPath)
            print(f"Video {_newVideoName} Saving Completed ....")

            ###################### Video is saved till now ###########################

            if not isVideoFilesizeAllowed(getFileSize(_videoPath)):
                message = "Videosize exceeded maximum limit"
                print(message)
                error_code = 400

            ###################### Validation complete Video will be processed now ###########################

            extracted_json = extractVideoPosterInjectionData(_newBaseName, _extension, _newVideoName, _videoPath)

            _videoUploadCompletedTime = datetime.utcnow()

            generatedVideoStartingTime = datetime.utcnow()
            gen_video_dt_string = generatedVideoStartingTime.strftime("%Y%m%d%H%M%S")
            generatedvideoname = gen_video_dt_string + "_generated_" + _newVideoName.split('.')[0]

        message = "Successfully uploaded...."
        print(message)
        return jsonify(
            status="Success",
            message=message
        ), 200
    except CustomException:
        return jsonify(
            status="Error",
            message=message
        ), error_code

    except Exception as err:
        message = "Problem while uploading....Please try with next video..."
        print(message)
        return jsonify(
            status="Error",
            message=str(err)
        ),


@app.rout('/test', methods=["GET"])
def test_api():
    return jsonify(status='API works!!')
