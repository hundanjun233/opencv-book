# 2.2.4 读取/写入视频文件
import cv2

videoCapture = cv2.VideoCapture('testVideo.mp4')
fps = videoCapture.get(cv2.CAP_PROP_FPS)  # 参数的值是5
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),  # 参数的值是3
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 参数的值是4
videoWriter = cv2.VideoWriter(
    'MyOutput.mp4', cv2.VideoWriter_fourcc('X', '2', '6', '4'),
    fps, size
)

success, frame = videoCapture.read()
while success:  # 循环直到没有更多的帧
    videoWriter.write(frame)
    success, frame = videoCapture.read()