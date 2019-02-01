The Following results were obtained with the Raspberry Pi's camera board using the code at this commit: https://github.com/theostangebye/cam_test/commit/4978aed8bb18b63bf9f2d54ec265020affe8d3d4.
No online processing or saving of frames was performed.

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
