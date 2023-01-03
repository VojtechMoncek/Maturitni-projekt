import cv2

qrCascade = cv2.CascadeClassifier("cascade.xml")

img = cv2.imread("images/2.jpg")
multiplier = 1
if img.shape[1] > img.shape[0]:
    multiplier = 250 / img.shape[1]
else:
    multiplier = 2\50 / img.shape[0]

width = int(img.shape[1] * multiplier)
height = int(img.shape[0] * multiplier)
img = cv2.resize(img, (width,height), interpolation = cv2.INTER_AREA)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

thresh = cv2.adaptiveThreshold (imgGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
thresh2 = cv2.adaptiveThreshold (imgGray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
ret, thresh3 = cv2.threshold (imgGray,127,255,cv2.THRESH_BINARY)

cv2.imshow("G img", imgGray)
cv2.imshow("thresh", thresh)
qr = qrCascade.detectMultiScale(imgGray,1.2,5)


for (x,y,w,h) in qr:
    print("aaa")
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0, 255,0),2)



img = cv2.resize(img, (width,height), interpolation = cv2.INTER_AREA)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()