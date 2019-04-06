from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class KivyButton(App):
    def disable(self, instance, *args):
        instance.disabled = True

    def update(self, instance, *args):
        instance.text = "I am disabled!"

    def build(self):
        mybtn = Button(text="click me to disable!", background_color=(1, 0, 1, 1), pos=(300, 350), size_hint=(0.25, 0.18))
        mybtn.bind(on_press=partial(self.disable, mybtn))
        mybtn.bind(on_press=partial(self.update, mybtn))
        return mybtn


KivyButton().run()
