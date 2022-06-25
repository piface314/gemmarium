from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
import threading

Builder.load_file('src/view/screen/menu.kv')


class MenuScreen(Screen):

    logo = ObjectProperty(None)
    username = StringProperty("")

    def on_logo(self, _, logo):
        box_layout = self.ids['box_layout']
        logo.animate = True
        logo.size_hint = (1, 1)
        logo.allow_stretch = True
        box_layout.add_widget(logo, len(box_layout.children))
        
