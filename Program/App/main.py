import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
import webbrowser
from pyzbar.pyzbar import decode
import numpy as np
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.camera import Camera
#Builder.load_file("main.kv")

class MainPage(Screen):
    def openPopup(self,instance):
        Factory.MyPopup().open()
        #MyPopup.title = main.url


class SettingsPage(Screen):
    pass
class MyPopup(Popup):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(MyPopup, self).__init__(**kwargs)
        self.url = ""
    def open_website(self, instance):

        webbrowser.open(self.url)
class ScreenManager(ScreenManager):
    pass
class Main(App):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Main, self).__init__(**kwargs)
        self.url = ""
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(MainPage(name='main'))
        self.sm.add_widget(SettingsPage(name='settings'))




        # self.mainPage = MainPage()
        Window.clearcolor = (0.9, 0.9, 0.9, 1) #background
        # self.capture = cv2.VideoCapture(0)
        #Clock.schedule_interval(self.loadVideo, 1.0 / 24.0)

        return self.sm
    def loadVideo(self, *args):


        camera = self.sm.get_screen("main").ids["camera"]
        cameraTexture = camera.texture
        pixels = cameraTexture.pixels

        #cameraTexture.flip_horizontal()
        img = np.frombuffer(pixels, np.uint8)

        height, width = camera.texture.height, camera.texture.width

        img = np.frombuffer(camera.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

        if not isinstance(App.get_running_app().root_window.children[0], Popup):
            for qr in decode(img):
                print(qr.data.decode())
                self.url = qr.data.decode("utf-8")

                MP = MyPopup()
                MP.open()
                MP.title = qr.data.decode("utf-8")
                MP.url = qr.data.decode("utf-8")
                print(MyPopup().title)
                break
if __name__ == "__main__":
    Main().run()