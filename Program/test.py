
from datetime import datetime

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)
with open("MainApp/history.csv", "a") as f:
    f.write(f"qrcodeData1; {dt_string}\n")
with open("MainApp/history.csv", "a") as f:
    f.write(f"qrcodeData1; datetime\n")