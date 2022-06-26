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
    check_icon = ObjectProperty(None)
    value = BooleanProperty(False)
    toggle = ObjectProperty(lambda *args: None)

class ToggleList(BoxLayout):

    objs = ListProperty([])
    check_icon = ObjectProperty(None)
    handle_toggle = ObjectProperty(lambda *args: None)

    def on_objs(self, _, val):
        layout = self.ids['toggle_list']
        layout.clear_widgets()
        for i, (obj, val, icon, text) in enumerate(val):
            row = ToggleRow(
                index=i,
                text=text,
                check_icon=self.check_icon,
                value=val,
                toggle=lambda v, obj=obj: self.handle_toggle(obj, v)
            )
            icon.size_hint = (None, None)
            icon.size = (48, 48)
            icon.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            row.add_widget(icon, 2)
            layout.add_widget(row)