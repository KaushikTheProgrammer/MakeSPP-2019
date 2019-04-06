from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image


# Definition of kivy App instance
class DisplayWindow(App):
    thing = False

    # Defining window contents
    def build(self):
        # Box to contain image and label attributes
        self.layout = FloatLayout(size=(300, 300))
        self.title_text = Label(text="Title", size_hint=(1, .1), pos=(20, 20))
        self.image = Image(source="1.jpg", size_hint=(.2, .2), pos=(20, 20))
        self.output = Label(text="one", size_hint=(.2, .2), pos=(20, 20))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.videoCallback, 1/60)
        Clock.schedule_interval(self.labelCallback, 1)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.output)
        return self.layout

    # Reloads image from the disk with specified refresh rate
    def videoCallback(self, dt):
        # Change to image.reload() in final
        if(self.thing):
            self.image.source = "1.jpg"
            self.thing = False
        else:
            self.image.source = "2.jpg"
            self.thing = True

    # Refreshes label at specified time interval, checking for change in detection boolean
    def labelCallback(self, dt):
        if(self.thing):
            self.output.text = "one"
        else:
            self.output.text = "two"


# Running kivy app
DisplayWindow().run()
