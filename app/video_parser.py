
def extractFrameInfosFromVideo(_videoPath):

    capture = cv2.VideoCapture(_videoPath)

    while (capture.isOpened()):
            stime = time.time()
            ret, frame = capture.read()

            originalFrame = frame
