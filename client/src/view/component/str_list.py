from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty
)
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('src/view/component/str_list.kv')

class StrRow(BoxLayout):

    index = NumericProperty(0)
    text = StringProperty("")
    del_icon = ObjectProperty(None)
    delete = ObjectProperty(lambda *args: None)


class StrList(BoxLayout):

    strs = ListProperty([])
    hint_text = StringProperty("")
    add_icon = ObjectProperty(None)
    del_icon = ObjectProperty(None)
    add = ObjectProperty(lambda *args: None)
    delete = ObjectProperty(lambda *args: None)

    def on_strs(self, _, val):
        layout = self.ids['str_list']
        layout.clear_widgets()
        for i, s in enumerate(val):
            row = StrRow(
                index=i,
                text=s,
                del_icon=self.del_icon,
                delete=self.handle_del
            )
            layout.add_widget(row)
    
    def handle_add(self, t: str):
        self.strs = sorted(self.strs + [t])
        self.add(t)
        self.ids['text_input'].text = ''

    def handle_del(self, i: int):
        d = self.strs[i]
        self.strs = self.strs[:i] + self.strs[i+1:]
        self.delete(d)
    
    
