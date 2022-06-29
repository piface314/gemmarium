from datetime import datetime
from ctrl.collection import CollectionCtrl
from model.misc import GemList, SearchResult
from model.trade import Trade
from network.trade import TradeEndpoint, TradeEvent


class TradeCtrl:

    def __init__(self, col_ctrl: CollectionCtrl, endp: TradeEndpoint):
        self.__collection_ctrl = col_ctrl
        self.__listeners = ([], [], [], [], [], [])
        self.__endpoint = endp
        self.__trades: dict[str, Trade] = {}
        endp.bind(TradeEvent.TRADE,
            lambda username, wanted, offered, addr, key, **args:
                self.__receive_update(username, GemList(wanted, offered), addr[0], key))
        endp.bind(TradeEvent.ACCEPT, lambda peer, **args: self.accept(self.get_trade(peer), False))
        endp.bind(TradeEvent.REJECT, lambda peer, **args: self.reject(self.get_trade(peer), False))
        endp.bind(TradeEvent.FUSION, lambda peer, **args: self.fuse(self.get_trade(peer), False))
        endp.bind(TradeEvent.GEMS, lambda peer, gems, **args: self.receive(peer, gems))

    def bind(self, ev: TradeEvent, cb):
        listeners = self.__listeners[ev.value]
        i = len(listeners)
        listeners.append(cb)
        return i
    
    def unbind(self, ev: TradeEvent, i: int):
        ls = self.__listeners[ev.value]
        if not 0 <= i < len(ls):
            return
        self.__listeners[ev.value] = ls[:i] + ls[i+1:]

    def list(self):
        trades = self.__trades.values()
        return sorted(trades, key=lambda t: t.last_update_at)
    
    def count_unseen(self):
        return sum(t.unseen for t in self.__trades.values())
    
    def get_trade(self, peername: str):
        return self.__trades.get(peername, None)
    
    def add_trade(self, trade: Trade):
        trade.self_gems = self.__collection_ctrl.get_gallery()
        self.__trades[trade.peername] = trade
        return trade

    def update(self, trade: Trade, gems: GemList):
        if not trade:
            return
        gl = GemList(gems.wanted, [g.name for g in gems.offered])
        self.__endpoint.update(trade.ip, trade.key, gl)
        trade.self_gems = gems
        trade.last_update_at = datetime.now()
            
    def __receive_update(self, peername: str, gems: GemList, ip, key):
        trade = self.get_trade(peername)
        if not trade:
            trade = Trade(peername, ip, key)
            self.add_trade(trade)
        trade.last_update_at = datetime.now()
        trade.peer_gems = gems
        trade.unseen = True
        for cb in self.__listeners[TradeEvent.TRADE.value]:
            cb(trade)

    def accept(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            self.__endpoint.accept(trade.ip, trade.key)
            trade.self_accepted = True
            trade.last_update_at = datetime.now()
        else:
            trade.last_update_at = datetime.now()
            trade.peer_accepted = True
            trade.unseen = True
            for cb in self.__listeners[TradeEvent.ACCEPT.value]:
                cb(trade)
        if trade.self_accepted and trade.peer_accepted:
            gems = [gem.payload for gem in trade.self_gems]
            self.__endpoint.send_gems(trade.ip, trade.key, gems)
            for cb in self.__listeners[TradeEvent.FINISH.value]:
                cb(trade)

    def reject(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            try:
                self.__endpoint.reject(trade.ip, trade.key)
            except Exception as e:
                print("TradeCtrl: ", e)
            self.__trades.pop(trade.peername, None)
        else:
            self.__trades.pop(trade.peername, None)
            for cb in self.__listeners[TradeEvent.REJECT.value]:
                cb(None)

    def fuse(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            self.__endpoint.fuse(trade.ip, trade.key)
            trade.self_fusion = True
            trade.last_update_at = datetime.now()
        else:
            trade.last_update_at = datetime.now()
            trade.peer_fusion = True
            trade.unseen = True
            for cb in self.__listeners[TradeEvent.FUSION.value]:
                cb(trade)
    
    def receive(self, peername: str, gems):
        gems = [self.__collection_ctrl.new_gem(g) for g in gems]
        for gem in gems:
            self.__collection_ctrl.add_gem(gem)
        for cb in self.__listeners[TradeEvent.TRADE.value]:
            cb(peername, gems)