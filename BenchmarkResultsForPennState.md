# Benchmark Results:

> **USING THIS COMMIT:** [https://github.com/gcc-ant-robot/OpenCV-Camera-Test/commit/62edf8fadf2c447f4b94a16c5775a5e5e1a818e5](https://github.com/gcc-ant-robot/OpenCV-Camera-Test/commit/62edf8fadf2c447f4b94a16c5775a5e5e1a818e5)

```python
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
```


### Odroid: 
* Record images (jpeg 1280x720):
		 
```bash
(cv) odroid@odroid:~/Desktop/OpenCV-Camera-Test$ for i in {1..5}; do rm images/*; python cam_benchmark.py -n 500 -s 1; done
rm: cannot remove 'images/*': No such file or directory
[INFO] sampling THREADED frames from webcam...
VIDEOIO ERROR: V4L: can't open camera by index 0
Traceback (most recent call last):
  File "cam_benchmark.py", line 41, in <module>
	frame = imutils.resize(frame, width=1280)
  File "/home/odroid/.virtualenvs/cv/lib/python3.6/site-packages/imutils/convenience.py", line 69, in resize
	(h, w) = image.shape[:2]
AttributeError: 'NoneType' object has no attribute 'shape'
rm: cannot remove 'images/*': No such file or directory
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 32.44
[INFO] approx. FPS: 15.41
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 35.28
[INFO] approx. FPS: 14.17
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 34.27
[INFO] approx. FPS: 14.59
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 33.67
[INFO] approx. FPS: 14.85
```
* Find Brightest Dot: 

```bash
(cv) odroid@odroid:~/Desktop/OpenCV-Camera-Test$ for i in {1..5}; do python cam_benchmark.py -n 500 -b 1; done
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 13.00
[INFO] approx. FPS: 38.45
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 12.38
[INFO] approx. FPS: 40.38
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 12.66
[INFO] approx. FPS: 39.49
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 13.20
[INFO] approx. FPS: 37.88
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 12.82
[INFO] approx. FPS: 38.99
```
### RPI:
* Record images (jpeg 1280x720):

> Below suggests ~12 FPS.  However, I think that we get closer to 15 FPS depending on the complexity of the image and the temperature of the RPi. (thermals)

```bash
(env_python3) pi@pi3:~/Desktop/cam_test $ for i in {1..5}; do rm images/*; python cam_benchmark.py -n 500 -s 1; done
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 40.19
[INFO] approx. FPS: 12.44
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 38.83
[INFO] approx. FPS: 12.88
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 39.76
[INFO] approx. FPS: 12.57
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 41.10
[INFO] approx. FPS: 12.17
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 38.64
[INFO] approx. FPS: 12.94
(env_python3) pi@pi3:~/Desktop/cam_test $
```
* Find Brightest Dot: 

```bash
(env_python3) pi@pi3:~/Desktop/cam_test $ for i in {1..5}; do python cam_benchmark.py -n 500 -b 1; done
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 8.95
[INFO] approx. FPS: 55.89
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 9.02
[INFO] approx. FPS: 55.41
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 8.95
[INFO] approx. FPS: 55.88
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 9.04
[INFO] approx. FPS: 55.32
[INFO] sampling THREADED frames from webcam...
[INFO] elasped time: 8.94
[INFO] approx. FPS: 55.94
(env_python3) pi@pi3:~/Desktop/cam_test $
```
### Ant Robot
* Record images (jpeg 640x480): 4 FPS
* Find Brightest Dot: 10 FPS
