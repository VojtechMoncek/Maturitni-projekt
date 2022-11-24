class generateQrCode():
    def __init__(self, data):
        self.data = data
    def showData(self):
        for line in data:
            for bool in line:
                if bool:
                    print("■  ",end="")
                else:
                    [print("   ",end="")]
            print()

    def getFormatData(self):
        formatData = {
            "ec" : [self.data[8][0], self.data[8][1]],
            "ec2" : [self.data[-1][8], self.data[-2][8]],
            "mask": [self.data[8][2], self.data[8][3], self.data[8][4]],
            "mask2" : [self.data[-3][8], self.data[-4][8], self.data[-5][8]]
        }
        """
        print(self.data[0][8])
        print(self.data[1][8])
        print(self.data[2][8])
        print(self.data[3][8])
        print(self.data[4][8])
        print(self.data[5][8])
        #print(self.data[6][8])
        print("x")
        print(self.data[7][8])
        
        print("_____")
        print(self.data[8][0])
        print(self.data[8][1])
        print(self.data[8][2])
        print(self.data[8][3])
        print(self.data[8][4])
        print(self.data[8][5])
        # print(self.data[8][6])
        print("x")
        print(self.data[8][7])
        print("_____")


        print(self.data[8][-8])
        print(self.data[8][-7])
        print(self.data[8][-6])
        print(self.data[8][-5])
        print(self.data[8][-4])
        print(self.data[8][-3])
        print(self.data[8][-2])
        print(self.data[8][-1])

        print("______")

        #print(self.data[-8][8])
        print(self.data[-7][8])
        print(self.data[-6][8])
        print(self.data[-5][8])
        print(self.data[-4][8])
        print(self.data[-3][8])
        print(self.data[-2][8])
        print(self.data[-1][8])
        """
        print(formatData)

if __name__ == "__main__":
    data = [
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],


    ]
    generator = generateQrCode(data)
    generator.showData()
    generator.getFormatData()

