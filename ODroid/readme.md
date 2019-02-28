# Odroid Setup

> Odroid User login information: **User:** “**odroid**”, **Password:** “**followtheants**”.

### Goals
1. Update Odroid and perform necessary setup steps
2. Test OpenCV Image Pipeline, possibly saving to disk: [OpenCV on RPi](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/)
3. Communicate with Camera - test [CSRT Tracker](https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/ "CSRT Tracker")

## Update Odroid with latest software

I’m following the setup guide here: [https://magazine.odroid.com/article/getting-started-with-ubuntu-18-04-on-the-odroid-xu4-a-beginners-guide/?ineedthispage=yes](https://magazine.odroid.com/article/getting-started-with-ubuntu-18-04-on-the-odroid-xu4-a-beginners-guide/?ineedthispage=yes)
* `apt-get update`
* `apt ugrade` \<- this took a long time!
Currently installing VNC: [https://forum.odroid.com/viewtopic.php?f=52&t=15320](https://wiki.odroid.com/odroid-xu4/application_note/software/headless_setup)

### VNC Connection to Odroid (Screen Sharing)
1. Download [https://www.realvnc.com/en/connect/download/viewer/](https://www.realvnc.com/en/connect/download/viewer/) and install to your laptop
2. Ssh into the Odroid and enter the following command:
    ```bash
    odroid@odroid:~$ vncserver :1 -geometry 1200x675 -depth 24
    ```
3. Open the “VNC Viewer” application you just installed on your laptop.
4. Type: `10.0.1.9:5901` into the top bar and press enter on your keyboard. (Where `10.0.1.9` is the IP address of the Odroid on the network.
5. The **Password is “followth”** (I tried to make it the same password as the Odroid login, but it can only be 8 characters long…)

### SSH Into Odroid:
```bash
[your laptop]$ ssh odroid@10.0.1.9
```
The password is “followtheants”

---- 
## Camera Test
First, we’d like to install OpenCV and Imutils and implement the image pipeline which fetching frames from the camera: [OpenCV on RPi](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/)
* I’ve created a virtualenv environment at `/home/odroid/Desktop/OpenCV-Camera-Test/env`.  Note that this is inside of our cloned Github Repository: [https://github.com/gcc-ant-robot/OpenCV-Camera-Test](https://github.com/gcc-ant-robot/OpenCV-Camera-Test).
Here are the commands I”ve used to install dependencies:
1. First try the trivial install: 
    ```bash
    (env) odroid@odroid:~/Desktop/OpenCV-Camera-Test$ pip install -r requirements.txt
    ```
2. Following [These Directions](http://milq.github.io/install-opencv-ubuntu-debian/), I’m installing `python3-opencv` and `libopencv-dev`:
    ```bash
    sudo apt-get install libopencv-dev python3-opencv
    ```
3. I tried `$ pip install numpy`, which failed but directed me to install:
    ```bash
    sudo apt-get install python-dev
    sudo apt-get install python3-dev

    pip install numpy
    ```

> We need to pick up here… Try this; [https://a-loner.github.io/odroid/xu4/qt/libfreenect2/opencv/2017/02/23/how-to-set-up-odroid-xu4-with-qt-opencv-and-ros.html](https://a-loner.github.io/odroid/xu4/qt/libfreenect2/opencv/2017/02/23/how-to-set-up-odroid-xu4-with-qt-opencv-and-ros.html)
