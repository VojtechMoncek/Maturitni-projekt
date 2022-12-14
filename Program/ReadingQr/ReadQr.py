import math
import time
import cv2
import numpy as np

class QrReader():
    def __init__(self, img, height=1000, width=1000):
        self.debug = 1
        if self.debug: print("__init__")
        self.img = img
        self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.height = height
        self.width = width
    def loadImage(self, img):
        self.img = img
        #self.img = resizedImg = cv2.resize(img, (self.height,self.width), interpolation=cv2.INTER_AREA)
        cv2.imshow("camera", img)
        self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        #self.img = cv2.blur(self.img, (7, 7))

    def getFourPointsContours(self, contours):
        if self.debug: print("\ngetFourPointsContours()")


        newContours = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, .05 * cv2.arcLength(contour, True), True)
            rect = cv2.minAreaRect(contour)

            box = cv2.boxPoints(rect)
            box = np.int0(box)
            newContours.append(box)
            #if len(approx) == 4:
            #    newContours.append(approx)

        if self.debug: print(f"    {len(newContours)} contours found")

        _image = self.img.copy()
        #cv2.drawContours(_image, contours, -1, (255, 0, 0), 5)
        print(newContours)
        #cv2.drawContours(_image,np.array( newContours ), -1, (255, 0, 0), 10)
        cv2.imshow("wtf proc nic nedelas",_image)
        return newContours

    def getBiggestContour(self,contours, number=1):
        if self.debug: print("\ngetBiggestContour()")
        bigContours = []
        biggestContourSize = 0
        biggestContour = ""
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggestContourSize:
                biggestContour = contour
            if area > 1000:
                bigContours.append(contour)
        if self.debug: print(f"    Biggest contour: {biggestContour.tolist()[0],biggestContour.tolist()[1],biggestContour.tolist()[2],biggestContour.tolist()[3]}")


        img_contours = np.zeros(self.img.shape)
        _img = self.img.copy()
        #cv2.drawContours(_img, contours, -1, (255, 0, 0), 3)
        cv2.imshow("bgst", _img)
        #cv2.drawContours(self.img, biggestContour, -1, (0, 255, 0), 3)
        #print("__Showing bigest contour")


        return biggestContour

    def getContours(self, img):
        if self.debug: print("\ngetContours()")

        ret, thresh_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(thresh_img, 100, 200)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if self.debug: print(f"    {len(contours)} contours found")

        #cv2.drawContours(self.img, contours, -1, (0, 0, 255), 1)
        cv2.imshow("thresh", thresh_img)

        return contours

    def warpQr(self, coordinates):
        if self.debug: print("\nwarpQr()")
        #print(coordinates)

        coordinates = np.float32(coordinates)



        finalCoordinates = np.float32([[0, 0], [0, self.height], [self.width, self.height], [self.width, 0]])


        matrix = cv2.getPerspectiveTransform(coordinates, finalCoordinates)
        warpedQr = cv2.warpPerspective(self.img, matrix, (self.width, self.height))
        #warpedQr = cv2.resize(warpedQr, (1000, 1000), interpolation=cv2.INTER_AREA)
        self.warpedQr = warpedQr
        return warpedQr

    def rotateQrAndGetNumberOfRaws(self, warpedQr):
        if self.debug: print("__rotateQrAndGetNumberOfRaws__")
        def distance(coordinate, coordinate2):
            print(coordinate, coordinate2)
            vector = [coordinate[0] - coordinate2[0], coordinate[1] - coordinate2[1]]
            distance = abs((vector[0] ** 2 + vector[1] ** 2)) ** 1 / 2
            return distance
        def getSquaredContours(img):
            cnts = self.getContours(img)
            fourPointsCnts = self.getFourPointsContours(cnts)

            #cv2.drawContours(warpedQr, fourPointsCnts, -1, (255, 0, 0), 3)

            squaredCnts = []
            for cnt in fourPointsCnts:
                cnt = cnt.tolist()
                squareArea = distance(cnt[0] , cnt[1])
                averageEdgeLenght = (distance(cnt[0] , cnt[1]) + distance(cnt[1] , cnt[2]) + distance(cnt[2] , cnt[3]) + distance(cnt[3] , cnt[0])) / 4
                squareArea *= 2
                if averageEdgeLenght + averageEdgeLenght/5 >= squareArea**1/2 and averageEdgeLenght - averageEdgeLenght/5 <= squareArea**1/2:
                    squaredCnts.append(cnt)

            #cv2.drawContours(self.img, np.array(squaredCnts), -1, (0, 0, 255), 1)
            return squaredCnts

        def findContourInCorner(cnts):
            dic = []
            distances = []
            inCorner = []
            inCorner2 = []
            for cnt in cnts:

                #print(cnt)
                listX = [cnt[0][0], cnt[1][0], cnt[2][0], cnt[3][0]]
                listY = [cnt[0][1], cnt[1][1], cnt[2][1], cnt[3][1]]
                listX.sort()
                listY.sort()


                leftX = listX[0]
                rightX = listX[3]
                topY = listY[0]
                bottomY = listY[3]
                dic.append({"cnt": cnt, "left": leftX, "right": rightX, "top": topY, "bottom": bottomY})

                x = [leftX, self.width - leftX]
                y = [topY, self.height - bottomY]
                distances.append([x, y])

                if x[0] > (y[0] - self.width/100) and x[0] < (y[0] + self.width/100):
                    inCorner.append(cnt)

                elif x[0] > (y[1] - self.width/100) and x[0] < (y[1] + self.width/100):
                    inCorner.append(cnt)
                else:
                    pass
            closest = self.width - dic[0]["right"]
            closestCnt = dic[0]
            for square in dic:
                if (square["left"] + self.width/100) >= (self.width - square["right"]) and square["left"] - self.width/100<= (self.width - square["right"]):
                    continue
                if self.width - square["right"] < square["left"]:

                    if self.width - square["right"] < closest:

                        if closest + self.width/100 > self.width - square["right"]:

                            if cv2.contourArea(np.array(closestCnt["cnt"])) < cv2.contourArea(np.array(square["cnt"])) + self.width/100:
                                closestCnt = square
                        else:
                            closest = self.width - square["right"]

                            closestCnt = square
                else:
                    if square["left"] < closest:
                        if closest + self.width / 100 > self.width - square["right"]:

                            if cv2.contourArea(np.array(closestCnt["cnt"])) < cv2.contourArea(np.array(square["cnt"])) + self.width/100:
                                closestCnt = square
                        else:
                            closest = self.width - square["right"]
                            closestCnt = square

                        #closest = square["left"]
                        #closestCnt = square
            #cv2.drawContours(warpedQr, np.array(inCorner), -1, (0, 0, 255), 3)
            #cv2.drawContours(warpedQr, np.array(closestCnt["cnt"]), -1, (255, 0, 255), 10)
            return closestCnt

        def rotateQr(cnt):
            #left top
            warpedQr_ = warpedQr
            if cnt["left"] < self.width - cnt["right"] and cnt["top"] < self.width - cnt["bottom"]:
                warpedQr_ = warpedQr
            #right top
            elif cnt["left"] > self.width - cnt["right"] and cnt["top"] < self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            # left bottom
            elif cnt["left"] < self.width - cnt["right"] and cnt["top"] > self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            # right bottom
            elif cnt["left"] > self.width - cnt["right"] and cnt["top"] > self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            return warpedQr_

        squaredCnts = getSquaredContours(warpedQr)
        cnt = findContourInCorner(squaredCnts)
        warpedQr = rotateQr(cnt)
        cv2.imshow("wq", warpedQr)
        raws = abs( round(self.width / ((cnt["right"] - cnt["left"]) / 3)) )
        #print(raws) {'cnt': [[[71, 71]], [[282, 71]], [[282, 287]], [[69, 285]]], 'left': 69, 'right': 282, 'top': 71, 'bottom': 287}
        return warpedQr, raws

    """
    def getNumberOfRaws(self, warpedQr):
        if self.debug: print("\ngetNumberOfRaws")
        ret, thresh_img = cv2.threshold(warpedQr, 100, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(thresh_img, 100, 200)
        #cv2.imshow("warpedQR", canny)

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        smallestContourSize = 999999
        smallestContour = ""
        shortestContourLenght = 999999
        shortestContour = ""


        #img_contours = np.zeros(self.img.shape)


        squaredContours = self.getFourPointsContours(contours)
        for contour in squaredContours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if shortestContourLenght > perimeter:
                shortestContourLenght = perimeter
                shortestContour = contour

            if area < smallestContourSize:
                smallestContour = contour
                smallestContourSize = area
        #cv2.drawContours(warpedQr, shortestContour, -1, (0, 0, 255), 10)

        #print("__smallest squared contour__")
        #cv2.imshow("smallest squared contour", self.warpedQr)

        pixelHeight = math.ceil((len(warpedQr) / 14))#math.ceil(shortestContourLenght/4)
        raws = math.ceil(len(warpedQr)/pixelHeight)
        
        if self.debug: print(f"    raws: {raws}")
        return raws
    """
    def readPixels(self, warpedQr, raws):
        if self.debug: print("\nreadPixels()")
        pixelHeight = math.ceil(len(warpedQr)/raws)
        if self.debug: print(f"    Pixel Height: {pixelHeight}px (raws: {raws})")
        ret, thresh_img = cv2.threshold(warpedQr, 100, 255, cv2.THRESH_BINARY)
        data = []
        for raw in range(0, raws):
            rawData = []
            for collumn in range(0, raws):

                pixelValue = 0
                _pixel = thresh_img[(raw * pixelHeight):(raw * pixelHeight + pixelHeight),
                         (collumn * pixelHeight):(collumn * pixelHeight + pixelHeight)]
                pixel = _pixel.tolist()

                for x in pixel:
                    if x.count([255, 255, 255]) > x.count([0, 0, 0]):
                        pixelValue += 1
                    else:
                        pixelValue -= 1


                if pixelValue < 0:
                    rawData.append(1)
                else:
                    rawData.append(0)

            data.append(rawData)

        return data

    def decodeData(self, data):
        if self.debug: print("\ndecodeData()")
        def removeBorders(data):
            #return data
            if self.debug: print(f"    Data:")
            if self.debug: print(f"        With borders: {data}")

            while True:
                if (data[0].count(1) == len(data[0]) and data[-1].count(1) == len(data)) or (data[0].count(0) == len(data[0]) and data[-1].count(0) == len(data)):
                    for i, x in enumerate(data):

                        del data[i][-1]
                        del data[i][0]

                    del data[0]
                    del data[len(data)-1]
                else:
                    break

            if self.debug: print(f"        Data without borders: {data}")
            return data


        def decodeData(data, size=5):

            newData = []
            newDataRow = ""
            for x_, x in enumerate(data):
                for y_, y in enumerate(x):
                    #print(x_,y_)
                    if x_ < 4 and y_ < 4:
                        print(y)
                    else:
                        newDataRow += str(y)
                        if (len(newDataRow)) % size == 0:
                            newData.append("0b" + newDataRow)
                            #print(newDataRow)
                            newDataRow = ""
            if self.debug: print(newData)

            def listToDecimal(data):
                decimalList = []
                for a in data:
                    decimalList.append(int(a, 2))
                return decimalList
            decimalList = listToDecimal(newData)

            return decimalList

        dataWithoutBorders = removeBorders(data)

        data = decodeData(dataWithoutBorders)

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
        text = convertToText(data)
        if self.debug: print(f"    Text: {text}")
        return text

    def main(self, img):
        #resizedImg = cv2.resize(img, (1000,1000), interpolation=cv2.INTER_AREA)
        self.loadImage(img)
        contours = self.getContours(self.grayImg)
        fourPointContours = self.getFourPointsContours(contours)
        biggestContour = self.getBiggestContour(fourPointContours)
        warpedQr = self.warpQr(biggestContour)
        warpedQr, raws = self.rotateQrAndGetNumberOfRaws(warpedQr)
        CryptedData = self.readPixels(warpedQr, raws)
        EncryptedData = self.decodeData(CryptedData)
        print(raws)
        print(EncryptedData)
        """
        try:
            self.loadImage(img)
            contours = self.getContours(self.grayImg)
            fourPointContours = self.getFourPointsContours(contours)
            biggestContour = self.getBiggestContour(fourPointContours)
            warpedQr = self.warpQr(biggestContour)
            warpedQr, raws = self.rotateQrAndGetNumberOfRaws(warpedQr)
            CryptedData = self.readPixels(warpedQr, raws-1)
            EncryptedData = self.decodeData(CryptedData)
            print(raws)
            print(EncryptedData)
        except Exception as e:
            print("fail")
            print(e)
        """

        #print("\n________________\n")
        #print(f"Text: {EncryptedData}")

if __name__ == "__main__":
    """
    cam = cv2.VideoCapture(0)

    img = cv2.imread("example4.jpg")
    qrReader = QrReader(img)
    qrReader.debug = 0
    while True:
        ret, frame = cam.read()
        cv2.imshow("kamera", frame)
        if cv2.waitKey(1) & 0xFF == ord('x'):

            qrReader.main(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cam.release()
    """

    img = cv2.imread("example11.png")
    qrReader = QrReader(img)
    qrReader.main(img)
    cv2.imshow("kamera", img)
    cv2.waitKey(-1)