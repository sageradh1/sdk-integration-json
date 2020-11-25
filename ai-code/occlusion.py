import cv2
import numpy as np

kernel = np.ones((3, 3), np.uint8)

def findOcclusionCoordinates(frame, mini_dil, fr_h, fr_w):

	mini_dil = cv2.erode(mini_dil, kernel, iterations=3)
	mini_dil_gray = cv2.cvtColor(mini_dil, cv2.COLOR_BGR2GRAY)
	ret ,thres = cv2.threshold(mini_dil_gray, 5, 255, cv2.THRESH_BINARY_INV)	
	contours, hier = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	bounding_coordinates = []
	if not contours:
		return bounding_coordinates
		
	else:
		# Note: Convert to integer to avoid "integer serializable JSON Error"
		bounding_coordinates = [[int((fr_w * 0.08) + contour[0][0]), int((fr_h * 0.05) + contour[0][1])] for contour in contours[0]]
		return bounding_coordinates