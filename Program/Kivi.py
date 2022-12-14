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
from kivy.uix.camera import Camera
#Builder.load_file("main.kv")
Builder.load_string('''
#:import Factory kivy.factory.Factory
<MyPopup@Popup>
    id: popik
    auto_dismiss: True
    title: ""

    size_hint: 0.6, 0.2
    pos_hit: {"x":0.5, "top": 0.5}
    Button:
        size_hint: 0.4, 1
        text: "Vyhledat na internetu"
        font_size: 24
        on_release: root.open_website(self)


<MainPage>

    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height
        Camera:
            id: camera
            play: True

''')
url = ""
class MainPage(Widget):
    def checkbox_click(self,instance, value, text):
        if value == True:
            Window.clearcolor = (0.9, 0.9, 0.9, 1)
            self.ids.labela.text = text
        else:
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
            self.ids.labela.text = "False"
        print(value)
    def openPopup(self,instance):
        Factory.MyPopup().open()
        #MyPopup.title = main.url



class MyPopup(Popup):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(MyPopup, self).__init__(**kwargs)
        self.url = ""
    def open_website(self, instance):

        webbrowser.open(self.url)

class main(App):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(main, self).__init__(**kwargs)
        self.url = ""
    def build(self):
        self.mainPage = MainPage()
        Window.clearcolor = (0.9, 0.9, 0.9, 1) #background
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.loadVideo, 1.0 / 60.0)
        return self.mainPage
    def loadVideo(self, *args):


        camera = self.mainPage.ids["camera"]
        cameraTexture = camera.texture
        pixels = cameraTexture.pixels

        cameraTexture.flip_horizontal()
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
    main().run()