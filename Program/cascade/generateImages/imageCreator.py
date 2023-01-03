import random
from Program.generateQr import generateQr
import cv2
import os
import numpy as np
from PIL import Image
import imutils
if __name__ == "__main__":

    generateQr = generateQr.GenerateQr(10)
    def createQrs():
        chars = "abcdefghijklmnopqrstuvwxyz .,?-"
        texts = []
        for i in range(4000):
            text = ""
            for j in range(random.randrange(10,150)):
                text += chars[random.randrange(0,len(chars))]
            texts.append(text)


        for x in range(len(texts)):
            codedText = generateQr.codeText(texts[x])

            qr = generateQr.fillImageWithData(codedText)
            qr = generateQr.resizeQr(qr, random.randrange(50,500))
            randomness1 = 0, 200
            randomness2 = 800, 1000
            finalCoordinates = np.float32([[random.randrange(*randomness1), random.randrange(*randomness1)], [random.randrange(*randomness2), random.randrange(*randomness1)], [random.randrange(*randomness2), random.randrange(*randomness2)], [random.randrange(*randomness1), random.randrange(*randomness2)]])

            coordinates = np.float32( ((0,0), (qr.shape[0], 0), (qr.shape[0], qr.shape[1]), (0, qr.shape[1]) ))
            matrix = cv2.getPerspectiveTransform(coordinates, finalCoordinates)

            qr = cv2.cvtColor(qr, cv2.COLOR_BGR2BGRA)
            warpedQr = cv2.warpPerspective(qr, matrix, (1000, 1000))

            warpedQr = imutils.rotate_bound(warpedQr, random.randrange(0,360))
            warpedQr = generateQr.resizeQr(warpedQr, random.randrange(100, 700))
            #cv2.imshow(f"{filename}big", lImg)
            #cv2.imshow(str(x), warpedQr)
            #warpedQr = cv2.addWeighted(warpedQr, random.randrange(4,14) /10, warpedQr, 1, 1)
            bright = random.randrange(4,14)/10
            warpedQr[:, :, 0] = cv2.multiply(warpedQr[:, :, 0], bright)
            warpedQr[:, :, 1] = cv2.multiply(warpedQr[:, :, 1], bright)
            warpedQr[:, :, 2] = cv2.multiply(warpedQr[:, :, 2], bright)
            #warpedQr = cv2.convertScaleAbs(warpedQr, alpha=0.5)

            cv2.imwrite("qrs/" + str(x) + ".png", warpedQr)
            #images.append(qr)
    def placeQrOnImage(qr, img,ImageWithQr):
        imgQr = Image.open(qr)
        img = Image.open(img)

        #imgQr = imgQr.resize((100, 100))
        xMaxPos = img.width - imgQr.width
        yMaxPos = img.height - imgQr.height
        #print(imgQr.width)
        #print(img.width)
        #print()
        xPos = random.randrange(0, xMaxPos)
        yPos = random.randrange(0, yMaxPos)
        img.paste(imgQr, (xPos, yPos), imgQr)
        img.save(ImageWithQr)
    #createQrs()
    intI = 840
    file = os.listdir("C:/Users/moncevo19/Downloads/archive")

    for i, filename in enumerate(file):
        try:
            placeQrOnImage(f"qrs/{intI}.png", f"C:/Users/moncevo19/Downloads/archive/{filename}", f"imagesWithQr/{intI}.jpg")
            print(intI)
            intI += 1
        except Exception as e:
            print(intI)
            print(f"        {e}")

       #placeQrOnImage()
    #codedText = generateQr.codeText(texts[random.randrange(0, len(texts))])

    #qr = generateQr.fillImageWithData(codedText)
    #qr = generateQr.resizeQr(qr, 500)
    #cv2.imshow("img", qr)

    cv2.waitKey(0)
    cv2.destroyAllWindows()