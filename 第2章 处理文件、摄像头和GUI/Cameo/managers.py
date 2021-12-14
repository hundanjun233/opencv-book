import cv2
import numpy
import time


class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None,
                 shouldMirrorPrevies = False):
        self.previewWindowManager = previewWindowManager   # 一个自己的写的WindowManager，
                                                           # 本身是对cv2.namedWindow的一种高级封装。
        self.shouldMirrorPreview = shouldMirrorPrevies     # 在预览窗口中是否镜像显示。
        self._capture = capture                            # 一般会传入cv2.videoCapture
        self._channel = 0                                  # 多个摄像头时使用
        self._enteredFrame = False                         # 用于控制当前帧
        self._frame = None                                 # 记录当前帧
        self._imageFileName = None                         # 截屏功能的文件名
        self._videoFileName = None                         # 录屏功能的文件名
        self._videoEncoding = None                         # 录屏功能的存储编码
        self._videoWriter = None                           # 传入cv2.videoWriter
        self._startTime = None                             # 用于估计帧数
        self._framesElapsed = 0                            # 记录流过的帧数
        self._fpsEstimate = None                           # 记录估计的帧率

    @property
    def channel(self):                                     # 通过CaptureManager.channel读取CaptureManager._channel
        return self._channel

    @channel.setter
    def channel(self, value):                              # 通过CaptureManager.channel = <xxx>改变CaptureManager._channel
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):                                       # 通过CaptureManager.frame读取CaptureManager._frame（只读）
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
                self._frame, self.channel
            )
        return self._frame

    @property
    def isWritingImage(self):                              # 添加了一个属性，和文件名绑定
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):                              # 同上
        return self._videoFileName is not None

    def enterFrame(self):                                  # 后边注释直接看notion文档
        """Capture the next frame, if any"""
        # But first, check that any previous frame was exited,
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """Draw to the window. Write to files. Release the frame."""

        # Check whether any grabbed frame is retrievable
        # The getter may retrieve and cache the frame.
        if self.frame is None:
            self._enteredFrame = False
            return

        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Draw to the window, if any.
        if self.shouldMirrorPreview:
            mirroredFrame = numpy.fliplr(self._frame)
            self.previewWindowManager.show(mirroredFrame)
        else:
            self.previewWindowManager.show(self._frame)

        # Write to the image file, if any.
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        # Write to the video file, if any.
        self._writeVideoFrame()

        # Release the frame.
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        """Write the next exited frame to an image file."""
        self._imageFileName = filename

    def startWritingVideo(
            self, filename,
            encoding = cv2.VideoWriter_fourcc('M','J','P','G')):
        """Start writing exited frames to a video file."""
        self._videoFileName = filename
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        """Stop writing exited frames to a video file."""
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                # The capture's FPS is unkown so use estimate.
                if self._framesElapsed < 20:
                    # Wait until more frames elaspse so that the
                    # estimate is more stable.
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(
                        cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                        cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(
                self._videoFileName, self._videoEncoding,
                fps, size)
        self._videoWriter.write(self._frame)


class WindowManager(object):
    def __init__(self, windowName, keypressCallback= None):
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    # 管理窗口事件及其生命周期
    @property
    def isWindowCreated(self):
        return self._isWindowCreated
    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True
    def show(self, frame):
        cv2.imshow(self._windowName, frame)
    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            self.keypressCallback(keycode)