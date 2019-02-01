# Raspberry Pi Image Pipeline
Jan 30th, 2019

**EXPERIMENT GUIDE:** [https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/). This guide shows how to use threading to reduce I/O latency between us and the camera.

## Notes:
* I am using python 2.7 and am using a virtual env called venv.
* [https://github.com/theostangebye/cam\_test](https://github.com/theostangebye/cam_test)
* When installing `picamera` on the Pi, **use** `$ pip install "picamera[array]"`.  The `[array]` portion enables us to [grab frames from the camera as NumPy arrays](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)!

* According to the following [Forum Post](https://www.raspberrypi.org/forums/viewtopic.php?t=85899), we will likely get better performance using the Raspberry Pi's Camera Board vs. using a USB Webcam.

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

* I ended up finding the source code of the blog post: [Source](./blog_code/ "Source Code in Repo"). Note that when installing `OpenCV` for the Raspberry Pi, you **must use an ARM **version.  Instead of compiling mine own from source, I [added piwheels to my pip config](https://www.piwheels.org).  Then, I was able to install OpenCV with the following command: `$ pip install opencv-contrib-python`.  **Note that I changed to Python 3.5** as PiWheels did not have precompiled support for OpenCV with Python 2.7.
* I tried testing with `$ python picamera_fps_demo.py ` but was receiving errors related to low level dev objects “No shared object,” etc.  I found the [following](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) which helped: 
	> “On the Raspberry PI I kept receiving errors when I would import cv2 in python3.
	> It would say: ImportError: libcblas.so.3: cannot open shared object file: No such file or directory
	> I did find the fix for it here: https://github.com/amymcgovern/pyparrot/issues/34#issuecomment-379557137
	> I had to install these dependencies:
	> ```bash
	> sudo apt-get install libatlas-base-dev
	> sudo apt-get install libjasper-dev
	> sudo apt-get install libqtgui4
	> sudo apt-get install python3-pyqt5
	> ```
	> ” - [https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)


## First Results:
1. The following results were captured with the defaults code implementation, **320x240 resolution** from a remote **ssh terminal**
	```bash
	(env_python3) pi@pi3:~/Desktop/cam_test/blog_code $ python picamera_fps_demo.py
	[INFO] sampling frames from `picamera` module...
	[INFO] elasped time: 3.43
	[INFO] approx. FPS: 29.47
	[INFO] sampling THREADED frames from `picamera` module...
	[INFO] elasped time: 0.40
	[INFO] approx. FPS: 249.15
	```

2.  The Following Results were obtained while connected to the Pi over **VNC** from the Pi’s Linux GUI and terminal app.  Note that the resolution of each image is only **320x240**.  We will need to increase that.
	```bash
	(env_python3) pi@pi3:~/Desktop/cam_test/blog_code $ python picamera_fps_demo.py -d 1 -n 1000
	[INFO] sampling frames from `picamera` module...
	[INFO] elasped time: 33.50
	[INFO] approx. FPS: 29.88
	[INFO] sampling THREADED frames from `picamera` module...
	[INFO] elasped time: 9.33
	[INFO] approx. FPS: 107.20
	```

3.  When the resolution of each image is increased the frame rate drops dramatically. Here’s Full HD Results from the internal console over VNC shared desktop with the `-d 1` flag enabled so that the Pi displays images in the GUI. Notice that the number of frames considered has gone from 1000 to 100: 
	```bash
	(env_python3) pi@pi3:~/Desktop/cam_test/blog_code $ python picamera_fps_demo.py -d 1 -n 100
	[INFO] sampling frames from `picamera` module...
	/home/pi/Desktop/cam_test/env_python3/lib/python3.5/site-packages/picamera/encoders.py:544: PiCameraResolutionRounded: frame size rounded up from 1920x1080 to 1920x1088
	  width, height, fwidth, fheight)))
	[INFO] elasped time: 30.26
	[INFO] approx. FPS: 3.34
	[INFO] sampling THREADED frames from `picamera` module...
	[INFO] elasped time: 12.94
	[INFO] approx. FPS: 7.73
	```

4. However, if the program is called from a **remote ssh terminal** and the **RPI is not asked to display each frame**, the FPS increased dramatically for 100 frames at full HD resolution, enabling an expected FPS of almost 30!: 
	```bash
	(env_python3) pi@pi3:~/Desktop/cam_test/blog_code $ python picamera_fps_demo.py -n 100
	[INFO] sampling frames from `picamera` module...
	/home/pi/Desktop/cam_test/env_python3/lib/python3.5/site-packages/picamera/encoders.py:544: PiCameraResolutionRounded: frame size rounded up from 1920x1080 to 1920x1088
	  width, height, fwidth, fheight)))
	[INFO] elasped time: 22.17
	[INFO] approx. FPS: 4.56
	[INFO] sampling THREADED frames from `picamera` module...
	[INFO] elasped time: 3.36
	[INFO] approx. FPS: 29.80
	```
