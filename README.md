## Overview

---

Find the best detector for your object detection project.  
Select multiple object detectors and compare their performance in real time.
Adjust parameters to find the setup best suited to your task.   
Allows video files and camera input.


## Installation

---
git clone https://github.com/ihprojects/HAAR-Cascades.git

pip install -r requirements.txt


###note: 
To avoid xcb version conflict using cv2, you can use opencv-python-headless instead of opencv-python


see here:
https://forum.qt.io/topic/119109/using-pyqt5-with-opencv-python-cv2-causes-error-could-not-load-qt-platform-plugin-xcb-even-though-it-was-found/15

---

     

## Usage

----

1. Choose whether to use video from file or camera in menubar
2. Add object detector from dropdown menu
3. Select which object you want to find in video
4. Add detector
5. Adjust parameters and see their effect on object detection in real time
6. Creating your own scenario widget allows visualization of your data and export to external files  
   (use the Scenario class as base for you own widgets)
7. Add your own detectors by inheriting from Detector class(a name and an init argument must be added to the   
AVAILABLE_DETECTORS dictionary in DetectorManager class)
