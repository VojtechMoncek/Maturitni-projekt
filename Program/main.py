'imporotvani:'
import cv2
import time
import numpy as np
"""
img = cv2.imread("images/rias.png")

'zobraz image'
cv2.imshow("output",img)

'cekej inf sekund'
cv2.waitKey(0)
"""

"""
webcam = cv2.VideoCapture(0)

webcam.set(3, 640) #3 je width
webcam.set(4, 480) #4 je height
webcam.set(10,500) #10 je brightnes
while True:
    sucess, img = webcam.read()
    imgSeda = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img, (7,7),0)
    cv2.imshow("Video",imgSeda)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
"""


"""
img = cv2.imread("images/rias.png")
kernel = np.ones((4,4),np.uint8)



imgSeda = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgRozmazana = cv2.GaussianBlur(imgSeda, (5,5),0)

imgCanny = cv2.Canny(img, 100,100)
imgDialation = cv2.dilate(imgCanny,kernel, iterations=1)

cv2.imshow("Rias", imgRozmazana)
cv2.imshow("Rias", imgCanny)
#cv2.imshow("Rias", imgDialation)




cv2.waitKey(0)
"""

"""
img = cv2.imread("images/rias.png")
print(img.shape)

#imgResize = cv2.resize(img,(200, 300))

imgCropped = img[0:400,200:400]
cv2.imshow("Rias", imgCropped)




cv2.waitKey(0)
"""
"""

img = cv2.imread("images/rias.png")

img = np.zeros((512,512,3),np.uint8)

#img[200:300,100:300] = 0,0,255

cv2.line(img, (0,0),(img.shape[0],img.shape[1]),(0,0,255),4)
cv2.rectangle(img, (0,0),(250,300), (0,255,0),cv2.FILLED)
cv2.circle(img,(400,50), 30, (255,255,0),cv2.FILLED)
cv2.putText(img,"RIAS",(250,250),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)

cv2.imshow("Rias", img)




cv2.waitKey(0)
"""

"""
img = cv2.imread("images/rias.png")

imgHor = np.hstack((img,img))
imgVer = np.vstack((img,img))

cv2.imshow("hor",imgHor)
cv2.waitKey(0)

"""

"""
def empty(value):
    pass


cv2.namedWindow("trackBars")
cv2.resizeWindow("trackBars",640,240)

cv2.createTrackbar("Hue min", "trackBars",0,179,empty)
cv2.createTrackbar("Hue max", "trackBars",0,179,empty)
cv2.createTrackbar("Sat min", "trackBars",219,255,empty)
cv2.createTrackbar("Sat max", "trackBars",0,255,empty)
cv2.createTrackbar("Val min", "trackBars",0,26,empty)
cv2.createTrackbar("Val max", "trackBars",0,255,empty)


while True:
    img = cv2.imread("images/rias.png")

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue min", "trackBars")
    h_max = cv2.getTrackbarPos("Hue max", "trackBars")
    s_min = cv2.getTrackbarPos("Sat min", "trackBars")
    s_max = cv2.getTrackbarPos("Sat max", "trackBars")
    v_min = cv2.getTrackbarPos("Val min", "trackBars")
    v_max = cv2.getTrackbarPos("Val max", "trackBars")

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("hsv",imgHSV)
    cv2.imshow("img", img)
    cv2.imshow("Mask", mask)

    cv2.imshow("result", imgResult)

    cv2.waitKey(1)
"""
"""
imgOriginal = cv2.imread("images/tvary.png")

imgGray = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur, 50,50)

imgBlank = np.zeros_like(imgOriginal       )

#cv2.imshow("original",imgOriginal)
cv2.imshow("imgGray",imgGray)
cv2.imshow("imgBlur",imgBlur)
cv2.imshow("imgCanny",imgCanny)

cv2.waitKey(0)
"""


webcam = cv2.VideoCapture(0)

webcam.set(3, 640) #3 je width
webcam.set(4, 480) #4 je height
#webcam.set(10,500) #10 je brightnes

#classifier = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")
classifier = cv2.CascadeClassifier("Cascades/cascade.xml")

cv2.namedWindow("trackBars")
cv2.resizeWindow("trackBars",640,240)


def empty(value):
    pass

#cv2.createTrackbar("rozpeti 1", "trackBars",0,255,empty)
#cv2.createTrackbar("rozpeti 2", "trackBars",0,255,empty)

while True:
    #rozpeti_1 = cv2.getTrackbarPos("rozpeti 1", "trackBars")
    #rozpeti_2 = cv2.getTrackbarPos("rozpeti 2", "trackBars")

    sucess, img = webcam.read()
    faces = classifier.detectMultiScale(img,1.1,4)
    biggestSizeQr = 0
    biggestQr = [0,0,0,0]
    for index,(x,y,w,h) in enumerate(faces):
        if w*h > biggestSizeQr:
            biggestSizeQr = w*h
            biggestQr = [x,y,w,h]


    cv2.rectangle(img, (biggestQr[0],biggestQr[1]), (biggestQr[0]+biggestQr[2],biggestQr[1]+biggestQr[3]), (0,255,0), 2)

    """
    pts1 = np.float32([[x,y],[x,y+h],[x+w,y],[x+w,y+h]])
    pts2 = np.float32([[0,0],[0,h],[w,0],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    """
    if biggestSizeQr > 0:
        #print(biggestQr)
        imgCropped = img[biggestQr[1]:biggestQr[1]+biggestQr[3],biggestQr[0]:biggestQr[0]+biggestQr[2]]
        imgGray = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGray,200,200)


        #thresh, imgBlackWhite = cv2.threshold(imgGray,rozpeti_1, rozpeti_2, cv2.THRESH_BINARY)
        thresh, imgBlackWhite = cv2.threshold(imgGray, 90, 255, cv2.THRESH_BINARY)



        contours, hiearchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area:
                #print(area)

                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri,True)


                if len(approx) == 4:
                    print(peri)
                    print(approx)


                    pts1 = np.float32([approx[0],approx[1],approx[2],approx[3]])

                    pts2 = np.float32([[0, 0], [0, 600], [600, 0], [600, 600]])

                    matrix = cv2.getPerspectiveTransform(pts1, pts2)

                    imgWarp = cv2.warpPerspective(imgGray, matrix, (w, h))

                    cv2.drawContours(imgGray, cnt, -1, (255, 0, 0), 3)


        print("\n\n")







        cv2.imshow("output",imgGray)



    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break
    time.sleep(2)











