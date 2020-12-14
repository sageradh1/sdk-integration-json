import cv2
import numpy as np
import os
import json
import moviepy.editor as mpe

from .occlusion import *
from .JSONUtils import *
from app import app

outputVideoPath= app.config['VIDEO_POSTER_INJECTION_GENERATED_FOLDER']

def extractVideoPosterInjectionData(__newBaseName,_extension,_newVideoName,_videoFulllPath):
    isPosterInjected=False
    poster = cv2.imread(f"{app.config['ADIMAGE_POSTER_INJECTION_UPLOADS_FOLDER']}/easports.jpg")
    cap = cv2.VideoCapture(_videoFulllPath)

    # fps, width and height of the current video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fr_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fr_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    tempNoAudioFileName=f"{__newBaseName}_no_Audio.mp4"
    withAudioOutputFileName=f"injected_{__newBaseName}.mp4"
    jsonFileName=f"{__newBaseName}.json"
    # object to writing the output video
    out = cv2.VideoWriter(outputVideoPath + f"/{tempNoAudioFileName}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (fr_w, fr_h))

    # Getting the reference point from the function in utils
    reference_point, left, right, top, bottom, framenum, fr_w, fr_h,isPosterInjected= get_reference_point(cap, poster, fps, out, fr_w, fr_h)

    #Initializing the different switches and Flags
    HSVSwitch = True
    gijiFlag = True
    posterFlag = 0
    firstFrameSwitch = True
    posterStartSwitch = True

    # List for the occlusion Coordinates
    posterData = list()

    # Looping over all the video frames
    while True:
        # Reading the frames
        ret, frame = cap.read()

        # Break condition at the end of the video
        if not ret:
            break 

        frameTime = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        if firstFrameSwitch:
            firstFrameSwitch = False
            firstFrameTime = frameTime//1000

        # Extracting the target-area from the frame to inject the poster
        area = frame[top:bottom, left:right, :]

        # Resizing the poster as per the defined area above. Note: cv2.resize() takes in as (w,h)
        poster = cv2.resize(poster, (right - left, bottom - top))
        
        # Convert the whole frame into HSV COLORSPACE
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Getting the HSV values of the reference point
        currHSV = hsv[reference_point]

        if HSVSwitch:
            HSVSwitch = False
            firstHSV = currHSV

        # Getting the lower and upper values using the function from utils
        lower, upper = get_hsv_range(currHSV, firstHSV)

        # Create kernel for image dilation
        kernel = np.ones((1,1), np.uint8)

        # Creating the mask using for the HSV frame using the upper and lower values
        mask = cv2.inRange(hsv, lower, upper)

        # Perform dilation on the mask to reduce noise
        dil = cv2.dilate(mask, kernel, iterations=5)
        
        # To check whether there is gijigiji or not
        if gijiFlag:
            # We check giji giji at t sec, t + 10 sec and t + 20 sec
            if frameTime//1000 in [firstFrameTime, firstFrameTime + 10, firstFrameTime + 20]:
                gijiFlag = checkGijiGiji(dil, fr_w, fr_h)

            out.write(frame)
            frame = cv2.resize(frame, None, fx=0.5, fy = 0.5)
            # cv2.imshow('frame', frame)
            print(f"Frame {framenum}: Done!")
            framenum += 1

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            continue

        # At this point, we are sure that the poster gets injected into the video
        if posterStartSwitch:
            posterFlag = 1
            posterStartTime = frameTime
            posterStartSwitch = False

        # Now extract the area from the HSV frame with individual 3 channels
        mini_dil = np.zeros_like(area)
        mini_dil[:, :, 0] = dil[top: bottom, left: right]
        mini_dil[:, :, 1] = dil[top: bottom, left: right]
        mini_dil[:, :, 2] = dil[top: bottom, left: right]

        # Checking the occlusion and getting the occluded coordinates at every 10 frame
        if framenum % 10 == 0:
            occlusionCoordinatesList = findOcclusionCoordinates(frame, mini_dil, fr_h, fr_w)

            if occlusionCoordinatesList:
                occlusionDict = dict()
                occlusionDict["timeInMilliSec"] = frameTime
                occlusionDict["occlusionCoords"] = occlusionCoordinatesList
                posterData.append(occlusionDict)

        # Create the copy of the poster
        poster_copy = poster.copy()

        # Set pixel values of the poster_coy to 1 where pixel value of the mask is 0
        poster_copy[mini_dil == 0] = 1

        # Now set the pixel values in the target area to 1 where the pixel values of the poster_copy is not 1
        area[mini_dil != 0] = 1

        # Merge the poster_copy and the target area
        area = area * poster_copy

        # Now insert the final poster into the main frame
        frame[top: bottom, left:right, :] = area
        out.write(frame)
        frame = cv2.resize(frame, None, fx=0.5, fy = 0.5)
        
        # Showing the final frame 
        # cv2.imshow('frame', frame)
        print(f"Frame {framenum}: Done!")
        framenum += 1

        # Waiting for the key to be pressed by the user. If key is 'q' then quit everything
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()

    # if not os.path.exists("Output JSON"):
    #     os.mkdir("Output JSON")

    # Generating the final data for JSON
    if posterFlag:
        isPosterInjected=True
        finalData = {

            "dataForVideo":
                {
                    "endPoint": f"{app.config['API_BASE_URL']}/{app.config['VIDEO_POSTER_INJECTION_GENERATED_RELATIVEPATH_FOLDER']}/{withAudioOutputFileName}",
                    "videoResolutionX": fr_w,
                    "videoResolutionY": fr_h
                },

            "posterForVideo": [
            {
                "posterFlag": posterFlag,
                "posterWidth": right-left,
                "posterHeight": bottom-top,
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom,
                "posterStart": posterStartTime,
                "posterEnd": frameTime,
                "posterURL": "asmi.co",
                "posterImageUrl": f"{app.config['API_BASE_URL']}/{app.config['ADIMAGE_POSTER_INJECTION_RELATIVEPATH_FOLDER']}/easports.jpg",
                "posterData": posterData,
                }
            ]
        }
    else:
        isPosterInjected=False
        finalData = {
            "dataForVideo":
                {
                    "endPoint": f"{app.config['API_BASE_URL']}/{app.config['VIDEO_POSTER_INJECTION_UPLOADS_RELATIVEPATH_FOLDER']}/{_newVideoName}",
                    "videoResolutionX": fr_w,
                    "videoResolutionY": fr_h
                },
            "posterForVideo": [
            {
                "posterFlag": 0,
                "posterWidth": None,
                "posterHeight": None,
                "left": None,
                "top": None,
                "right": None,
                "bottom": None,
                "posterStart": None,
                "posterEnd": None,
                "posterURL": None,
                "posterImageUrl": None,
                "posterData": None,
                }
            ]
        }

    with open(f"{app.config['VIDEOANALYTICS_POSTER_INJECTION_GENERATED_FOLDER']}/{jsonFileName}", "w") as f:
        json.dump(finalData, f, indent=3)

    # Generating final video with audio // Make sure you run the whole video
    videoWithAudio = mpe.VideoFileClip(_videoFulllPath)
    posterVideoWithoutAudio = mpe.VideoFileClip(outputVideoPath + f"/{tempNoAudioFileName}")
    audio_bg = videoWithAudio.audio
    posterVideoWithAudio = posterVideoWithoutAudio.set_audio(audio_bg)
    posterVideoWithAudio.write_videofile(outputVideoPath + f"/{withAudioOutputFileName}")

    if os.path.isfile(outputVideoPath + f"/{tempNoAudioFileName}"):
        os.remove(outputVideoPath + f"/{tempNoAudioFileName}")
    
    return jsonFileName,withAudioOutputFileName,isPosterInjected