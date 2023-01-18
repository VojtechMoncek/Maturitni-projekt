#raws: 13, data: /fpjacb xhxhcbdj ipc
import json
import time
import webbrowser
from datetime import datetime
import qrcode

from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivy.core.image import Image as CoreImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivy.config import Config

from io import BytesIO
import numpy as np
import cv2


import generateQr
import ReadQr
from android.permissions import request_permissions, Permission
import os

os.environ["KIVY_ORIENTATION"] = "Portrait"
Config.set('graphics', 'rotation', 0)
Window.rotation = 0

class GeneratePage(Screen):
    pass
class InfoPage(Screen):
    pass
class SettingsPage(Screen):
    pass
class MainPage(Screen):
    pass


class newGeneratePage(Screen):
    pass
class NewPage(Screen):
    pass
class Main(MDApp):
    def __init__(self, **kwargs):
        # DOnt overwrite anything
        super(Main, self).__init__(**kwargs)
        self.popups = []
        self.sm = ScreenManager(transition=NoTransition())
        self.settings = self.getSettings()
        self.url = ""

    def updateSettings(self):
        """
        update settings and check if values are possible to set
        :return:
        """
        #Frame rate
        #frameRate = self.page.ids["FrameRate"].text
        standardReading = self.page.ids["StandardReading"].active
        print(standardReading)

        #Which reading use
        self.settings["StandardReading"] = standardReading
        self.changeTexture()

        """
        #FrameRate
        if self.page.ids["FrameRate"].text.isdigit() and int(frameRate) <= 99:
            self.settings["FrameRate"] = frameRate
        else:
            self.page.ids["FrameRate"].text = self.settings["FrameRate"]
        """

        self.saveSettings(self.settings)
    def getSettings(self):
        """
        return json data in dic
        :return:
        """
        with open("settings.json", "r") as f:
            data = f.read()
        return json.loads(data)
    def saveSettings(self, settings):
        """
        setting fc
        :param settings:
        :return:
        """
        with open("settings.json", "w") as f:
            f.write(json.dumps(self.settings))


    def openPopup(self, actionType = "website", value = ""):
        """
        create and open popup
        :param value: Text on popup
        :return:
        """


        #self.page.ids["generatedQr"].texture.save("qr.png")
        if isinstance(MDApp.get_running_app().root_window.children[0], MDDialog): return

        if actionType == "website":
            if value == "": return
            print("# website")
            self.popup = MDDialog(
                title="obsah:",
                text=value,
                buttons=[
                    MDFlatButton(
                        text="Zavřít",
                        on_release=self.closePopup,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="Najít na internetu",
                        on_release=self.openWebsite,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    )
                ]


            )

        elif actionType == "saveQr":
            self.popup = MDDialog(
                title="Uložit Qr kód?",
                text=value,
                buttons=[
                    MDFlatButton(
                        text="Neukládat",
                        on_release=self.closePopup,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="Uložit",
                        on_release=self.saveQrImage,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    )
                ]

            )
        dt_string = datetime.now().strftime("%d.%m. %Y %H:%M")
        # print("date and time =", dt_string)
        with open("history.csv", "a", encoding="UTF-8") as f:
            f.write(f"{value};{dt_string}\n")
        self.createHistoryContent(self.page.ids["history_content"])
        self.url = value
        self.popup.open()
        print(f"popup otevren   data: {value}")

        #webbrowser.open(value)
    def closePopup(self, *obj):
        """
        close popup
        :param obj:
        :return:
        """
        self.popup.dismiss()
    def openWebsite(self,obj):
        """
        open website
        :param obj:
        :return:
        """
        print(self.url)
        webbrowser.open(self.url)


    def findQr(self, img):
        """
        Find qr code from image
        :param img: Image with qr
        :return:
        """
        self.i += 1
        if self.settings["StandardReading"] == True:
            _qr = cv2.flip(img, -1)
            _qr = cv2.flip(_qr, 1)
            detect = cv2.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(_qr)
            self.openPopup("website", value)
        else:

            img = cv2.resize(img, (round(img.shape[1] * 500 / img.shape[1]), round(img.shape[0] * 500 / img.shape[1])), interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            qrReader = ReadQr.QrReader(img)
            text = qrReader.main(img)

            if text is not None and len(text) >1:
                text = text.rstrip()
                if text[0] == "u" and text[-1] == "u":
                    print(text)
                    self.openPopup("website", text[1:-1])
        if self.i % 30 == 0:
            print(f"Total time: {time.time() - self.startTime}")
            self.startTime = time.time()


    def getFrame(self, *args):
        """
        Get frame from camera
        :param args:
        :return:
        """
        #cam = self.sm.get_screen("main").ids["camera"]
        cam = self.page.ids["camera"]

        cameraTexture = cam.texture
        pixels = cameraTexture.pixels

        # cameraTexture.flip_horizontal()
        #img = np.frombuffer(pixels, np.uint8)

        height, width = cam.texture.height, cam.texture.width

        img = np.frombuffer(cam.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        #img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        self.findQr(img)

    def changePage(self, name):
        """
        Turning off and on camera
        :param name: Name of new page
        :return:
        """
        self.sm.current = name

        if self.sm.current == "main":
            self.sm.get_screen(name).ids["camera"].play = False



        if self.sm.current == "main":
            self.sm.get_screen(name).ids["camera"].play = True



    def build(self):

        request_permissions([Permission.CAMERA])
        self.page = NewPage()
        #self.sm.add_widget(GeneratePage(name='newGenerate'))
        self.sm.add_widget(GeneratePage(name='generate'))
        self.sm.add_widget(InfoPage(name='info'))
        self.sm.add_widget(MainPage(name='main'))
        self.sm.add_widget(SettingsPage(name='settings'))


        #Window.size = (432, 768)
        self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Indigo"

        self.GeneratePage = GeneratePage()
        self.changeTexture()
        self.sm.current = "main"
        #print(self.settings["FrameRate"])
        self.startTime = time.time()
        self.i = 0
        Clock.schedule_interval(self.getFrame, 1.0 / 24)

        print(self.page.ids)

        self.createHistoryContent(self.page.ids["history_content"])
        return self.page

    def createHistoryContent(self, container):
        """
        Write history to GUI from csv
        :param container: Id of container in GUI
        :return:
        """
        lines = self.historyReturn()

        print(len(container.children))

        while container.children:
            container.remove_widget(container.children[0])
        print(len(container.children))
        #data = ""
        dList = []
        for i, line in enumerate( reversed(lines) ):

            date = line.split(";")[1]
            data = line.split(";")[0]
            dList.append((date, data))
            print("data: " + data)
            def openPopup(_data):
                print(_data)
                self.openPopup("website", str(_data))
            #opup = partial(openPopup)

            container.add_widget(
                MDBoxLayout(

                    MDBoxLayout(

                        TwoLineListItem(
                            id=f"popup_{i}",
                            divider=None,
                            text=date,
                            secondary_text=dList[i][1],
                            #on_release= lambda x: openPopup(data)
                        ),
                        adaptive_height=True,
                    ),

                    adaptive_height=True,
                ),
            )
        print("deti")
        print(self.page.ids["history_content"])
    def historyReturn(self):
        """
        Getting history from csv file
        :return: All lines from csv
        """
        with open("history.csv", "r", encoding="utf-8") as f:
            try:
                lines = f.readlines()
                print(lines)
            except:
                lines=["Historie se nepovedla načíst;"]
            return lines


    def changeTexture(self):
        """
        Creating Qr code
        :return:
        """
        text = self.page.ids["input"].text
        if text == "": text = "rias gremory"

        if self.settings["StandardReading"] == True:
            imgQR = qrcode.make(text)
            img = self.page.ids["generatedQr"]
            img.texture = imgQR

            data = BytesIO()
            imgQR.save(data, format='png')
            data.seek(0)  # yes you actually need this
            newImg = CoreImage(BytesIO(data.read()), ext='png')
            self.page.ids["generatedQr"].texture = newImg.texture
            print(newImg.texture)
        else:
            gQr = generateQr.GenerateQr(50)
            imgQR = gQr.main(text)
            cv2.cvtColor(imgQR, cv2.COLOR_BGR2RGB)
            imgQR = cv2.flip(imgQR, 0)

            npQr = np.array(imgQR)

            texture = Texture.create(size=(imgQR.shape[1], imgQR.shape[0]), colorfmt='rgb')
            texture.blit_buffer(npQr.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            img = self.page.ids["generatedQr"]
            img.texture = texture


            self.page.ids["generatedQr"].texture = img.texture

    def saveQrImage(self, obj):
        print("saving QR")
        self.page.ids["generatedQr"].texture.save("qr.png")
        self.closePopup()
        #self.openPopup("saveQr")



Main().run()