from app import app,db
from app.database.models import UploadedVideo
from flask import request,jsonify,json
import urllib.request
from werkzeug.utils import secure_filename
from datetime import datetime
from .ai.posterinjection.video_parser import extractVideoPosterInjectionData
from .utils.file_validation import *

@app.route('/analyse-video', methods=["POST"])
def analyse_video():
    try:       
        if request.method == 'POST':
            ########################## Validation ###########################
            if not request.form.get("API_KEY")==app.config['API_KEY']:
                message ="Invalid api key"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ),403

            _videoUploadTime=datetime.utcnow()
            startingdt_string = _videoUploadTime.strftime("%Y%m%d%H%M%S")

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

            _videoPath=os.path.join(app.config["VIDEO_POSTER_INJECTION_UPLOADS_FOLDER"], _newVideoName)
            print(f"Video {_newVideoName} Saving Started ....")
            video.save(_videoPath)
            print(f"Video {_newVideoName} Saving Completed ....")

            ###################### Video is saved till now ###########################

            if not isVideoFilesizeAllowed(getFileSize(_videoPath)):
                message="Videosize exceeded maximum limit"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ), 400

            ###################### Validation complete Video will be processed now ###########################
            
            jsonFileName,withAudioOutputFileName = extractVideoPosterInjectionData(_newBaseName,_extension,_newVideoName,_videoPath)
            print()
            generatedVideoTime=datetime.utcnow()
            gen_video_dt_string = generatedVideoTime.strftime("%Y%m%d%H%M%S")
            generatedvideoname = gen_video_dt_string+"_generated_"+_newVideoName.split('.')[0]

            _uploadedVideo = UploadedVideo(filename = withAudioOutputFileName,uploadStartedTime = _videoUploadTime,uploadCompletedTime=generatedVideoTime,analyticsFileName=jsonFileName,generatedVideoFileName=withAudioOutputFileName)
            db.session.add(_uploadedVideo)
            db.session.commit()

        message = "Successfully uploaded...."
        print(message)
        return jsonify(
            status="Success",
            message=message,
            videoId=_uploadedVideo.videoid
            ), 200

    except Exception as err:
        message = "Problem while uploading....Please try with next video..."
        print(err)
        return jsonify(
            status="Error",
            message=message
            ), 400

@app.route('/get-json', methods=["POST"])
def get_json():
    try:       
        if request.method == 'POST':
            ########################## Validation ###########################
            if not request.form.get("API_KEY")==app.config['API_KEY']:
                message ="Invalid api key"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ),403

            if not request.form.get("videoId"):
                message ="Please provide proper videoid"
                print(message)
                return jsonify(
                    status="Error",
                    message=message
                    ),400

        _uploadedVideo = UploadedVideo.query.filter_by(videoid=request.form.get("videoId")).first()

        filename = _uploadedVideo.analyticsFileName
        message="Successfully fetched"
        print(message)
        return json.load(open(f"{app.config['VIDEOANALYTICS_POSTER_INJECTION_GENERATED_FOLDER']}/{filename}"))

    except Exception as err:
        message = "Problem while fetching json."
        print(err)
        return jsonify(
            status="Error",
            message=message
            ),500
