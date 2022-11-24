import math
import cv2
import numpy as np


class QrReader():
    def __init__(self, img, height=1000, width=1000):
        print("__init__")
        self.img = img
        self.grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.height = height
        self.width = width

    def getFourPointsContours(self, contours):
        print("\ngetFourPointsContours()")


        newContours = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                newContours.append(approx)
        print(f"    {len(newContours)} contours found")
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
        print(f"    Biggest contour: {biggestContour.tolist()[0],biggestContour.tolist()[1],biggestContour.tolist()[2],biggestContour.tolist()[3]}")


        #img_contours = np.zeros(self.img.shape)
        #cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
        #cv2.drawContours(img_contours, biggestContour, -1, (0, 255, 0), 10)
        #print("__Showing bigest contour")


        return biggestContour

    def getContours(self):
        print("\ngetContours()")

        ret, thresh_img = cv2.threshold(self.grayImg, 100, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(thresh_img, 100, 200)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        print(f"    {len(contours)} contours found")
        return contours

    def warpQr(self, coordinates):
        print("\nwarpQr()")

        coordinates = coordinates.tolist()
        newCoordinates = []
        for cor in coordinates:
            newCoordinates.append(cor[0])
        coordinates = np.float32(newCoordinates)



        finalCoordinates = np.float32([[0, 0], [0, self.height], [self.width, self.height], [self.width, 0]])


        matrix = cv2.getPerspectiveTransform(coordinates, finalCoordinates)
        warpedQr = cv2.warpPerspective(self.img, matrix, (self.width, self.height))
        return warpedQr

    def getNumberOfRaws(self, warpedQr):
        print("\ngetNumberOfRaws")
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
        cv2.drawContours(warpedQr, shortestContour, -1, (0, 0, 255), 10)
        #print("__smallest squared contour__")
        #cv2.imshow("smallest squared contour", self.warpedQr)

        pixelHeight = math.ceil((len(warpedQr) / 7))#math.ceil(shortestContourLenght/4)
        raws = math.ceil(len(warpedQr)/pixelHeight)
        print(f"    raws: {raws}")
        return raws

    def readPixels(self, warpedQr, raws):
        print("\nreadPixels()")
        pixelHeight = math.ceil(self.height/raws)
        print(f"    Pixel Height: {pixelHeight}px")
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
        print("\ndecodeData()")
        def removeBorders(data):
            #return data
            print(f"    Data:")
            print(f"        With borders: {data}")

            while True:
                if (data[0].count(1) == len(data[0]) and data[-1].count(1) == len(data)) or (data[0].count(0) == len(data[0]) and data[-1].count(0) == len(data)):
                    for i, x in enumerate(data):

                        del data[i][-1]
                        del data[i][0]

                    del data[0]
                    del data[len(data)-1]
                else:
                    break


            print(f"        Data without borders: {data}")
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
            #print(newData)

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
        print(f"    Text: {text}")
        return text

    def main(self, img):
        self.img = img

        contours = self.getContours()
        fourPointContours = self.getFourPointsContours(contours)
        biggestContour = self.getBiggestContour(fourPointContours)
        warpedQr = self.warpQr(biggestContour)
        raws = self.getNumberOfRaws(warpedQr)
        CryptedData = self.readPixels(warpedQr, raws)
        EncryptedData = self.decodeData(CryptedData)

        print("\n________________\n")
        print(f"Text: {EncryptedData}")


if __name__ == "__main__":
    img = cv2.imread("example1.png")

    qrReader = QrReader(img)
    for x in range(100):
        qrReader.main(img)




    cv2.waitKey(0)
    #qrReader.showImg()
