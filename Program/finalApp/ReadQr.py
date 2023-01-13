import time
import cv2
import numpy as np


class QrReader():
    def __init__(self, img, height=1000, width=1000):
        self.debug = 0
        if self.debug: print("__init__")
        self.img = img
        self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.height = height
        self.width = width
        self.brightness = 150

    def loadImage(self, img):
        errorMessage = ""
        try:
            self.img = img
            # self.img = resizedImg = cv2.resize(img, (self.height,self.width), interpolation=cv2.INTER_AREA)


            self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        except:
            errorMessage = "Can not load image"
        return errorMessage

    def getFourPointsContours(self, contours):
        errorMessage = ""
        if self.debug: print("\ngetFourPointsContours()")
        if len(contours) == 0: errorMessage = "No contours in argument"

        newContours = []
        for contour in contours:
            try:

                approx = cv2.approxPolyDP(contour, .01 * cv2.arcLength(contour, True), True)
                rect = cv2.minAreaRect(approx)

                box = cv2.boxPoints(rect)
                box = np.int0(box)
                if len(approx) == 4:
                    newContours.append(approx)

                #   newContours.append(approx)
            except:
                pass
        if self.debug: print(f"    {len(newContours)} contours found")

        # print(newContours)
        # cv2.drawContours(_image,np.array( newContours ), -1, (255, 0, 0), 10)

        if len(newContours) == 0: errorMessage = "No Four points contours in argument"
        return newContours, errorMessage

    def getBiggestContour(self, contours, number=1):
        errorMessage = ""
        if self.debug: print("\ngetBiggestContour()")
        bigContours = []
        biggestContourSize = 0
        biggestContour = ""
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > biggestContourSize:
                biggestContourSize = area
                biggestContour = contour
                #print(area)
            if area > 1000:
                #print(area)
                bigContours.append(contour)

        if self.debug: print(
            f"    Biggest contour: {biggestContour.tolist()[0], biggestContour.tolist()[1], biggestContour.tolist()[2], biggestContour.tolist()[3]}")


        _img = self.img.copy()

        if len(biggestContour) == 0: errorMessage = "Biggest Contour not found"
        return biggestContour, errorMessage

    def getContours(self, img):
        startTime = time.time()
        errorMessage = ""
        if self.debug: print("\ngetContours()")
        img = cv2.blur(img, (7, 7))
        #print(f"t1 {time.time() - startTime}")
        try:
            thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        except:
            ret, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        #print(f"t {time.time() - startTime}")
        canny = cv2.Canny(thresh_img, 100, 200)

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if self.debug: print(f"    {len(contours)} contours found")

        if len(contours) == 0: errorMessage = "No contours found"
        #print(f"t fish {time.time() - startTime}")
        return contours, errorMessage

    def warpQr(self, coordinates):
        errorMessage = ""
        if len(coordinates) == 0: "No coordinates given"
        if self.debug: print("\nwarpQr()")
        try:
            coordinates = np.float32(coordinates)

            finalCoordinates = np.float32([  [0, self.height] ,[0, 0],  [self.width, 0]  ,[self.width, self.height]  ])


            matrix = cv2.getPerspectiveTransform(coordinates, finalCoordinates)
            warpedQr = cv2.warpPerspective(self.img, matrix, (self.width, self.height))
            self.warpedQr = warpedQr
        except:
            errorMessage = "Failed to warp qr"
            warpedQr = ""
        return warpedQr, errorMessage

    def rotateQrAndGetNumberOfRaws(self, warpedQr):
        timeFceStart = time.time()
        errorMessage = ""
        if self.debug: print("__rotateQrAndGetNumberOfRaws__")

        def distance(coordinate, coordinate2):

            vector = [coordinate[0][0] - coordinate2[0][0], coordinate[0][1] - coordinate2[0][1]]
            distance = abs((vector[0] ** 2 + vector[1] ** 2)) ** 1 / 2
            return distance

        def getSquaredContours(cnts):
            def getFourPointsContours(contours):
                errorMessage = ""
                if self.debug: print("\ngetFourPointsContours()")
                if len(contours) == 0: errorMessage = "No contours in argument"

                newContours = []
                for contour in contours:
                    try:

                        convexHull = cv2.convexHull(contour)
                        approx = cv2.approxPolyDP(convexHull, .01 * cv2.arcLength(contour, True), True)
                        rect = cv2.minAreaRect(approx)


                        if len(approx) == 4:
                            newContours.append(approx)

                    except:
                        pass

                return newContours

            cnts = cnts[0]

            fourPointsCnts = getFourPointsContours(cnts)


            squaredCnts = []
            for cnt in fourPointsCnts:

                squareArea = distance(cnt[0], cnt[1])
                averageEdgeLenght = (distance(cnt[0], cnt[1]) + distance(cnt[1], cnt[2]) + distance(cnt[2],
                                                                                                    cnt[3]) + distance(
                    cnt[3], cnt[0])) / 4
                squareArea *= 2
                if averageEdgeLenght + averageEdgeLenght / 5 >= squareArea ** 1 / 2 and averageEdgeLenght - averageEdgeLenght / 5 <= squareArea ** 1 / 2:
                    squaredCnts.append(cnt)

            return squaredCnts

        def findContourInCorner(cnts):
            errorMessage = ""
            cv2.drawContours(warpedQr, np.array(cnts), -1, (0, 0, 255), 1)

            dic = []
            distances = []
            inCorner = []
            for cnt in cnts:
                listX = [cnt[0][0][0], cnt[1][0][0], cnt[2][0][0], cnt[3][0][0]]

                listY = [cnt[0][0][1], cnt[1][0][1], cnt[2][0][1], cnt[3][0][1]]
                listX.sort()
                listY.sort()

                leftX = listX[0]
                rightX = listX[3]
                topY = listY[0]
                bottomY = listY[3]

                x = [leftX, self.width - leftX]
                y = [topY, self.height - bottomY]
                distances.append([x, y])

                if x[0] > (y[0] - self.width / 100) and x[0] < (y[0] + self.width / 100):
                    dic.append({"cnt": cnt, "left": leftX, "right": rightX, "top": topY, "bottom": bottomY})
                    inCorner.append(cnt)

                elif x[0] > (y[1] - self.width / 100) and x[0] < (y[1] + self.width / 100):
                    dic.append({"cnt": cnt, "left": leftX, "right": rightX, "top": topY, "bottom": bottomY})
                    inCorner.append(cnt)
                else:
                    pass
            if len(dic) == 0: return []
            closest = self.width - dic[0]["right"]
            closestCnt = dic[0]
            for square in dic:
                if (square["left"] + self.width / 100) >= (self.width - square["right"]) and square[
                    "left"] - self.width / 100 <= (self.width - square["right"]):
                    continue
                if self.width - square["right"] < square["left"]:

                    if self.width - square["right"] < closest:

                        if closest + self.width / 100 > self.width - square["right"]:

                            if cv2.contourArea(np.array(closestCnt["cnt"])) < cv2.contourArea(
                                    np.array(square["cnt"])) + self.width / 100:
                                closestCnt = square
                        else:
                            closest = self.width - square["right"]

                            closestCnt = square
                else:
                    if square["left"] < closest:
                        if closest + self.width / 100 > self.width - square["right"]:

                            if cv2.contourArea(np.array(closestCnt["cnt"])) < cv2.contourArea(
                                    np.array(square["cnt"])) + self.width / 100:
                                closestCnt = square
                        else:
                            closest = self.width - square["right"]
                            closestCnt = square


            if len(inCorner) == 0: errorMessage = "Corner square not found"
            return closestCnt

        def rotateQr(cnt):
            # left top
            warpedQr_ = warpedQr
            if cnt["left"] < self.width - cnt["right"] and cnt["top"] < self.width - cnt["bottom"]:
                warpedQr_ = warpedQr
            # right top
            elif cnt["left"] > self.width - cnt["right"] and cnt["top"] < self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_COUNTERCLOCKWISE)
                #warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
                #warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            # left bottom
            elif cnt["left"] < self.width - cnt["right"] and cnt["top"] > self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            # right bottom
            elif cnt["left"] > self.width - cnt["right"] and cnt["top"] > self.width - cnt["bottom"]:
                warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_180)
                #warpedQr_ = cv2.rotate(warpedQr_, cv2.ROTATE_90_CLOCKWISE)
            return warpedQr_


        gray = cv2.cvtColor(warpedQr, cv2.COLOR_BGR2GRAY)
        #print(f"tf1 {time.time() - timeFceStart}")
        #Meneni jasu
        ret, thresh_img = cv2.threshold(gray, self.brightness, 255, cv2.THRESH_BINARY)


        #print(f"tf1.2 {time.time() - timeFceStart}")
        cnts = self.getContours(thresh_img)
        #print(f"tf1.3 {time.time() - timeFceStart}")
        squaredCnts = getSquaredContours(cnts)
        #print(f"tf2 {time.time() - timeFceStart}")
        cnt = findContourInCorner(squaredCnts)
        try:
            cv2.drawContours(warpedQr, cnt, -1, (255,0,0), 3)
        except:
            pass

        if cnt == []: return warpedQr, 1, "Square in corner not found"
        warpedQr = cv2.resize(warpedQr, (250, 250))
        warpedQr = rotateQr(cnt)
        #print(f"tf3 {time.time() - timeFceStart}")
        pixelHeight = ((cnt["right"] - cnt["left"]) / 3)
        pixelHeight = cv2.contourArea( cnt["cnt"] ) ** (1/2) / 3
        #print(pixelHeight)
        #meneni tolerance
        pixelHeight -= pixelHeight/15
        if pixelHeight < 1: errorMessage = "pixelHeight == 0"; pixelHeight = 10
        raws = abs(round(self.width / pixelHeight))
        #print(f"tf4 {time.time() - timeFceStart}")
        return warpedQr, raws, errorMessage



    def readPixels(self, warpedQr, raws):
        errorMessage = ""
        if self.debug: print("\nreadPixels()")

        pixelHeight = len(warpedQr) / raws
        if self.debug: print(f"    Pixel Height: {pixelHeight}px (raws: {raws})")
        #meneni jasu
        ret, thresh_img = cv2.threshold(warpedQr, self.brightness, 255, cv2.THRESH_BINARY)
        data = []
        for raw in range(0, raws):
            rawData = []
            for collumn in range(0, raws):

                pixelValue = 0
                _pixel = thresh_img[round(raw * pixelHeight):round(raw * pixelHeight + pixelHeight),
                         round(collumn * pixelHeight):round(collumn * pixelHeight + pixelHeight)]
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
        if len(data) == 0: errorMessage = "Loaded zero pixels"
        return data, errorMessage

    def decodeData(self, data):
        errorMessage = ""
        if self.debug: print("\ndecodeData()")

        def removeBorders(data):
            #print(data)
            # return data
            if self.debug: print(f"    Data:")
            if self.debug: print(f"        With borders: {data}")

            while len(data) > 1:
                if (data[0].count(1) == len(data[0]) and data[-1].count(1) == len(data)) or (
                        data[0].count(0) == len(data[0]) and data[-1].count(0) == len(data)):
                    for i, x in enumerate(data):
                        del data[i][-1]
                        del data[i][0]

                    del data[0]
                    del data[len(data) - 1]
                else:
                    break

            if self.debug: print(f"        Data without borders: {data}")
            if len(data) == 0: errorMessage = "No data"

            return data

        def decodeData(data, size=5):

            newData = []
            newDataRow = ""
            for x_, x in enumerate(data):
                for y_, y in enumerate(x):
                    # print(x_,y_)
                    if x_ < 4 and y_ < 4:
                        pass
                    else:
                        newDataRow += str(y)
                        if (len(newDataRow)) % size == 0:
                            newData.append("0b" + newDataRow)
                            # print(newDataRow)
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

        return text, errorMessage

    def main(self, img):
        startTime = time.time()

        # resizedImg = cv2.resize(img, (1000,1000), interpolation=cv2.INTER_AREA)
        self.loadImage(img)
        contours, msg = self.getContours(self.grayImg)
        _image = self.grayImg.copy()

        fourPointContours, msg = self.getFourPointsContours(contours)

        #print(f"t1 {time.time() - startTime}")
        biggestContour, msg = self.getBiggestContour(fourPointContours)

        warpedQr, msg = self.warpQr(biggestContour)
        if warpedQr == "": return
        brightness =  warpedQr
        brightness = np.mean(brightness, axis=(0,1))
        brightness = brightness[0] * 0.59 + brightness[1] * 0.11 + brightness[2] * 0.3
        #print(f"br {brightness}")
        self.brightness = brightness * .85

        #print(f"t2 {time.time() - startTime}")

        # cv2.drawContours(warpedQr, fourPointContours, -1, (0, 0, 255), 3)
        # print(msg

        warpedQr, raws, msg = self.rotateQrAndGetNumberOfRaws(warpedQr)

        if raws == 1 or raws == 100:
            return ""
        else:
            print(f"raws: {raws}", end=", ")
        #print(f"t3 {time.time() - startTime}")
        CryptedData, msg = self.readPixels(warpedQr, raws)
        #print(f"C data: {CryptedData}, {msg}", end=", ")
        if len(CryptedData) > 100: return ""
        print(f"Crypted data: {CryptedData}")
        #if len(CryptedData) > 0: print(f"len crypted: {len(CryptedData)}")
        EncryptedData, msg = self.decodeData(CryptedData)
        finishTime = time.time() - startTime
        if len(EncryptedData) > 0:
            print(f"data: {EncryptedData}")
            #print(f"cas: {finishTime}")
        return EncryptedData
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

        # print("\n________________\n")
        # print(f"Text: {EncryptedData}")


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

    img = cv2.imread("C:/Users/moncevo19/PycharmProjects/Maturitni-projekt/Program/ReadingQr/examples/qr (30).jpg")

    img = cv2.resize(img, ( round(img.shape[1] * 500/img.shape[1]), round(img.shape[0] * 500/img.shape[1])), interpolation=cv2.INTER_AREA)
    qrReader = QrReader(img)
    text = qrReader.main(img)







    cv2.waitKey(-1)