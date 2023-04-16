import cv2
import pickle
import cvzone
import numpy as np

#////////
# from cvzone.SelfiSegmentationModule import SelfiSegmentation
# selfieSegmentation = SelfiSegmentation()
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
# while True:
#     success, img = cap.read()
#     imgOut = selfieSegmentation.removeBG(img, (0, 0, 255), threshold=0.8)
#     cv2.imshow("Image", imgOut)
#     cv2.waitKey(1)
# 60 cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,  thickness=2, offset=0, colorR=color)

# //////
# select Video

# cap = cv2.VideoCapture('carPark.mp4')
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('demo3.mp4')
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4600)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 4020)

# cap = cv2.VideoCapture('demo2.mp4')


with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# width, height = 107, 48
# width, height = 65, 90
# width, height = 95,150
width, height = 80, 90




def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 900:
            color = (0, 255, 10)
            thickness = 4
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Available space : {spaceCounter}/{len(posList)}', (40, 40),scale=2,
                           thickness=5, offset=20, colorR=(0,200,0))

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)