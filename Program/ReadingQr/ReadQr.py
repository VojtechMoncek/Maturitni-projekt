import math
import cv2
import numpy as np


class QrReader():
    def __init__(self, img):
        print("__init__")
        self.img = img
        self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def getFourPointsContours(self, contours):
        print("\ngetFourPointsContours()")
        newContours = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                newContours.append(approx)

        return newContours

    def getBiggestContour(self,contours, number=1):
        print("\ngetBiggestContour()")
        bigContours = []
        biggestContourSize = 0
        biggestContour = ""
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggestContourSize:
                biggestContour = contour
            if area > 1000:
                bigContours.append(contour)
        print(f"    Biggest contour: \n{biggestContour}")
        img_contours = np.zeros(self.img.shape)


        #cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
        #cv2.drawContours(img_contours, biggestContour, -1, (0, 255, 0), 10)
        #print("__Showing bigest contour")


        return biggestContour
    def getContours(self):
        print("\ngetContours()")
        def getFourPointsRectangles(contours):
            newContours = []
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                if len(approx) == 4:
                    newContours.append(approx)

            return newContours

        ret, thresh_img = cv2.threshold(self.grayImg, 100, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(thresh_img, 100, 200)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return  contours
        """
        print(f"get 4 points contours")
        contours = getFourPointsRectangles(contours)

        bigContours = []
        biggestContourSize = 0
        biggestContour = ""
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggestContourSize:
                biggestContour = contour
            if area > 1000:
                bigContours.append(contour)
        print(f"__Biggest contour__\n{biggestContour}")
        img_contours = np.zeros(self.img.shape)

        cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
        cv2.drawContours(img_contours, biggestContour, -1, (0, 255, 0), 10)

        print("__Showing bigest contour")
        #cv2.imshow("Bigest contour", img_contours)
        #cv2.imshow("imgContours", thresh_img)

        return biggestContour
        """
    def getCorners(self):
        pass
        #contours = self.getContours()
        newContours = []
        #print(contours)
        #for contour in contours:
        #    if len(contour) == 4:
        #        pass
        """
            #print(contour)
            if len(contour) == 4:
                img_contours = np.zeros(self.img.shape)
                
                print(f"contour: {contour}")
                print(f"contour[0]: {contour[0][0]}")
                print(f"contour[1]: {contour[1][0]}")
                print(f"contour[2]: {contour[2][0]}")
                print(f"contour[3]: {contour[3][0]}")
                
                A = contour[0][0]
                B = contour[1][0]
                C = contour[2][0]
                D = contour[3][0]
                #print(A,B,C,D)

                a = (((A[0] - A[1]) ** 2 + (B[0] - B[1])) ** 2) ** (1 / 2)
                b = (((B[0] - B[1]) ** 2 + (C[0] - C[1])) ** 2) ** (1 / 2)
                c = (((C[0] - C[1]) ** 2 + (D[0] - D[1])) ** 2) ** (1 / 2)
                d = (((D[0] - D[1]) ** 2 + (A[0] - A[1])) ** 2) ** (1 / 2)
                #print(f"delka {a}, {b}, {c}, {d}")

                #print(contour)
                if (a+b+c+d):
                    print(f"{a} + {b} + {c} + {d} | {a + b + c + d}")
                newContours.append(contour)
                #print(img_contours)

            """


    def warpQr(self):
        width = 1000
        height = 1000

        contours = self.getContours()
        FourPointContours = self.getFourPointsContours(contours)
        BiggestContour = self.getBiggestContour(FourPointContours)
        coordinates = BiggestContour
        #coordinates = self.getContours()

        coordinates = coordinates.tolist()

        newCoordinates = []
        for cor in coordinates:
            newCoordinates.append(cor[0])

        coordinates = np.float32(newCoordinates)



        finalCoordinates = np.float32([[0, 0], [0, height], [width, height], [width, 0]])

        try:
            print(f"__Warping__")
            matrix = cv2.getPerspectiveTransform(coordinates, finalCoordinates)
            warpedQr = cv2.warpPerspective(self.img, matrix, (width, height))

            self.warpedQr = warpedQr
            #cv2.imshow("qr", warpedQr)
        except:
            print(f"__Warping failed__")

    def getSize(self):
        ret, thresh_img = cv2.threshold(self.warpedQr, 100, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(thresh_img, 100, 200)
        #cv2.imshow("warpedQR", canny)

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        smallestContourSize = 999999
        smallestContour = ""
        shortestContourLenght = 999999
        shortestContour = ""


        img_contours = np.zeros(self.img.shape)
        def getFourPointsRectangles(contours):
            newContours = []
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                if len(approx) == 4:

                    newContours.append(approx)

            return newContours

        #epsilon = 0.1 * cv2.arcLength(smallestContour, True)
        #approxContour = cv2.approxPolyDP(smallestContour, epsilon, True)
        #cv2.drawContours(img_contours, smallestContour, -1, (0, 255, 0), 3)

        squaredContours = getFourPointsRectangles(contours)
        for contour in squaredContours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if shortestContourLenght > perimeter:
                shortestContourLenght = perimeter
                shortestContour = contour

            if area < smallestContourSize:
                smallestContour = contour
                smallestContourSize = area
        cv2.drawContours(self.warpedQr, shortestContour, -1, (0, 0, 255), 10)
        print("__smallest squared contour__")
        #cv2.imshow("smallest squared contour", self.warpedQr)

        pixelHeight = math.ceil((len(self.warpedQr) / 7))#math.ceil(shortestContourLenght/4)
        rows = math.ceil(len(self.warpedQr)/pixelHeight)
        print(f"__Number of rows: {1000 / pixelHeight}__")


        print("__recognizing pixels__")
        print(thresh_img[0:1,0:2])
        data = []
        for row in range(0,rows):
            rowData = []
            print(row)
            for collumn in range(0,rows):

                pixelValue = 0
                _pixel = thresh_img[(row * pixelHeight):(row * pixelHeight + pixelHeight), (collumn * pixelHeight):(collumn * pixelHeight + pixelHeight)]
                pixel = _pixel.tolist()

                for x in pixel:
                    if x.count([255, 255, 255]) > x.count([0, 0, 0]):
                        pixelValue += 1
                    else:
                        pixelValue -= 1

                #pixelList.append()
                #if row == 0:

                    #cv2.imshow(f"{row}, {collumn}", _pixel)
                #print(pixelValue, end="")
                #black = pixel[0].count([255, 255, 255])
                #white = pixel[0].count([0, 0, 0])
                #print(f"black: {black}, white: {white}, result: {pixelValue}")
                if pixelValue < 0:
                    rowData.append(1)
                    print(1)
                else:
                    rowData.append(0)
                    print(0)
            print("\n")
            data.append(rowData)
        #print(data)
        #print(thresh_img)
        #cv2.imshow("treshold", thresh_img)
        return data
    def readPixels(self, data):

        def removeBorders(data):
            #return data
            print("__Data__")
            print(f"with borders: \n{data}")

            while True:
                if (data[0].count(1) == len(data[0]) and data[-1].count(1) == len(data)) or (data[0].count(0) == len(data[0]) and data[-1].count(0) == len(data)):
                    for i, x in enumerate(data):

                        del data[i][-1]
                        del data[i][0]
                        print(i)

                    del data[0]
                    del data[len(data)-1]
                else:
                    break


            print(f"data without borders: \n{data}")
            return data

        def decodeData(data, size=5):
            newData = []
            newDataRow = ""
            for x in data:
                for y in x:
                    newDataRow += str(y)
                    if (len(newDataRow)) % size == 0:
                        newData.append("0b" + newDataRow)
                        #print(newDataRow)
                        newDataRow = ""
            print(newData)

            def listToDecimal(data):
                decimalList = []
                for a in data:
                    decimalList.append(int(a, 2))
                return decimalList
            decimalList = listToDecimal(newData)

            return decimalList

        data = removeBorders(data)
        data = decodeData(data)

        def convertToText(data):
            convertor = {
                0: " ",
                1: "a",
                2: "b",
                3: "c",
                4: "d",
                5: "e",
                6: "f",
                7: "g",
                8: "h",
                9: "i",
                10: "j",
                11: "k",
                12: "l",
                13: "m",
                14: "n",
                15: "o",
                16: "p",
                17: "q",
                18: "r",
                19: "s",
                20: "t",
                21: "u",
                22: "v",
                23: "w",
                24: "x",
                25: "y",
                26: "z",
                27: ".",
                28: ",",
                29: "/",
                30: "_",
                31: "!",
            }
            text = ""
            for x in data:
                text += convertor[x]

            return text
        data = convertToText(data)
        print(data)



    def decodePixels(self):
        pass

    def returnImg(self):
        return self.img

    def showImg(self):
        #cv2.imshow("imgGray", self.grayImg)
        #cv2.imshow("img", img)
        #cv2.waitKey(0)
        pass

#img = cv2.imread("qrExample.png")
img = cv2.imread("example1.png")


qrReader = QrReader(img)
qrReader.warpQr()
data = qrReader.getSize()
qrReader.readPixels(data)
cv2.waitKey(0)
#qrReader.showImg()
