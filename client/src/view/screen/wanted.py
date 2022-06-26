from ctrl.collection import CollectionCtrl
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('src/view/screen/wanted.kv')


class WantedScreen(Screen):

    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        back, icon = app.get_back_button()
        def cb(*args):
            self.save()
            back()
        bar = self.ids['header']
        bar.lt_btn = [(cb, icon)]
        str_list = self.ids['str_list']
        str_list.del_icon = app.get_texture('buttons-reject')
        str_list.add_icon = app.get_texture('buttons-add')
        ctrl: CollectionCtrl = app.collection_ctrl
        str_list.strs = ctrl.list_wanted()
    
    def save(self):
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        ctrl.sync_gallery()
    
    def handle_add(self, gem: str):
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        ctrl.add_wanted(gem)
    
    def handle_del(self, gem: str):
        app = App.get_running_app()
        ctrl: CollectionCtrl = app.collection_ctrl
        ctrl.remove_wanted(gem)
