# USAGE
# python fps_demo.py
# python fps_demo.py --display 1

# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import pdb
import numpy as np

import pdb


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
ap.add_argument("-s", "--save-frames", type=int, default=-1,
	help="# Whether or not to save image frames to ./images/")
ap.add_argument("-b", "--brightest-pixel", type=int, default=-1,
    help="# Whether or not to find location of brightest pixel")
args = vars(ap.parse_args())

# created a *threaded *video stream, allow the camera senor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()
i = 0      #Only for testing brightest_pixel logic
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=1280)

	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	if args["save_frames"] > 0:
		cv2.imwrite(("./images/img"+ str(fps._numFrames)+".jpg"), frame)
                        
	if args["brightest_pixel"] > 0:

		decVal = 3	#Number of interval of row to keep in decimating
		decimated_frame = frame[::decVal,:,1] # only uses every decVal'th col, and grabs red channel

		max_val = np.amax(decimated_frame)

		# Get the indices of maximum element in np array
		result = np.where(decimated_frame == max_val)

		# result is 2 arrays: 
		# 	the first holds the indices of max_val on the x axis,
		# 	the second holds the indices of max_val on the y axis
		row = result[0][0]
		col = result[1][0]

# 		print('First Maximum Value of ', max_val, ' Located at: ', row, ', ', col)
		                
    # update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
