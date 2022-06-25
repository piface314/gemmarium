from ctrl.collection import CollectionCtrl
from kivy.app import App
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from model.gem import Gem
from view.component.sprite import Sprite, gem_rects
import threading

Builder.load_file('src/view/screen/collection.kv')


class GemHolder(ButtonBehavior, RelativeLayout):
    pass


class CollectionScreen(Screen):

    gems = ListProperty([])

    def on_enter(self, *args):
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
        bar.rt_btn = [
            (self.goto_wanted, app.button_icons['edit_wanted']),
            (self.goto_offered, app.button_icons['edit_offered']),
        ]
        worker = threading.Thread(target=(self.load_gems))
        worker.start()

    def load_gems(self):
        app = App.get_running_app()
        self.ctrl: CollectionCtrl = app.collection_ctrl
        self.gems = self.ctrl.list_gems()

    def goto_offered(self, *args):
        print("goto_offered")

    def goto_wanted(self, *args):
        print("goto_wanted")

    def goto_gem(self, gem: Gem):
        popup = Factory.GemShow()
        popup.title = gem.name
        popup.text = gem.desc
        gem_sp = Sprite.from_bytes(
            gem.sprite,
            gem_rects,
            f'{gem.id}.png'
        )
        gem_sp.animate = True
        gem_sp.allow_stretch = True
        gem_sp.size_hint = (0.5, 0.5)
        gem_sp.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        holder = GemHolder()
        holder.add_widget(gem_sp)
        layout = popup.ids['layout']
        layout.add_widget(holder, 2)
        popup.open()

    @mainthread
    def on_gems(self, _, gems: list[Gem]):
        layout = self.ids['gem_list']
        layout.clear_widgets()
        for gem in gems:
            gem_sp = Sprite.from_bytes(
                gem.sprite,
                gem_rects,
                f'{gem.id}.png'
            )
            gem_sp.animate = True
            gem_sp.allow_stretch = True
            gem_sp.size_hint = (0.5, 0.5)
            gem_sp.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            holder = GemHolder()
            holder.add_widget(gem_sp)
            holder.bind(on_release=lambda *_, g=gem: self.goto_gem(g))
            layout.add_widget(holder)
