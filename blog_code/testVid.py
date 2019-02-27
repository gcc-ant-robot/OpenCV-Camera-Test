import picamera

with picamera.PiCamera() as camera:
     camera.resolution = (1280, 720)
     camera.start_recording('my_videoHD.h264')
     camera.wait_recording(60)
     camera.stop_recording()
