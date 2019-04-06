from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import cv2
import threading

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
        self.output = Label(text="one", size_hint=(1, .1))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.labelCallback, 1)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.output)
        return self.layout

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

    t1.join()
