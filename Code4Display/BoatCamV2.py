import sys
import os

import numpy as np
import cv2
from PyQt5 import sip
import pyrealsense2.pyrealsense2 as rs

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QAction, QApplication, QGridLayout,
                             QGroupBox, QLCDNumber, QLabel, 
                             QLabel, QMainWindow, QMenu, 
                             QMenuBar, QPushButton, QVBoxLayout,  QWidget,
                             QToolBar)
from PyQt5.QtCore import QTimer, QTime, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFont, QPixmap, QImage
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self._createActions()
        
        #Setup of Main Window
        self.setWindowTitle("Home")
        self.setFixedSize(800, 480)
        self.move(0,0)

        self.haveCameraToolBar = False
        self.continueTimer = False

        self.colorTH = CameraThread(self)
        self.depthTH = CameraThread(self)

        self.shouldBeColor = False
        self.shouldBeDepth = False

        #Creating a MenuBar
        self._createMenuBar()

        self._createHomeWindow()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setFont(QFont('Maax', 20))

        self.homeMenu = QMenu('&Home', self)
        self.homeMenu.setFont(QFont('Maax', 40))
        menuBar.addMenu(self.homeMenu)
        self.homeMenu.addAction(self.homeAction)

        self.cameraMenu = QMenu('&Camera', self)
        self.cameraMenu.setFont(QFont('Maax', 40))
        menuBar.addMenu(self.cameraMenu)
        self.cameraMenu.addAction(self.cameraAction)
        self.cameraMenu.addAction(self.depthCameraAction)

        self.clockMenu = QMenu('&Clock', self)
        self.clockMenu.setFont(QFont('Maax', 40))
        menuBar.addMenu(self.clockMenu)
        self.clockMenu.addAction(self.clockAction)
        self.timer = QTimer(self)

        self.setMenuBar(menuBar)

    def _createActions(self):
        self.homeAction = QAction('&Home', self)
        self.homeAction.triggered.connect(lambda: self._createHomeWindow())
        self.cameraAction = QAction('&Color', self)
        self.cameraAction.triggered.connect(lambda: self._createCameraWindow())
        self.depthCameraAction = QAction('&Depth')
        self.depthCameraAction.triggered.connect(lambda: self._createDepthCameraWindow())
        self.clockAction = QAction('&Clock')
        self.clockAction.triggered.connect(lambda: self._createClockWindow())
        self.updateAction = QAction('&Update')
        self.updateAction.triggered.connect(lambda: self._updateSoftware())

    def _createHomeWindow(self):
        self.setWindowTitle("Home Window")

        #Create a centrel Label
        self._createHomeButtonLayout()
        self.setCentralWidget(self.horizontalGroupBox)

        self.ExitStuff()

    def _createCameraWindow(self):
        self.setWindowTitle("Color Camera Window")

        #Create a centrel Label
        self.Colorlabel_show = QLabel("Color Window")
        self.Colorlabel_show.setGeometry(QRect(10, 0, 640, 480))
        self.setCentralWidget(self.Colorlabel_show)

        self.ExitStuff()

        self.open_colorCamera()

        self.createCameraButtons()


    def _createDepthCameraWindow(self):
        self.setWindowTitle("Depth Camera Window")

        #Create a centrel Label
        self.Depthlabel_show = QLabel("Depth Window")
        self.Depthlabel_show.setGeometry(QRect(10, 0, 640, 480))
        self.setCentralWidget(self.Depthlabel_show)
        
        self.ExitStuff()

        self.open_depthCamera()

        self.createCameraButtons()
      

    def _createClockWindow(self):
        self.setWindowTitle('Clock Window')

        font = QFont('Maax', 75, QFont.Bold)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)

        self.setCentralWidget(self.label)
       
        self.timer.timeout.connect(self.Time)

        self.timer.start(1000)

        self.continueTimer = True

        self.ExitStuff()
        

    def Time(self):
        current_time = QTime.currentTime()

        #Format         Result
        #dd.MM.yyyy	    21.05.2001
        #ddd MMMM d yy	Tue May 21 01
        #hh:mm:ss.zzz	14:13:09.120
        #hh:mm:ss.z	    14:13:09.12
        #h:m:s ap	    2:13:9 pm
        label_time = current_time.toString('h:m:s ap')

        if not sip.isdeleted(self.label):
            self.label.setText(label_time)

    def _createHomeButtonLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        
        cameraButton = QPushButton('Camera')
        depthButton = QPushButton('Depth')
        ThirdButton = QPushButton('3')
        clockButton = QPushButton('Clock')
        settingsButton = QPushButton('Settings')
        updateButton = QPushButton('Update')

        cameraButton.setFont(QFont('Maax', 30))
        depthButton.setFont(QFont('Maax', 30))
        ThirdButton.setFont(QFont('Maax', 30))
        clockButton.setFont(QFont('Maax', 30))
        settingsButton.setFont(QFont('Maax', 30))
        updateButton.setFont(QFont('Maax', 30))

        cameraButton.clicked.connect(self._createCameraWindow)
        depthButton.clicked.connect(self._createDepthCameraWindow)
        #ThirdButton.addAction()
        clockButton.clicked.connect(self._createClockWindow)
        #settingsButton.addAction()
        updateButton.clicked.connect(self._updateSoftwareWindow)

        layout.addWidget(cameraButton, 0, 0)
        layout.addWidget(depthButton, 0, 2)
        layout.addWidget(ThirdButton, 1, 0)
        layout.addWidget(clockButton, 1, 2)
        layout.addWidget(settingsButton, 2, 0)
        layout.addWidget(updateButton, 2, 2)
        
        self.horizontalGroupBox.setLayout(layout)
        self.setCentralWidget(self.horizontalGroupBox)

    def _updateSoftwareWindow(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        questionLabel = QLabel('Are you sure????????')
        yesButton = QPushButton('Yes')
        noButton = QPushButton('No')

        questionLabel.setFont(QFont('Maax', 30))
        yesButton.setFont(QFont('Maax', 30))
        noButton.setFont(QFont('Maax', 30))

        yesButton.clicked.connect(self._updateSoftware)
        noButton.clicked.connect(self._createHomeWindow)
        
        questionLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(questionLabel, 0, 0)
        layout.addWidget(yesButton, 1, 0)
        layout.addWidget(noButton, 2, 0)

        self.horizontalGroupBox.setLayout(layout)
        self.setCentralWidget(self.horizontalGroupBox)

    def _updateSoftware(self):
        os.system("xterm -hold -e ./update.sh")

    def open_colorCamera(self):
        if(self.depthTH.isRunning()):
            self.depthTH.changePixmap.disconnect()
            self.depthTH.stop()

        self.shouldBeColor = True
        self.shouldBeDepth = False
        self.colorCamera_label = QLabel(self)
        self.depthCamera_label = QLabel(self)
        self.setCentralWidget(self.colorCamera_label)
        self.colorTH = CameraThread(self)
        self.colorTH.setCamera(0)
        self.colorTH.changePixmap.connect(self.setImage)
        self.colorTH.start()
        self.show()

    def open_depthCamera(self):
        if(self.colorTH.isRunning()):
            self.colorTH.changePixmap.disconnect()
            self.colorTH.stop()

        self.shouldBeColor = False
        self.shouldBeDepth = True
        self.colorCamera_label = QLabel(self)
        self.depthCamera_label = QLabel(self)
        self.setCentralWidget(self.depthCamera_label)
        self.depthTH = CameraThread(self)
        self.depthTH.setCamera(1)
        self.depthTH.changePixmap.connect(self.setImage)
        self.depthTH.start()
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        if not sip.isdeleted(self.colorCamera_label):
            if(self.shouldBeColor):
                self.colorCamera_label.setPixmap(QPixmap.fromImage(image))

        if not sip.isdeleted(self.depthCamera_label):
            if(self.shouldBeDepth):
                self.depthCamera_label.setPixmap(QPixmap.fromImage(image))

    def createCameraButtons(self):
        self.haveCameraToolBar = True

        self.cameraToolBar = QToolBar("Camera Tool Bar")
  
        self.addToolBar(self.cameraToolBar)
  
        photo_action = QAction("Take Photo", self)
        photo_action.setStatusTip("This will capture picture")
        photo_action.setToolTip("Capture picture")
        if(self.shouldBeColor):
            photo_action.triggered.connect(self._takeColorPhoto)
        else:
            photo_action.triggered.connect(self._takeDepthPhoto)

        self.video_action = QAction("Record", self)
        self.video_action.setStatusTip("This will record video")
        self.video_action.setToolTip("Record")
        if(self.shouldBeColor):
            self.video_action.triggered.connect(self._takeColorVideo)
        else:
            self.video_action.triggered.connect(self._takeDepthVideo)

        self.cameraToolBar.addAction(photo_action)
        self.cameraToolBar.addAction(self.video_action)
        
    def _takeColorPhoto(self):
        self.colorTH.TakePhoto()

    def _takeDepthPhoto(self):
        self.depthTH.TakePhoto()

    def _takeColorVideo(self):
        self.cameraToolBar.setStyleSheet("border: 3px solid red;")
        self.video_action.triggered.connect(self._stopColorVideo)
        self.colorTH.TakeVideo()

    def _stopColorVideo(self):
        self.cameraToolBar.setStyleSheet("border: solid white;")
        self.video_action.triggered.connect(self._takeColorVideo)
        self.colorTH.StopVideo()
    
    def _takeDepthVideo(self):
        self.cameraToolBar.setStyleSheet("border: 3px solid red;")
        self.video_action.triggered.connect(self._stopDepthVideo)
        self.depthTH.TakeVideo()

    def _stopDepthVideo(self):
        self.cameraToolBar.setStyleSheet("border: solid white;")
        self.video_action.triggered.connect(self._takeDepthVideo)
        self.depthTH.StopVideo()

    def ExitStuff(self):
        if(not self.continueTimer):
            self.timer.stop()
            self.continueTimer = False

        if(self.haveCameraToolBar):
            self.removeToolBar(self.cameraToolBar)
            self.haveToolBar = False

        if(self.colorTH.isRunning()):
            self.colorTH.changePixmap.disconnect()
            self.colorTH.stop()

        if(self.depthTH.isRunning()):
            self.depthTH.changePixmap.disconnect()
            self.depthTH.stop()

class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.save_path = r"C:\Users\cie3\Desktop"
        #self.save_path = r"~/Desktop"

        self.running = True

        self.color_image = None
        self.depth_colormap = None
        
        self.cameraValue = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.recordThis = False
        self.recorderSETUP = False

    def run(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        if(self.cameraValue == 0):
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            self.isEnabled = True
            
            try:
                self.pipeline.start(self.config)
            except:
                print("No camera connected")
                sys.exit()

            try:
                while self.running:
                    frames = self.pipeline.wait_for_frames()
                    color_frame = frames.get_color_frame()

                    if not color_frame:
                        continue

                    self.color_image = np.asanyarray(color_frame.get_data())

                    color_image = cv2.cvtColor(self.color_image, cv2.COLOR_BGR2RGB)

                    h, w, ch = color_image.shape

                    if(self.recordThis):
                        if(self.recorderSETUP):
                            self.videoRecorder.write(self.color_image)
                        else:
                            self.setupVideoRecorder(h, w)

                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(color_image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(800, 480)
                    self.changePixmap.emit(p)

            except RuntimeError:
                print('')

            finally:
                self.pipeline.stop()

        elif(self.cameraValue == 1):
            self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            
            self.isEnabled = True

            try:
                self.pipeline.start(self.config)
            except:
                print("No camera connected")
                sys.exit()

            try:
                while self.running:
                    frames = self.pipeline.wait_for_frames()
                    depth_frame = frames.get_depth_frame()

                    if not depth_frame:
                        continue

                    depth_image = np.asanyarray(depth_frame.get_data())

                    self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                    depth_colormap = cv2.cvtColor(self.depth_colormap, cv2.COLOR_BGR2RGB)

                    h, w, ch = depth_colormap.shape

                    if(self.recordThis):
                        if(self.recorderSETUP):
                            self.videoRecorder.write(self.depth_colormap)
                        else:
                            self.setupVideoRecorder(h, w)

                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(depth_colormap.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(800, 480)
                    self.changePixmap.emit(p)

            except RuntimeError:
                print('')

            finally:
                self.pipeline.stop()

    def TakePhoto(self):
        if(self.cameraValue == 0):
            cv2.imwrite(os.path.join(self.save_path, 'thing.jpg'), self.color_image)
        else:
            cv2.imwrite(os.path.join(self.save_path, 'thing.jpg'), self.depth_colormap)

    def setupVideoRecorder(self, h, w):
        if(self.cameraValue == 0):
            self.videoRecorder = cv2.VideoWriter(os.path.join(self.save_path, 'thing.avi'), self.fourcc, 30, (w, h))
        else:
            self.videoRecorder = cv2.VideoWriter(os.path.join(self.save_path, 'thing.avi'), self.fourcc, 30, (w, h))

        self.recorderSETUP = True

    def TakeVideo(self):
        self.recordThis = True

    def StopVideo(self):
        self.recordThis = False
        self.videoRecorder.release()

    def setCamera(self, value):
        self.cameraValue = value

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())