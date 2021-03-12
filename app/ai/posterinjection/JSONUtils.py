

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
			# isPosterInjection=True
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

	return reference_point, left, right, top, bottom, framenum, fr_w, fr_h,frame

# #Function to get the upper and lower hsv range of values
# def get_hsv_range(currHSV, firstHSV):

# 	threshold = 40

# 	if (currHSV[0] not in range(firstHSV[0]-5, firstHSV[0]+5)) and (currHSV[2] not in range(firstHSV[2]-5, firstHSV[2]+5)):
# 		currHSV = firstHSV

# 	lower = np.array([0, currHSV[1] - threshold, currHSV[2] - threshold])
# 	upper = np.array([255, currHSV[1] + threshold, currHSV[2] + threshold])

# 	return lower, upper





########################################################################################3
import cv2
import dlib
import numpy as np

# Threshold for the upper and lower hsv bound
hsv_threshold = 40

# Kernels for image dilation or erosion
kernel1 = np.ones((1, 1), np.uint8)
kernel3 = np.ones((3, 3), np.uint8)
kernel2 = np.ones((2,2), np.uint8)

# Bias to avoid zero-division error
bias = 0.00001


def check_camera_motion(prev_frame, curr_frame):
	"""
	This function checks whether there is camera motion or not.

	Parameters
	----------
	prev_frame: numpy.ndarray
		Previous raw video frame
	curr_frame: numpy.ndarray
		Current raw video frame

	Returns
	-------
	motion_flag: bool
		True if motion is detected
		False if motion is not detected

	"""
	fr_ht = curr_frame.shape[0]  # Height of the current frame
	fr_wt = curr_frame.shape[1]  # Width of the current frame

	cols = int(fr_wt * 0.02)  # This gives the number of columns to be evaluated	(2% of width)
	rows = int(fr_ht * 0.02)  # This gives the number of rows to be evaluated		(2% of height)

	left_top_arr_curr = curr_frame[:rows, :cols] / 255
	right_top_arr_curr = curr_frame[:rows, -cols - 1:-1] / 255
	left_bot_arr_curr = curr_frame[-rows - 1:-1, :cols] / 255
	right_bot_arr_curr = curr_frame[-rows - 1:-1, -cols - 1:-1] / 255

	left_top_arr_prev = (prev_frame[:rows, :cols] / 255) + bias
	right_top_arr_prev = (prev_frame[:rows, -cols - 1:-1]) / 255 + bias
	left_bot_arr_prev = (prev_frame[-rows - 1:-1, :cols]) / 255 + bias
	right_bot_arr_prev = (prev_frame[-rows - 1:-1, -cols - 1:-1]) / 255 + bias

	left_top_pc = ((left_top_arr_curr - left_top_arr_prev) / left_top_arr_prev).flatten()
	right_top_pc = ((right_top_arr_curr - right_top_arr_prev) / right_top_arr_prev).flatten()
	left_bot_pc = ((left_bot_arr_curr - left_bot_arr_prev) / left_bot_arr_prev).flatten()
	right_bot_pc = ((right_bot_arr_curr - right_bot_arr_prev) / right_bot_arr_prev).flatten()

	avg_left_top_pc = np.abs(np.mean(left_top_pc))
	avg_right_top_pc = np.abs(np.mean(right_top_pc))
	avg_left_bot_pc = np.abs(np.mean(left_bot_pc))
	avg_right_bot_pc = np.abs(np.mean(right_bot_pc))

	if (avg_left_top_pc > 0.03) and (avg_right_top_pc > 0.03) and (avg_left_bot_pc > 0.03) and (avg_right_bot_pc > 0.03):
		# print("Camera Motion Detected!!!")
		motion_flag = True

	else:
		print("No Camera Motion.")
		motion_flag = False

	return motion_flag


def refine_mask(mask):
	"""
	This function refines the binary mask with proper fg-bg segmentation

	Parameters
	----------
	mask: numpy.ndarray
		Binary mask to be refines

	Returns
	-------
	mask: numpy.ndarray
		Refines binary mask

	"""
	mask_ht, mask_wt = mask.shape

	left_border_pixels_set = {(0, ht) for ht in range(mask_ht)}
	right_border_pixels_set = {(mask_wt - 1, ht) for ht in range(mask_ht)}
	top_border_pixels_set = {(wt, 0) for wt in range(mask_wt)}
	bottom_border_pixels_set = {(wt, mask_ht - 1) for wt in range(mask_wt)}
	united_sets = left_border_pixels_set | right_border_pixels_set | top_border_pixels_set | bottom_border_pixels_set

	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	for contour in contours:
		contour_pixels_set = {tuple(coord.flatten().tolist()) for coord in contour}

		# Intersection of Sets
		intersection = united_sets & contour_pixels_set

		if not intersection:
			cv2.fillConvexPoly(mask, contour, (0, 0, 0))

	return mask


def generate_fine_mask(frame, reference_point, first_hsv):
	"""
	Function generates the fine binary mask

	Parameters
	----------
	frame: numpy.ndarray
		Raw Video Frame
	reference_point: tuple (y, x)
		Point to find the HSV range
	first_hsv: numpy.ndarray
		HSV values of the first frame

	Returns
	-------
	mask: numpy.ndarray
		Binary mask of the raw video frame

	"""

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	curr_hsv = hsv[reference_point]

	if (curr_hsv[0] not in range(first_hsv[0] - 2, first_hsv[0] + 2)) and \
		(curr_hsv[2] not in range(first_hsv[2] - 2, first_hsv[2] + 2)):
		curr_hsv = first_hsv

	lower = np.array([0, curr_hsv[1] - hsv_threshold, curr_hsv[2] - hsv_threshold])
	upper = np.array([179, curr_hsv[1] + hsv_threshold, curr_hsv[2] + hsv_threshold])

	mask = cv2.inRange(hsv, lower, upper)

	mask = cv2.dilate(mask, kernel1, iterations=5)
	# mask = cv2.erode(mask, kernel2, iterations=1)

	# Refining the mask
	mask = refine_mask(mask)
	mask = refine_mask(mask)

	# mask = cv2.erode(mask, kernel2, iterations=3)
	mask = cv2.dilate(mask, kernel2, iterations=3)

	return mask


def check_noisy_bg(mask, fr_w, fr_h):
	"""
	Function to check whether the background is noisy or not

	Parameters
	----------
	mask: numpy.ndarray
		Binary mask of the targeted video frame
	fr_h: int
		Height of the targeted video frame
	fr_w: int
		Width of the targeted video frame

	Returns
	-------
	noise_flag: bool
		True if background is noisy
		False if background is clean

	"""
	left_part = list(mask[int(fr_h * 0.01): int(fr_h * 0.05), int(fr_w * 0.01): int(fr_w * 0.05)].flatten())
	right_part = list(mask[int(fr_h * 0.01): int(fr_h * 0.05), int(fr_w * 0.94): int(fr_w * 0.99)].flatten())

	# Important Note:
	# Don't try to add the numpy array, because it will parse as matrix and add individual elements

	noise_thresh_left = len(left_part) * 0.05
	zero_count_left = left_part.count(0)

	noise_thresh_right = len(right_part) * 0.05
	zero_count_right = right_part.count(0)

	if (zero_count_left >= noise_thresh_left) or (zero_count_right >= noise_thresh_right):
		print("Noisy Background!!!")
		noise_flag = True
	else:
		print("Clean Background!!!")
		noise_flag = False

	return noise_flag


def process_frame(poster, frame, cropped_frame, cropped_mask, left, right, top, bottom):
	"""
	This function injects the poster onto the targeted area.

	Parameters
	----------
	poster: numpy.ndarray
		Poster with the size of the targeted injection area
	frame: numpy.ndarray
		Raw Video Frame
	cropped_frame: numpy.ndarray
		Targeted area of the video frame
	cropped_mask: numpy.ndarray
		Mask of the targeted area
	left: int
		Left position of the injection area (x1)
	right: int
		Right position of the injection area (x2)
	top: int
		Top position of the injection area (y1)
	bottom: int
		Bottom position of the injection area (y2)

	Returns
	-------
	frame: numpy.ndarray
		Processed Frame with injection

	"""

	poster_copy = poster.copy()
	poster_copy[cropped_mask == 0] = 1
	cropped_frame[cropped_mask != 0] = 1
	cropped_frame = cropped_frame * poster_copy
	frame[top: bottom, left: right, :] = cropped_frame

	return frame


def find_occluded_coords(cropped_mask, left, top):
	cropped_mask_inv = 255 - cropped_mask
	contours, _ = cv2.findContours(cropped_mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	bounding_coordinates = []
	if not contours:
		return bounding_coordinates

	else:
		# Note: Convert to integer to avoid "integer serializable JSON Error"
		bounding_coordinates = [[int(left + contour[0][0]), int(top + contour[0][1])] for contour in contours[0]]

		return bounding_coordinates
