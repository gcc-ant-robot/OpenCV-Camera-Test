# Raspberry Pi Image Pipeline
Jan 30th, 2019

**EXPERIMENT GUIDE:** [https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/). This guide shows how to use threading to reduce I/O latency between us and the camera.

## Notes:
* I am using python 2.7 and am using a virtual env called venv.
* [https://github.com/theostangebye/cam\_test](https://github.com/theostangebye/cam_test)
* When installing `picamera` on the Pi, **use** `$ pip install "picamera[array]"`.  The `[array]` portion enables us to [grab frames from the camera as NumPy arrays](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)!

##### Importance of Using NumPy Arrays
* The following explains why we want to access camera data as NumPy arrays.  Essentially, **NumPy arrays avoid expensive JPEG compression**.
	> Here is an example of polling the camera for a single frame: [Source](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/). The article continues to show how to access video frames at ~30fps.  However, we are going to continue with the “Experiment Guide” listed above in order to attain higher framerates through threading.
	> ```python
	> # import the necessary packages
	> from picamera.array import PiRGBArray
	> from picamera import PiCamera
	> import time
	> import cv2
	>  
	> # initialize the camera and grab a reference to the raw camera capture
	> camera = PiCamera()
	> rawCapture = PiRGBArray(camera)
	>  
	> # allow the camera to warmup
	> time.sleep(0.1)
	>  
	> # grab an image from the camera
	> camera.capture(rawCapture, format="bgr")
	> image = rawCapture.array
	>  
	> # display the image on screen and wait for a keypress
	> cv2.imshow("Image", image)
	> cv2.waitKey(0)
	> ```
	> “From there, we initialize our PiCamera object on Line 8 and grab a reference to the raw capture component on Line 9. This rawCapture  object is especially useful since it (1) gives us direct access to the camera stream and (2) avoids the expensive compression to JPEG format, which we would then have to take and decode to OpenCV format anyway. I highly recommend that you use PiRGBArray  whenever you need to access the Raspberry Pi camera — the performance gains are well worth it.”

* 
