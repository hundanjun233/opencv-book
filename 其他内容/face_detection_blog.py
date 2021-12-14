# -*- coding: utf-8 -*-

import cv2
import sys

# 获得相应参数
imagePath = sys.argv[1]  # 从命令行读取图片路径
cascPath = "haarcascade_frontalface_default.xml"  # 预训练的权重文件，这里使用相对路径


# 创建haar级联分类器
faceCascade = cv2.CascadeClassifier(cascPath)

# 读取图片并将BGR图像变换为灰度图
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 检测人脸图像
# scaleFactor：确定每个图像缩放比例大小。
# minNeighbors：确定每个候选矩形应保留多少个相邻框。
# minSize：最小目标的大小。小于该值的目标将被忽略。
# maxSize：最大目标的大小。大于该值的目标将被忽略。
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30,30),
        # 如果使用OpenCV3，则需要注释下面这句
    # flags=cv2.CV_HAAR_SCALE_IMAGE
)

# x,y,w,h分别是人脸框区域的左上角点的坐标和人脸框的宽高
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("Found {0} faces!".format(len(faces)),image)
cv2.waitKey(0)

