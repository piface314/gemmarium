from ctrl.trade import TradeCtrl, TradeEvent
from kivy.app import App
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from model.gem import Gem
from view.component.holder import GemHolder
import threading

Builder.load_file('src/view/screen/menu.kv')


class MenuScreen(Screen):
    
    username = StringProperty("")
    unseen = NumericProperty(0)

    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        self.username = app.profile_ctrl.get_username()
        self.events = [TradeEvent.UPDATE, TradeEvent.ACCEPT, TradeEvent.FUSION, TradeEvent.CLOSE]
        self.bindings = [ctrl.bind(ev, self.update_unseen) for ev in self.events]
        self.update_unseen()

    def on_leave(self, *args):
        super().on_leave(*args)
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        for ev, i in zip(self.events, self.bindings):
            ctrl.unbind(ev, i)
    
    @mainthread
    def update_unseen(self, **args):
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        self.unseen = ctrl.count_unseen()
        
