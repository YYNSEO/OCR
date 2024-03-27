import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while True:
    rt, frame = cap.read()
    if rt:
        res1 = np.fliplr(frame)
        if res1.shape[:][1]%2!=0:
            res1=res1[:,:-1]
        height,width=res1.shape[:2]
        width2 = width//2
        res2 = res1[:,:width2]
        res1[:,width2:] = np.fliplr(res2)
        cv2.imshow('ress',res1)
        cv2.waitKey(1)