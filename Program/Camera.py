from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import webbrowser
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        #cv2.imshow("a", camera.texture.pixels)
        #print(camera.texture.pixels)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestCamera(App):

    def loadVideo(self, *args):
        camera = self.camera.ids["camera"]
        pixels = self.camera.ids["camera"].texture.pixels
        img = np.frombuffer(pixels, np.uint8)

        height, width = camera.texture.height, camera.texture.width

        img = np.frombuffer(camera.texture.pixels, np.uint8)
        img = img.reshape(height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        for qr in decode(img):
            print(qr.data.decode("utf-8"))
            webbrowser.open(qr.data.decode("utf-8"))
        #cv2.imshow("a",img)
        #cv2.waitKey(0)

    def build(self):
        self.camera = CameraClick()
        Clock.schedule_interval(self.loadVideo, 1.0 / 60.0)
        return self.camera



TestCamera().run()