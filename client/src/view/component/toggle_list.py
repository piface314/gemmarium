from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
    BooleanProperty
)
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('src/view/component/toggle_list.kv')

class ToggleRow(BoxLayout):

    index = NumericProperty(0)
    text = StringProperty("")
    icon_size = NumericProperty(32)
    check_icon = ObjectProperty(None)
    value = BooleanProperty(False)
    toggle = ObjectProperty(lambda *args: None)

class ToggleList(BoxLayout):

    objs = ListProperty([])
    check_icon = ObjectProperty(None)
    handle_toggle = ObjectProperty(lambda *args: None)
    icon_size = NumericProperty(48)

    def on_objs(self, _, val):
        layout = self.ids['toggle_list']
        layout.clear_widgets()
        for i, (obj, val, icon, text) in enumerate(val):
            row = ToggleRow(
                index=i,
                text=text,
                icon_size=self.icon_size * 1.2,
                check_icon=self.check_icon,
                value=val,
                toggle=lambda v, obj=obj, i=i: self.handle_toggle(obj, v, i)
            )
            icon.size_hint = (None, 1)
            icon.size = (self.icon_size, self.icon_size)
            icon.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            row.add_widget(icon, 2)
            layout.add_widget(row)