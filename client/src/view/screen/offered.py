from ctrl.collection import CollectionCtrl
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from model.gem import Gem
from view.component.sprite import Sprite, gem_rects

Builder.load_file('src/view/screen/offered.kv')


class OfferedScreen(Screen):

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = App.get_running_app()
        back, icon = app.get_back_button()
        def cb(*args):
            self.save()
            back()
        bar = self.ids['header']
        bar.lt_btn = [(cb, icon)]
    
    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        toggle_list = self.ids['toggle_list']
        toggle_list.check_icon = app.get_texture('buttons-accept')
        toggle_list.objs = [
            (gem, gem.is_public, self.gem_icon(gem), self.gem_label(gem))
            for gem in ctrl.list_gems()
        ]

    def gem_icon(self, gem: Gem):
        gem_sp = Sprite.from_bytes(
            gem.sprite,
            gem_rects,
            f'{gem.id}.png'
        )
        gem_sp.animate = False
        gem_sp.allow_stretch = True
        return gem_sp

    def gem_label(self, gem: Gem):
        at = gem.obtained_at.strftime("%Y/%m/%d")
        metadata = f'{at} @{gem.created_for}'
        return f'{gem.name}\n[size=12][color=cccccc]{metadata}[/color][/size]'

    def save(self):
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        ctrl.sync_gallery()
    
    def handle_toggle(self, gem, val, *args):
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        ctrl.set_visibility(gem, val)