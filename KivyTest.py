from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image


class thiccBoi(App):
    thing = False
    def build(self):
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.image = Image(source="1.jpg")
        self.mylabel = Label(text="one")
        Clock.schedule_interval(self.Clock_Callback, 1/60)
        Clock.schedule_interval(self.Clock_Callback2, 1)
        self.box.add_widget(self.image)
        self.box.add_widget(self.mylabel)
        return self.box
    def Clock_Callback(self, dt):
        # Change to image.reload() in final
        if(self.thing):
            self.image.source = "1.jpg"
            self.thing = False
        else:
            self.image.source = "2.jpg"
            self.thing = True
    def Clock_Callback2(self, dt):
        if(self.thing):
            self.mylabel.text = "one"
        else:
            self.mylabel.text = "two"


thiccBoi().run()
