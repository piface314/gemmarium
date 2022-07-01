from ctrl.trade import TradeCtrl
from model.trade import Trade
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('src/view/screen/trade_list.kv')


class TradeListScreen(Screen):

    trades = ListProperty([])

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]

    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        self.trades = []
        self.trades = ctrl.list()
    
    def on_trades(self, _, trades):
        layout = self.ids['trade_list']
        layout.labels = [(self.format_label(t), t.unseen) for t in trades]
    
    def format_label(self, trade: Trade):
        label = f'@{trade.peername}\n[size=12][color=cccccc]{trade.ip}:{trade.port}[/color][/size]'
        return f'[b]{label}[/b]' if trade.unseen else label
    
    def goto_trade(self, row):
        trade: Trade = self.trades[row.index]
        app = App.get_running_app()
        app.current_peer = trade.peerid
        self.manager.current = 'trade'