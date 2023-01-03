import os
import cv2
file = os.listdir("negativeJpg/")
print(file)
for i, filename in enumerate(file):

    try:
        img = cv2.imread(f"negativeJpg/{filename}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f"negativeGrayJpg/{str(i)}.jpg", img)
    except:
        print(i)
