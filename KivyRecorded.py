from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from sightengine.client import SightengineClient
from skimage import io
import cv2
import threading
import io
import os
from PIL import Image as PILIMAGE

file_name = "image.jpg"
framespeed = 1/10
client = SightengineClient('185769829', 'b8CCfNrKrYnWYwsUeBbK')
frame_counter = 0
cap = cv2.VideoCapture('images/storerobbery.mp4')

# Definition of kivy App instance
class DisplayWindow(App):
    violenceFlag = False
    # Defining window contents
    def build(self):
        # Layout of window to contain image and label attributes
        self.layout = BoxLayout(orientation="vertical")
        self.title_text = Label(text="Title", size_hint=(1, .1))
        self.image = Image(source=file_name, size_hint=(1, .7))
        self.output = Label(text="one", size_hint=(1, .1))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.labelCallback, 1)
        Clock.schedule_interval(self.videoCallback, framespeed)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.output)
        return self.layout

    # Reloads image from the disk with specified refresh rate
    def videoCallback(self, dt):
        # Capture frame-by-frame
        global cap
        ret, frame = cap.read()
        global frame_counter
        frame_counter += 1

        cv2.imwrite(file_name, frame)
        cv2.imwrite('images/live.jpg', frame)
        self.image.reload()
    
    # Refreshes label at specified time interval, checking for change in detection boolean
    def labelCallback(self, dt):
        if(self.violenceFlag):
            self.output.text = "Violence has been detected."
        else:
            self.output.text = "two"

def analyzeFrame():
    while True:
        global frame_counter
        if frame_counter == 5:
            output = client.check('wad').set_file('images/live.jpg')
            print(output)
            frame_counter = 0

if __name__ == "__main__":

    t2 = threading.Thread(target = analyzeFrame)
    t2.start()

    DisplayWindow().run()

    t2.join()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print("done")
