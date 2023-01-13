import math
import cv2
import numpy as np

class GenerateQr():
    def __init__(self,width):
        self.width = width
        self.height = width
        self.pixelWidth = width
        self.additionalDataLenght = 16 + 10

    def codeText(self, text):

        convertor = {
            " ": "00000",
            "a": "00001",
            "b": "00010",
            "c": "00011",
            "d": "00100",
            "e": "00101",
            "f": "00110",
            "g": "00111",
            "h": "01000",
            "i": "01001",
            "j": "01010",
            "k": "01011",
            "l": "01100",
            "m": "01101",
            "n": "01110",
            "o": "01111",
            "p": "10000",
            "q": "10001",
            "r": "10010",
            "s": "10011",
            "t": "10100",
            "u": "10101",
            "v": "10110",
            "w": "10111",
            "x": "11000",
            "y": "11001",
            "z": "11010",
            ".": "11011",
            ",": "11100",
            "/": "11101",
            "_": "11110",
            "!": "11111"
        }
        codedText = "10101"
        for char in text:
            try:
                codedText += convertor[char]
            except:
                codedText += "00000"
            #print(char)
        codedText += "10101"

        return codedText

    def fillImageWithData(self, data):

        def getSize(textLenght):
            lenght = textLenght + self.additionalDataLenght
            widthNoBorders = math.ceil(lenght ** (1 / 2))
            widthWithBorders = widthNoBorders + 4
            return widthWithBorders

        columns = getSize(len(data))
        self.width = self.pixelWidth * columns
        self.height = self.pixelWidth * columns
        img = np.zeros((self.pixelWidth * columns, self.pixelWidth * columns, 3), dtype=np.uint8)

        #print(pixelWidth)

        cv2.rectangle(img, (0, 0), (self.width, self.height),(255, 255, 255), -1) #white border
        cv2.rectangle(img, (self.pixelWidth, self.pixelWidth), (self.width - self.pixelWidth, self.height - self.pixelWidth), (0, 0, 0), -1)  # black border
        cv2.rectangle(img, (self.pixelWidth*2, self.pixelWidth*2), (self.width - self.pixelWidth*2, self.height - self.pixelWidth*2), (255, 255, 255), -1)

        cv2.rectangle(img, (self.pixelWidth * 2, self.pixelWidth * 2), (self.pixelWidth * 6, self.pixelWidth * 6), (0, 0, 0), -1)  # black corner
        cv2.rectangle(img, (self.pixelWidth*2, self.pixelWidth*2), (self.pixelWidth*5, self.pixelWidth*5), (255, 255, 255), -1)  # white corner
        #cv2.rectangle(img, (self.pixelWidth*3, self.pixelWidth*3), (self.pixelWidth * 4, self.pixelWidth * 4), (0, 0, 0), -1)  # corner dot

        dataChar = 0
        for x in range(2,columns-2):
            for y in range(2,columns-2):

                if x > 5 or y > 5:
                    if len(data) > dataChar:
                        if data[ dataChar ] == "0":
                            cv2.rectangle(img, (y*self.pixelWidth,x*self.pixelWidth), (self.pixelWidth + y*self.pixelWidth, self.pixelWidth + x*self.pixelWidth), (255,255,255), -1)
                            dataChar += 1
                        else:
                            cv2.rectangle(img, (y*self.pixelWidth,x*self.pixelWidth), (self.pixelWidth + y*self.pixelWidth, self.pixelWidth + x*self.pixelWidth), (0,0,0), -1)
                            dataChar += 1
                    else:
                        pass
                        #cv2.rectangle(img, (y * pixelWidth, x * pixelWidth),(pixelWidth + y * pixelWidth, pixelWidth + x * pixelWidth), (255, 0, 0), -1)
        return img

    def resizeQr(self, img, width):
        img = cv2.resize(img, (width,width), interpolation=cv2.INTER_AREA)
        return img

    def saveImage(self, img, name = "generatedQr.jpg"):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(name, img)

    def main(self, text):

        codedText = self.codeText(text)
        qr = self.fillImageWithData(codedText)
        qr = self.resizeQr(qr, 500)
        return qr


if __name__ == "__main__":
    generateQr = GenerateQr(50)
    txt = "rias gremory"
    qr = generateQr.main(txt)
    """
    generateQr = GenerateQr(50)
    texts = ["masinou", "prosperujici", "vyzkumne", "pozitivnich", "podporovany", "informacnimi", "nepodminkovany", "potrebujeme nove vybaveni pro kancelar", "dneska se ucastnime konference", "nase firma se rozviji velmi rychle", "potrebujeme nove zamestnance", "vcera jsme se vratili z dovolene v Karibiku", "predstaveni noveho produktu se bude konat zitra vecer", "v nedeli rano se budeme venovat uklidu v parku", "nase skupina se bude zucastnovat mezinarodni vystavy v Nemecku", "na vylet do hor se chystame uz tento vikend", "nase spolecnost se specializuje na vyvoj aplikaci pro mobilni telefony", "dneska poobede se budeme schazet na porade o novych projektech", "v sobotu vecer se chystame na koncert oblibene kapely", "nase nove kancelarove prostory se nachazeji v centru mesta", "v patek odpoledne budeme mit prezentaci noveho projektu pred klienty", "v pristim mesici se budeme soustredit na rozsireni nasich sluzeb do dalsich statu", "v nasi firmi pracuji lidi z různých koutů světa", "v pondeli ráno se budeme věnovat schvalování nových smluv a dohod", "v úterý odpoledne se budeme účastnit konference o nových trendech v oboru", "naše společnost se zaměřuje na vývoj a výrobu inovativních technologií", "v pátek ráno se budeme scházet na poradě o plánování"]
    for i, text in enumerate(texts):
        codedText = generateQr.codeText(text)

    #qr = generateQr.createBlackImage()
        qr = generateQr.fillImageWithData(codedText)
        qr = generateQr.resizeQr(qr, 500)
        generateQr.saveImage(qr, "qrs/" + str(i) + ".jpg")
    print(codedText)

    """
    #qr = cv2.flip(qr, -1)
    #qr = cv2.flip(qr, 1)
    #qr = cv2.rotate(qr, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #qr = cv2.flip(qr, 0)
    cv2.imshow("qr code - black", qr)

    cv2.waitKey(0)
    cv2.destroyAllWindows()