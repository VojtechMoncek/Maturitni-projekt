from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
import cv2


class MainApp(App):
    def build(self):

        self.image = Image()
        self.btn = Button(
            text="click",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None,None)
        )


        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.image)
        layout.add_widget(self.btn)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.loadVideo, 1.0/60.0)
        return layout
    def loadVideo(self,*args):
        succes, frame = self.capture.read()

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")

        self.image.texture = texture


if __name__ == "__main__":
    MainApp().run()