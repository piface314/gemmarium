from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty
)

Builder.load_file('src/view/component/bar.kv')


class Bar(Widget):

    lt_btn = ListProperty([])
    rt_btn = ListProperty([])
    title = StringProperty("")
    bgcolor = ColorProperty()
    padding = NumericProperty(6)

    def on_lt_btn(self, _, buttons):
        layout = self.ids['lt_stack']
        self.add_buttons(layout, buttons)

    def on_rt_btn(self, _, buttons):
        layout = self.ids['rt_stack']
        self.add_buttons(layout, buttons)

    def add_buttons(self, layout, buttons):
        layout.clear_widgets()
        for cb, tx in buttons:
            btn = Factory.IconButton()
            if cb:
                btn.bind(on_release=cb)
            btn.tx = tx
            btn.pad = self.padding
            layout.add_widget(btn)
            
    
