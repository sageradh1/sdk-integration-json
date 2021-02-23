import cv2
import dlib
import numpy as np

def checkGijiGiji(checkDil, fr_w, fr_h):

	leftPart = list(checkDil[0: int(fr_h * 0.10), 0: int(fr_w * 0.10)].flatten())
	rightPart = list(checkDil[0: int(fr_h * 0.10), (fr_w - int(fr_w * 0.10)): fr_w].flatten())
	
	finalGiji = leftPart + rightPart
	# Note: 
	# Don't try to add the numpy array, because it will parse as matrix and add individual elements -> So We convert into a list

	threshGijiCount = len(finalGiji) * 0.10
	finalGijiCount = finalGiji.count(0)
	
	if finalGijiCount >= threshGijiCount:
		print("Giji Giji Xa")
		gijiFlag = True
	else:
		print("Giji Giji Xaina")
		gijiFlag = False
	
	return gijiFlag

def get_reference_point(cap, poster, fps, out, fr_w, fr_h):
	isPosterInjection=False
	reference_point = 0,0
	left, right, top, bottom, framenum = 0,0,0,0,0
	# Shape of the poster
	pos_h, pos_w, _ = poster.shape
	ratio = pos_h/pos_w

	# Initializing to print the frame number
	framenum = 1

	# Initializing Face Detector
	detector = dlib.get_frontal_face_detector()

	# Setting up the switch: Switch is disabled as soon as a face is detected
	switch = True

	# Getting the center coordinates of the frame to check the placement of the poster
	fr_xc, fr_yc = fr_w//2, fr_h//2

	while True:

		# Reading the frames
		ret, frame = cap.read()

		# Break condition at the end of the video
		if not ret:
			break

		# Getting the faces in the frame
		faces = detector(frame)

		# If there is no any face and switch is True, then do nothing, just continue the loop
		if (not faces) and switch:
			out.write(frame)
			frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5)
			# cv2.imshow('frame', frame)
			print(f"Frame {framenum}: No Face Detected!")
			framenum += 1

			key = cv2.waitKey(1)
			if key == ord('q'):
				cv2.destroyAllWindows()
				break
				cap.release()

			continue

		# If there is a face and switch is True, get the top-left and bottom-right coordinates of the face and make switch False
		# Note: We define the injecting area as per the location of the face
		if faces and switch:
			isPosterInjection=True
			# Looping over the faces in the frame
			for face in faces:

				# Switch is False as the face is detected
				switch = False

				# Getting the x1,y1 and x2,y2 coordinates of the face detected
				x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

				# Getting the center coordinates of the face rectangle
				fc_xc, fc_yc = (x1 + x2)//2, (y1 + y2)//2

				#If the face-center is less than frame center (in the left side), then poster is injected on the right. And vice versa
				if fc_xc < fr_xc:
					print('Face on left and poster on right')
											#0.12			 #0.90
					top, right = int(fr_h * 0.05), int(fr_w * 0.92)

					if (fr_h >= fr_w) and (pos_h >= pos_w):
						print("Frame and poster both are potrait")
						left = right - int(fr_w//4)		# //2.3
						bottom = top + int((right-left) * ratio)

					elif (fr_h >= fr_w) and (pos_h < pos_w):
						print("Frame is potrait and poster is landscape")
						bottom = top + int(fr_w//4)		# //2.3
						left = right - int((bottom - top) / ratio)

					elif (fr_h < fr_w) and (pos_h >= pos_w):
						print("Frame is landscape and poster is potrait")
						left = right - int(fr_h//4)		# //2.3 
						bottom = top + int((right - left) * ratio)

					else:
						print("Frame and poster both are landscape")
						bottom = top + int(fr_h//4)		# //2.3
						left = right - int((bottom - top) / ratio)

					reference_point = top, right

				else:
					print('Face on right and poster on left')
										  # 0.12		   # 0.10	
					top, left = int(fr_h * 0.05), int(fr_w * 0.08)

					if (fr_h >= fr_w) and (pos_h >= pos_w):
						print("Frame and poster both are potrait")
						right = left + int(fr_w//4)		# //2.2
						bottom = top + int((right - left) * ratio)

					elif (fr_h >= fr_w) and (pos_h < pos_w):
						print("Frame is potrait and poster is landscape")
						bottom = top + int(fr_w//4)		# //2.2
						right = left + int((bottom - top) / ratio) 

					elif (fr_h < fr_w) and (pos_h >= pos_w):
						print("Frame is landscape and poster is potrait")
						right = left + int(fr_h//4)		# //2.2 
						bottom = top + int((right - left) * ratio)

					else:
						print("Frame and poster both are landscape")
						bottom = top + int(fr_h//4)		# //2.2
						right = left + int((bottom - top) / ratio)

					reference_point = top, left
		else:
			break

	return reference_point, left, right, top, bottom, framenum, fr_w, fr_h,isPosterInjection

#Function to get the upper and lower hsv range of values
def get_hsv_range(currHSV, firstHSV):

	threshold = 40

	if (currHSV[0] not in range(firstHSV[0]-5, firstHSV[0]+5)) and (currHSV[2] not in range(firstHSV[2]-5, firstHSV[2]+5)):
		currHSV = firstHSV

	lower = np.array([0, currHSV[1] - threshold, currHSV[2] - threshold])
	upper = np.array([255, currHSV[1] + threshold, currHSV[2] + threshold])

	return lower, upper