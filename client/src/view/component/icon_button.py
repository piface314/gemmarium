from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ColorProperty

Builder.load_file('src/view/component/icon_button.kv')


class IconButton(Button):

    icon = ObjectProperty(None)
    icon_color = ColorProperty((1, 1, 1, 1))