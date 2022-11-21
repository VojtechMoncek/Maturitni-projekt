class generateQrCode():
    def __init__(self, data):
        self.data = data
    def showData(self):
        for line in data:
            print(line)

    def getFormatData(self):
        pass
    def splitDataToBites(self):
        pass


if __name__ == "__main__":
    data = [
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [1, 0, 1, 1],
        [1, 1, 1, 0]
    ]
    generateQrCode(data).showData()
