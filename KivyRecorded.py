from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
import cv2
import threading
from PIL import Image as PILIMAGE

file_name = "image.jpg"
framespeed = 1/10


# Definition of kivy App instance
class DisplayWindow(App):
    thing = False

    # Defining window contents
    def build(self):
        # Layout of window to contain image and label attributes
        self.layout = BoxLayout(orientation="vertical")
        self.title_text = Label(text="Title", size_hint=(1, .1))
        self.image = Image(source="blank.jpg", size_hint=(1, .7))
        self.output = Label(text="one", size_hint=(1, .1))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.videoCallback, framespeed)
        Clock.schedule_interval(self.labelCallback, 1)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.output)
        return self.layout

    # Reloads image from the disk with specified refresh rate
    def videoCallback(self, dt):
        self.image.source = "image.jpg"
        try:
            PILIMAGE.open("image.jpg").verify()
            self.image.reload()
        except Exception:
            self.image.source = self.image.source

    # Refreshes label at specified time interval, checking for change in detection boolean
    def labelCallback(self, dt):
        if(self.thing):
            self.output.text = "one"
        else:
            self.output.text = "two"


def userInterface():
    DisplayWindow().run()


if __name__ == "__main__":

    t1 = threading.Thread(target=userInterface)
    t1.start()

    frame_counter = 0
    cap = cv2.VideoCapture('images/boxing.mp4')

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        cv2.imwrite(file_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            isQuit = True
            break

    t1.join()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print("done")
