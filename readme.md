# Raspberry Pi Image Pipeline
Jan 30th, 2019

## TODO:
1. [ ] Test FPS while saving images to disk.
2. [ ] Implement LaserDot RasterScan for benchmark.
3. [ ] Create I2C or serial comm link between RPi and myRIO.

## Important Links
* **Blog Post on Threaded Camera Polling:** [https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/). This guide shows how to use threading to reduce I/O latency between us and the camera.
* [Camera Module](https://www.amazon.com/gp/product/B012V1HEP4/ref=ppx_yo_dt_b_asin_title_o00__o00_s01?ie=UTF8&psc=1): Notice that this is not an official RPi component. 

## Notes:
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
