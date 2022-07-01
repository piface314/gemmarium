from ctrl.collection import CollectionCtrl
from ctrl.trade import TradeCtrl, TradeEvent
from model.gem import Gem
from model.misc import GemList
from model.trade import Trade
from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ColorProperty
from kivy.uix.screenmanager import Screen
from view.component.popup import Loading, Warning
from view.component.sprite import Sprite, gem_rects
import threading

Builder.load_file('src/view/screen/trade.kv')


class TradeScreen(Screen):

    TRANSPARENT = (1, 1, 1, 0)
    GREEN = (0, 1, 0, 0.2)
    PURPLE = (0.5, 0, 1, 0.2)

    trade_copy = ObjectProperty(Trade.empty())
    self_overlay = ColorProperty((1, 1, 1, 0))
    peer_overlay = ColorProperty((1, 1, 1, 0))

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
        self.binds[TradeEvent.REJECT] = ctrl.bind(TradeEvent.REJECT, self.receive_reject)
        self.binds[TradeEvent.FUSION] = ctrl.bind(TradeEvent.FUSION, self.receive_update)
        self.binds[TradeEvent.ERROR] = ctrl.bind(TradeEvent.ERROR, self.receive_error)
        self.binds[TradeEvent.CLOSE] = ctrl.bind(TradeEvent.CLOSE, self.receive_close)
    
    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        coll: CollectionCtrl = app.collection_ctrl
        trade = ctrl.get_trade(app.current_peer)
        trade.unseen = False
        self.trade_copy = trade.copy()
        offered = {gem.id for gem in trade.self_gems.offered }
        self.collection = [[gem.id in offered, gem] for gem in coll.list_gems()]
        so = self.ids['self_offered']
        so.objs = [(gem, offered, self.gem_icon(gem), self.gem_label(gem))
            for offered, gem in self.collection ]
        sw = self.ids['self_wanted']
        sw.strs = trade.self_gems.wanted
    
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
        metadata = f'@{gem.created_for}'
        return f'[size=10]{gem.name}\n[color=cccccc]{metadata}[/color][/size]'

    def handle_toggle(self, _, val, i):
        self.collection[i][0] = val

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        app = App.get_running_app()
        app.current_peer = None
        ctrl: TradeCtrl = app.trade_ctrl
        for ev, i in self.binds.items():
            ctrl.unbind(ev, i)

    def on_trade_copy(self, _, trade: Trade):
        self.self_overlay = self.PURPLE if trade.self_fusion else \
            self.GREEN if trade.self_accepted else self.TRANSPARENT
        self.peer_overlay = self.PURPLE if trade.peer_fusion else \
            self.GREEN if trade.peer_accepted else self.TRANSPARENT
        disabled = trade.self_fusion or trade.self_accepted
        self.ids['self_offered'].disabled = disabled
        self.ids['self_wanted'].disabled = disabled
        pw = self.ids['peer_wanted']
        pw.labels = list(trade.peer_gems.wanted)
        po = self.ids['peer_offered']
        po.labels = list(trade.peer_gems.offered)

    def handle_update(self, *args):
        app = App.get_running_app()
        sw = self.ids['self_wanted']
        wanted = list(sw.strs)
        offered = [gem for v, gem in self.collection if v]
        gl = GemList(wanted, offered)
        ctrl: TradeCtrl = app.trade_ctrl
        trade = ctrl.get_trade(app.current_peer)
        loading = Loading()
        loading.open()
        def cb():
            ctrl.update(trade, gl)
            loading.dismiss()
        threading.Thread(target=cb).start()

    def handle_accept(self, *args):
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        trade = ctrl.get_trade(app.current_peer)
        loading = Loading()
        loading.open()
        def cb():
            ctrl.accept(trade)
            self.trade_copy = trade.copy()
            loading.dismiss()
        threading.Thread(target=cb).start()

    def handle_reject(self, *args):
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        trade = ctrl.get_trade(app.current_peer)
        loading = Loading()
        loading.open()
        def cb():
            ctrl.reject(trade)
            self.trade_copy = trade.copy()
            loading.dismiss()
            self.receive_close()
        threading.Thread(target=cb).start()
    
    def handle_fusion(self, *args):
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        trade = ctrl.get_trade(app.current_peer)
        loading = Loading()
        loading.open()
        def cb():
            ctrl.fuse(trade)
            self.trade_copy = trade.copy()
            loading.dismiss()
        threading.Thread(target=cb).start()
    
    @mainthread
    def receive_update(self, trade: Trade):
        trade.unseen = False
        self.trade_copy = trade.copy()
    
    @mainthread
    def receive_reject(self, **args):
        popup = Warning("A troca foi rejeitada.", title='')
        popup.open()

    @mainthread
    def receive_error(self, **args):
        popup = Warning("Ocorreu um erro durante a troca.")
        popup.open()

    @mainthread
    def receive_close(self, **args):
        app = App.get_running_app()
        app.current_trade = None
        app.back_to_menu()