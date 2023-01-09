import csv
import json
import webbrowser
from datetime import datetime

from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import qrcode
from kivy.core.image import Image as CoreImage
from io import BytesIO
from kivy.uix.button import Button
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock

from functools import partial
import numpy as np
import cv2
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem

from Program.generateQr import generateQr

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

        self.sm = ScreenManager(transition=NoTransition())
        self.settings = self.getSettings()
        self.url = ""

    def updateSettings(self):
        """
        update settings and check if values are possible to set
        :return:
        """
        #Frame rate
        frameRate = self.page.ids["FrameRate"].text
        standardReading = self.page.ids["StandardReading"].active
        print(standardReading)

        #Which reading use
        self.settings["StandardReading"] = standardReading
        self.changeTexture()


        #FrameRate
        if self.page.ids["FrameRate"].text.isdigit() and int(frameRate) <= 99:
            self.settings["FrameRate"] = frameRate
        else:
            self.page.ids["FrameRate"].text = self.settings["FrameRate"]


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
                        text="Zavřít",
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
        with open("history.csv", "a") as f:
            f.write(f"{value};{dt_string}\n")
        self.createHistoryContent(self.page.ids["history_content"])
        self.url = value
        self.popup.open()
        print(f"popup otevren   data: {value}")

        #webbrowser.open(value)
    def closePopup(self, obj):
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
        if self.settings["StandardReading"] == True:
            detect = cv2.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(img)
            self.openPopup("website", value)
        else:
            pass


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
        img = np.frombuffer(pixels, np.uint8)

        height, width = cam.texture.height, cam.texture.width

        img = np.frombuffer(cam.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

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
        self.page = NewPage()
        #self.sm.add_widget(GeneratePage(name='newGenerate'))
        self.sm.add_widget(GeneratePage(name='generate'))
        self.sm.add_widget(InfoPage(name='info'))
        self.sm.add_widget(MainPage(name='main'))
        self.sm.add_widget(SettingsPage(name='settings'))


        Window.size = (432, 768)
        self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Indigo"

        self.GeneratePage = GeneratePage()
        self.changeTexture()
        self.sm.current = "main"
        print(self.settings["FrameRate"])
        Clock.schedule_interval(self.getFrame, 1.0 / int(self.settings["FrameRate"]))

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
            opup = partial(openPopup)
            container.add_widget(
                MDBoxLayout(
                    MDBoxLayout(

                        TwoLineListItem(
                            divider=None,
                            text=date,
                            secondary_text=dList[i][1],
                            on_release=opup
                        ),
                        adaptive_height=True,
                    ),
                    adaptive_height=True,
                ),
            )
        print("deti")
        print(self.page.ids["history_content"].children)
    def historyReturn(self):
        """
        Getting history from csv file
        :return: All lines from csv
        """
        with open("history.csv", "r") as f:
            lines = f.readlines()
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
            imgQR = cv2.rotate(imgQR, cv2.ROTATE_90_COUNTERCLOCKWISE)
            npQr = np.array(imgQR)

            texture = Texture.create(size=(imgQR.shape[1], imgQR.shape[0]), colorfmt='bgr')
            texture.blit_buffer(npQr.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

            img = self.page.ids["generatedQr"]
            img.texture = texture


            self.page.ids["generatedQr"].texture = img.texture

    def saveQrImage(self, obj):
        print("saving QR")
        self.openPopup("saveQr")



Main().run()