import kivy
from kivy.app import App
from kivy.uix.label import Label
import cv2
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore

# Replace this with your
# current version
kivy.require('1.11.1')


# Defining a class
class MyFirstKivyApp(App):

    # Function that returns
    # the root widget
    def build(self):
        savedData = JsonStore("data.json")
        try:
            print(f"name is {savedData.get('data')['name']}")
        except:
            pass
        #savedData.put("data", name="ahoj")
        cameraObject = Camera()
        layout = BoxLayout()
        layout.add_widget(cameraObject)
        return layout
        #while True:
            # rozpeti_1 = cv2.getTrackbarPos("rozpeti 1", "trackBars")
            # rozpeti_2 = cv2.getTrackbarPos("rozpeti 2", "trackBars")


        # Label with text Hello World is
        # returned as root widget


    # Here our class is initialized


# and its run() method is called.
# This initializes and starts
# our Kivy application.
MyFirstKivyApp().run()