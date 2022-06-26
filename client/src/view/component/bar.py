from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    StringProperty
)
from view.component.icon_button import IconButton

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
        h = self.size[1]
        pad = self.padding
        layout.clear_widgets()
        for cb, tx in buttons:
            btn = IconButton(icon=tx, padding=(pad, pad))
            btn.size_hint = (None, None)
            btn.size = (h-pad*2, h-pad*2)
            if cb:
                btn.bind(on_release=cb)
            layout.add_widget(btn)
            
    
