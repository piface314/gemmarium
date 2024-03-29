from kivy.lang import Builder
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
    BooleanProperty
)
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView


Builder.load_file('src/view/component/static_list.kv')

class LabelRow(ButtonBehavior, Label):

    index = NumericProperty(0)
    text = StringProperty("")
    marker = BooleanProperty(False)


class StaticList(ScrollView):

    labels = ListProperty([])
    handle = ObjectProperty(None)
    row_height = NumericProperty(48)

    def on_labels(self, _, val):
        layout = self.ids['static_list']
        layout.clear_widgets()
        for i, s in enumerate(val):
            mark = False
            if type(s) is tuple:
                s, mark = s
            row = LabelRow(index=i, text=s, marker=mark)
            if callable(self.handle):
                row.bind(on_release=self.handle)
            layout.add_widget(row)
    
    
