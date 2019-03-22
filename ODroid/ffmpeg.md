do `$v4l2-ctl --all` to show available cam device.

Note that for me, I get a device busy error about half of the time - which seems fishy to me.  When the commadn does work, I get this:

```
odroid@odroid:~/Desktop$ v4l2-ctl --all
Driver Info (not using libv4l2):
        Driver name   : uvcvideo
        Card type     : oCam-5CRO-U
        Bus info      : usb-xhci-hcd.3.auto-1.2
        Driver version: 4.14.102
        Capabilities  : 0x84200001
                Video Capture
                Streaming
                Extended Pix Format
                Device Capabilities
        Device Caps   : 0x04200001
                Video Capture
                Streaming
                Extended Pix Format
Priority: 2
Video input : 0 (Camera 1: ok)
Format Video Capture:
        Width/Height      : 640/480
        Pixel Format      : 'YUYV'
        Field             : None
        Bytes per Line    : 1280
        Size Image        : 614400
        Colorspace        : Default
        Transfer Function : Default (maps to Rec. 709)
        YCbCr/HSV Encoding: Default (maps to ITU-R 601)
        Quantization      : Default (maps to Limited Range)
        Flags             : 
Crop Capability Video Capture:
        Bounds      : Left 0, Top 0, Width 640, Height 480
        Default     : Left 0, Top 0, Width 640, Height 480
        Pixel Aspect: 1/1
Selection: crop_default, Left 0, Top 0, Width 640, Height 480
Selection: crop_bounds, Left 0, Top 0, Width 640, Height 480
Streaming Parameters Video Capture:
        Capabilities     : timeperframe
        Frames per second: 30.000 (30/1)
        Read buffers     : 0
                     brightness 0x00980900 (int)    : min=-4 max=4 step=1 default=0 value=0
                       contrast 0x00980901 (int)    : min=0 max=8 step=1 default=4 value=4
                     saturation 0x00980902 (int)    : min=0 max=8 step=1 default=4 value=4
                            hue 0x00980903 (int)    : min=0 max=11 step=1 default=6 value=6
              exposure_absolute 0x009a0902 (int)    : min=0 max=10 step=1 default=4 value=0

```


Using the guide here: [https://trac.ffmpeg.org/wiki/Capture/Webcam](https://trac.ffmpeg.org/wiki/Capture/Webcam).

I've done more digging; the low level support for cameras on the odroid comes from Video For Linux, or `v4l` (in this case `v4l2`) for version 2 of Video for Linux.  

Here, I list available devices, notice that `video0` is seen and recodnized as the odroid camera: 

```
(cv) odroid@odroid:~/Desktop/OpenCV-Camera-Test/blog_code$ v4l2-ctl --list-devices
s5p-mfc-dec (platform:11000000.codec):
        /dev/video10
        /dev/video11

s5p-jpeg encoder (platform:11f50000.jpeg):
        /dev/video30
        /dev/video31

s5p-jpeg encoder (platform:11f60000.jpeg):
        /dev/video32
        /dev/video33

exynos-gsc gscaler (platform:13e00000.video-scaler):
        /dev/video20

exynos-gsc gscaler (platform:13e10000.video-scaler):
        /dev/video21

oCam-5CRO-U (usb-xhci-hcd.3.auto-1.1):
        /dev/video0

```

However, Sometimes the `video0` device is not seen: 
```
(cv) odroid@odroid:~/Desktop/OpenCV-Camera-Test/blog_code$ v4l2-ctl --list-devices
s5p-mfc-dec (platform:11000000.codec):
        /dev/video10
        /dev/video11

s5p-jpeg encoder (platform:11f50000.jpeg):
        /dev/video30
        /dev/video31

s5p-jpeg encoder (platform:11f60000.jpeg):
        /dev/video32
        /dev/video33

exynos-gsc gscaler (platform:13e00000.video-scaler):
        /dev/video20

exynos-gsc gscaler (platform:13e10000.video-scaler):
        /dev/video21

Failed to open /dev/video0: No such file or directory
```

## Success FFPLAY
We were able to get a fairly high resolution and (good frame-rate) live playback from our Odroid Camera with the following:

```bash
(cv) odroid@odroid:~/Desktop$ ffplay -input_format mjpeg -f v4l2 -video_size 1280x720 -i /dev/video0
```
**Successful FFMPEG Recording to disk: ** `odroid@odroid:~/Desktop$ ffmpeg -input_format mjpeg -f v4l2 -video_size 1280x720 -i /dev/video0 mpeg.mpeg`

The video is slightly blocky, and I am investigating the mode in which the camera is currently operating (I believe it is in YUV420) currently.  Here are the supported modes:

```bash
odroid@odroid:~/Desktop$ ffmpeg -f v4l2 -list_formats all -i /dev/video0
ffmpeg version 3.4.2-2ubuntu4 Copyright (c) 2000-2018 the FFmpeg developers
  built with gcc 7 (Ubuntu/Linaro 7.3.0-16ubuntu3)
  configuration: --prefix=/usr --extra-version=2ubuntu4 --toolchain=hardened --libdir=/usr/lib/arm-linux-gnueabihf --incdir=/usr/include/arm-linux-gnueabihf --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-librsvg --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx --enable-openal --enable-opengl --enable-sdl2 --enable-v4l2_m2m --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
  libavutil      55. 78.100 / 55. 78.100
  libavcodec     57.107.100 / 57.107.100
  libavformat    57. 83.100 / 57. 83.100
  libavdevice    57. 10.100 / 57. 10.100
  libavfilter     6.107.100 /  6.107.100
  libavresample   3.  7.  0 /  3.  7.  0
  libswscale      4.  8.100 /  4.  8.100
  libswresample   2.  9.100 /  2.  9.100
  libpostproc    54.  7.100 / 54.  7.100
[video4linux2,v4l2 @ 0x4927b0] Raw       :     yuyv422 :           YUYV 4:2:2 : 2592x1944 1920x1080 1280x960 1280x720 640x480 320x240
[video4linux2,v4l2 @ 0x4927b0] Compressed:       mjpeg :          Motion-JPEG : 1920x1080 1280x720 640x480

```
