import cv2
import time
import numpy as np


webcam = cv2.VideoCapture(0)

webcam.set(3, 640)  # 3 je width
webcam.set(4, 480)  # 4 je height
# webcam.set(10,500) #10 je brightnes

# classifier = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")
classifier = cv2.CascadeClassifier("Cascades/cascade.xml")


def empty(value):
    pass



img = cv2.imread("images/5.jpg")
faces = classifier.detectMultiScale(img, 1.01, 4)
biggestSizeQr = 0
biggestQr = [0 ,0 ,0 ,0]


for (x, y, w, h) in faces:
    if w * h > biggestSizeQr:
        biggestSizeQr = w * h
        biggestQr = [x, y, w, h]

#cv2.rectangle(img, (biggestQr[0], biggestQr[1]), (biggestQr[0] + biggestQr[2], biggestQr[1] + biggestQr[3]),(0, 255, 0), 4)

"""
pts1 = np.float32([[x,y],[x,y+h],[x+w,y],[x+w,y+h]])
pts2 = np.float32([[0,0],[0,h],[w,0],[w,h]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)

imgWarp = cv2.warpPerspective(img,matrix,(w,h))
"""
if biggestSizeQr > 0:
    # print(biggestQr)
    imgCropped = img[biggestQr[1]:biggestQr[1] + biggestQr[3], biggestQr[0]:biggestQr[0] + biggestQr[2]]
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img, (13, 13), 0)
    imgCanny = cv2.Canny(imgBlur, 100, 10)

    # thresh, imgBlackWhite = cv2.threshold(imgGray,rozpeti_1, rozpeti_2, cv2.THRESH_BINARY)
    thresh, imgBlackWhite = cv2.threshold(imgGray, 90, 255, cv2.THRESH_BINARY)
    contours, hiearchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:
            # print(area)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
            if len(approx) == 4:
                print(peri)
                print(len(approx))
                """
                pts1 = np.float32([approx[0], approx[1], approx[2], approx[3]])

                pts2 = np.float32([[0, 0], [0, 600], [600, 0], [600, 600]])

                matrix = cv2.getPerspectiveTransform(pts1, pts2)

                imgWarp = cv2.warpPerspective(img, matrix, (w, h))
                """
                cv2.drawContours(imgGray, cnt, -1, (255, 0, 0), 6)

    print("\n\n")



    def warp(points1, points2, img):
        convertedPoints = np.float32(points2)
        originalPoints = np.float32(points1)

        perspectiveTransform = cv2.getPerspectiveTransform(originalPoints, convertedPoints)

        imgOutput = cv2.warpPerspective(img, perspectiveTransform, (500,500))

        #cv2.imshow("warp", imgOutput)
        return imgOutput
    def toBlackWhite(img):
        thresh, imgBlackWhite = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        return imgBlackWhite
    def blur(img):
        imgBlur = cv2.GaussianBlur(img, (7, 7), 0)
        return imgBlur
    def toGrayImg(img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return imgGray



    def editImg(img):
        warpedImg = warp([[285, 98], [478, 289], [14, 242], [220, 447]], [[0, 0], [500, 0], [0, 500], [500, 500]], img)
        grayImg = toGrayImg(warpedImg)
        blurImg = blur(grayImg)
        BWImg = toBlackWhite(blurImg)

        resized = cv2.resize(BWImg, (100,100), interpolation=cv2.INTER_LINEAR)

        return resized

    cv2.imshow("output", imgGray)
    cv2.namedWindow("edited Img", cv2.WINDOW_NORMAL)
    editedImg = editImg(img)
    cv2.imshow("edited Img", editedImg)
    print(editedImg)

    """
    resizedWarpedImg = toBlackWhite(warpedImg)
    cv2.namedWindow("bw", cv2.WINDOW_NORMAL)
    cv2.imshow("bw", resizedWarpedImg)
    """
    #cv2.imshow("cnn", imgCanny)
    #cv2.imshow("Video", img)

cv2.waitKey(0)









