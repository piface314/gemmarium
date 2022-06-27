from ctrl.trade import TradeCtrl
from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('src/view/screen/trade.kv')


class TradeScreen(Screen):

    self_wanted = ListProperty([])
    self_offered = ListProperty([])
    peer_wanted = ListProperty([])
    peer_offered = ListProperty([])

    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
        bar.rt_btn = [
            (self.handle_fusion, app.get_texture('buttons-fusion')),
            (self.handle_reject, app.get_texture('buttons-reject')),
            (self.handle_accept, app.get_texture('buttons-accept'))
        ]
        sw = self.ids['self_wanted']
        sw.add_icon = app.get_texture('buttons-add')
        sw.del_icon = app.get_texture('buttons-reject')
        so = self.ids['self_offered']
        so.check_icon = app.get_texture('buttons-accept')

    def handle_accept(self, *args):
        pass

    def handle_reject(self, *args):
        pass
    
    def handle_fusion(self, *args):
        pass