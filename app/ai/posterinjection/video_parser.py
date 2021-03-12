import cv2
import numpy as np
import os
import json
import moviepy.editor as mpe

# from .occlusion import *
from .JSONUtils import *
from app import app

outputVideoPath= app.config['VIDEO_POSTER_INJECTION_GENERATED_FOLDER']


import glob
import random


def extractVideoPosterInjectionData(__newBaseName,_extension,_newVideoName,_videoPath):

    posters = glob.glob(f"{app.config['ADIMAGE_POSTER_INJECTION_UPLOADS_FOLDER']}/*.jpg")
    random_image = random.choice(posters)
    poster = cv2.imread(random_image)
    cap = cv2.VideoCapture(_videoPath)

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
    reference_point, left, right, top, bottom, framenum, fr_w, fr_h,prevFrame= get_reference_point(cap, poster, fps, out, fr_w, fr_h)


#region new ##############################

	# Resizing the poster with the size of the target area
    poster = cv2.resize(poster, (right - left, bottom - top))

    # Getting the first HSV
    hsv = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2HSV)

    first_hsv = hsv[reference_point]

    ''' Until here we have the reference point and the four positions of the poster to be overlaid! '''

	# Initializing the required variables and data structures
    count_motion = 0
    count_idle = 0
    noise_flag = True
    posterData = list()
    posterFlag = 0
    poster_start_switch = True
    posterStartTime = 0
    frameTime = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Resetting the occluded_coords_list in every loop
        occluded_coords_list = list()

        frameTime = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        motion_flag = check_camera_motion(prevFrame, frame)
        prevFrame = frame

        '''We increase the value of the count_motion if motion is detected!
            And reset count_motion if motion is not detected! 
            Similarly, for count_idle'''

        if motion_flag:
            count_motion += 1

        else:
            count_idle += 1
            count_motion = 0

        if count_motion > 05.00:

            print("Motion Detected!!!")
            noise_flag = True  # Noise flag is set to True, which enables the checking bg after motion is stabilized

            count_idle = 0

            # After the motion is detected, we reset the first_hsv point until the video is stabilized
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            first_hsv = hsv[reference_point]

            out.write(frame)
            # cv2.imshow("frame", frame)
            # if cv2.waitKey(1) in [ord('q') or ord('Q')]:
            # 	break

            continue

        '''Now we check whether the video is idle for 2 seconds! If the video is idle for more than 2 seconds,
            then we again try to project the poster!!!'''
        if count_idle > fps * 2:

            # Cropping the targeted area from the raw video frame
            # This is the area where we inject the poster
            cropped_frame = frame[top: bottom, left: right, :]

            # Creating the fine mask of the video frame segregating the foreground and background
            mask = generate_fine_mask(frame, reference_point, first_hsv)

            # if noise_flag:
            # 	# Checking the noisy background
            # 	noise_flag = check_noisy_bg(mask, fr_w, fr_h)

            # 	out.write(frame)
            # 	cv2.imshow("frame", frame)
            # 	if cv2.waitKey(1) in [ord('q'), ord('Q')]:
            # 		break

            # 	continue

            # Extracting the region of interest from the mask
            cropped_mask = mask[top: bottom, left: right]
            # cv2.imshow("crop", cropped_mask)

            if poster_start_switch:
                posterFlag = 1
                posterStartTime = frameTime
                poster_start_switch = False

            occluded_coords_list = find_occluded_coords(cropped_mask, left, top)

            if occluded_coords_list:
                occlusion_dict = dict()
                occlusion_dict["timeInMilliSec"] = frameTime
                occlusion_dict["occlusionCoords"] = occluded_coords_list
                posterData.append(occlusion_dict)

            # Injecting the poster onto the target area since there is no noise and video is stable
            frame = process_frame(poster, frame, cropped_frame, cropped_mask, left, right, top, bottom)

        out.write(frame)
        # cv2.imshow("frame", frame)
        # if cv2.waitKey(1) in [ord('q'), ord('Q')]:
            # break

    cap.release()
    out.release()
#endregion##################

    # if not os.path.exists("Output JSON"):
    #     os.mkdir("Output JSON")

    # Generating the final data for JSON
    if posterFlag:
        # isPosterInjected=True
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
        # isPosterInjected=False
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
    videoWithAudio = mpe.VideoFileClip(_videoPath)
    posterVideoWithoutAudio = mpe.VideoFileClip(outputVideoPath + f"/{tempNoAudioFileName}")
    audio_bg = videoWithAudio.audio
    posterVideoWithAudio = posterVideoWithoutAudio.set_audio(audio_bg)
    posterVideoWithAudio.write_videofile(outputVideoPath + f"/{withAudioOutputFileName}")

    if os.path.isfile(outputVideoPath + f"/{tempNoAudioFileName}"):
        os.remove(outputVideoPath + f"/{tempNoAudioFileName}")
    
    return jsonFileName,withAudioOutputFileName,posterFlag
