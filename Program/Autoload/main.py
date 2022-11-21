import webbrowser
from datetime import datetime

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

import numpy as np
import cv2
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem


class GeneratePage(Screen):
    pass
class InfoPage(Screen):
    pass
class SettingsPage(Screen):
    pass
class MainPage(Screen):
    pass
class MySpeedDial(MDFloatingActionButtonSpeedDial):
    pass


class newGeneratePage(Screen):
    pass
class NewPage(Screen):
    pass
class Main(MDApp):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Main, self).__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())

        #print( self.page.ids.tab_manager.current )
        #print(self.page.ids.bottom_panel.current)
        #print(self.page.ids.tab_bar.current)
        self.url = ""

    def openPopup(self, value):

        if not isinstance(MDApp.get_running_app().root_window.children[0], MDDialog):
            if value != "":
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
        self.popup.dismiss()
    def openWebsite(self, obj):
        webbrowser.open(self.url)
    def findQr(self, img):
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        self.openPopup(value)
    def getFrame(self, *args):
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
        self.sm.current = name

        if self.sm.current == "main":
            self.sm.get_screen(name).ids["camera"].play = False

        self.sm.get_screen(name).ids["speedDial"].close_stack()

        if self.sm.current == "main":
            self.sm.get_screen(name).ids["camera"].play = True
    def historyReturn(self):
        with open("history.csv", "r") as f:
            lines = f.readlines()
            return lines

    def speedDialReturnData(self):
        data = {
            ' ': ['information', "on_press",lambda x: self.changePage("info")],
            '  ': ['cog', "on_press",lambda x: self.changePage("settings")],
            '   ': ['qrcode', "on_press",lambda x: self.changePage("newGenerate")],
            '    ': ['camera', "on_press",lambda x: self.changePage("main")],
         }
        return data

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

        Clock.schedule_interval(self.getFrame, 1.0 / 24.0)

        print(self.page.ids)

        self.createHistoryContent(self.page.ids["history_content"])
        return self.page
    def createHistoryContent(self, container):

        lines = self.historyReturn()
        print(len(container.children))

        # for child in container.children:
        #     container.remove_widget(child)

        while container.children:
            container.remove_widget(container.children[0])
        print(len(container.children))
        for line in lines:

            date = line.split(";")[1]
            data = line.split(";")[0]
            def openPopup(*args):
                self.openPopup(data)
            container.add_widget(
                MDBoxLayout(
                    MDBoxLayout(

                        TwoLineListItem(
                            divider =  None,
                            text = date,
                            secondary_text = data,
                            on_release = openPopup
                        ),
                        adaptive_height=True,
                    ),
                    adaptive_height=True,
                ),
            )
        print("deti")
        print(self.page.ids["history_content"].children)

    def onOpen(self):
        print("open")
    def changeTexture(self):
        imgQR = qrcode.make(self.page.ids["input"].text)
        img = self.page.ids["generatedQr"]
        #imgQR = qrcode.make(self.sm.get_screen("generate").ids["input"].text)
        #img = self.sm.get_screen("generate").ids["generatedQr"]
        img.texture = imgQR

        data = BytesIO()
        imgQR.save(data, format='png')
        data.seek(0)  # yes you actually need this
        newImg = CoreImage(BytesIO(data.read()), ext='png')
        self.page.ids["generatedQr"].texture = newImg.texture
        print(img.texture)


Main().run()