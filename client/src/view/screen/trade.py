from ctrl.trade import TradeCtrl, TradeEvent
from model.trade import Trade
from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('src/view/screen/trade.kv')


class TradeScreen(Screen):

    trade_copy = ObjectProperty(Trade.empty())

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
        bar.rt_btn = [
            (self.handle_fusion, app.get_texture('buttons-fusion')),
            (self.handle_reject, app.get_texture('buttons-reject')),
            (self.handle_accept, app.get_texture('buttons-accept')),
            (self.handle_update, app.get_texture('buttons-trade'))
        ]
        sw = self.ids['self_wanted']
        sw.add_icon = app.get_texture('buttons-add')
        sw.del_icon = app.get_texture('buttons-reject')
        so = self.ids['self_offered']
        so.check_icon = app.get_texture('buttons-accept')
        ctrl: TradeCtrl = app.trade_ctrl
        self.binds = {}
        self.binds[TradeEvent.UPDATE] = ctrl.bind(TradeEvent.UPDATE, self.receive_update)
        self.binds[TradeEvent.ACCEPT] = ctrl.bind(TradeEvent.ACCEPT, self.receive_update)
        self.binds[TradeEvent.REJECT] = ctrl.bind(TradeEvent.REJECT, self.receive_finish)
        self.binds[TradeEvent.FUSION] = ctrl.bind(TradeEvent.FUSION, self.receive_update)
        self.binds[TradeEvent.FINISH] = ctrl.bind(TradeEvent.FINISH, self.receive_finish)
    
    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        self.trade_copy = ctrl.get_trade(app.current_peer)

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        app = App.get_running_app()
        app.current_peer = None
        ctrl: TradeCtrl = app.trade_ctrl
        for ev, i in self.binds.items():
            ctrl.unbind(ev, i)

    def on_trade_copy(self, _, trade: Trade):
        print(trade)

    def handle_update(self, *args):
        pass

    def handle_accept(self, *args):
        pass

    def handle_reject(self, *args):
        pass
    
    def handle_fusion(self, *args):
        pass

    def receive_update(self, trade: Trade):
        self.trade_copy = trade.copy()

    def receive_finish(self, *args):
        app = App.get_running_app()
        app.current_trade = None
        app.back_to_menu()