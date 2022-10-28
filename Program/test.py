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
        #MyPopup.title = test.url



class MyPopup(Popup):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(MyPopup, self).__init__(**kwargs)
        self.url = ""
    def open_website(self, instance):

        webbrowser.open(self.url)

class test(App):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(test, self).__init__(**kwargs)
        self.url = ""
    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.9, 1) #background
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.loadVideo, 1.0 / 60.0)
        return MainPage()
    def loadVideo(self, *args):
        succes, frame = self.capture.read()
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")

        if not isinstance(App.get_running_app().root_window.children[0], Popup):
            for qr in decode(frame):
                print(qr.data.decode("utf-8"))
                self.url = qr.data.decode("utf-8")

                MP = MyPopup()
                MP.open()
                MP.title = qr.data.decode("utf-8")
                MP.url = qr.data.decode("utf-8")
                print(MyPopup().title)
                break

        self.root.ids.image.texture = texture
if __name__ == "__main__":
    test().run()