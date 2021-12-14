import cv2
import numpy as np
from images import image_path
import os
print(os.path.join(image_path,'my-image.JPG'))
img = cv2.imread(os.path.join(image_path,'my-image.JPG'))

cv2.imshow('my image', img)
cv2.waitKey()
cv2.destroyAllWindows()