from datetime import datetime
from ctrl.collection import CollectionCtrl
from model.misc import GemList, SearchResult
from model.trade import Trade
from network.trade import TradeEndpoint, TradeEvent


class TradeCtrl:

    def __init__(self, col_ctrl: CollectionCtrl, endp: TradeEndpoint):
        self.__collection_ctrl = col_ctrl
        self.__listeners = {ev: [] for ev in TradeEvent}
        self.__endpoint = endp
        self.__trades: dict[str, Trade] = {}
        endp.bind(TradeEvent.TRADE,
            lambda ip, key, peerid, peername, port, **_:
                self.start_trade(SearchResult(peerid, peername, ip, port, key, GemList([], []), False), False))
        endp.bind(TradeEvent.UPDATE,
            lambda peerid, wanted, offered, **_:
                self.update(self.get_trade(peerid), GemList(wanted, offered), False))
        endp.bind(TradeEvent.ACCEPT, lambda peerid, **_: self.accept(self.get_trade(peerid), False))
        endp.bind(TradeEvent.REJECT, lambda peerid, **_: self.reject(self.get_trade(peerid), False))
        endp.bind(TradeEvent.FUSION, lambda peerid, **_: self.fuse(self.get_trade(peerid), False))
        endp.bind(TradeEvent.GEMS, lambda peerid, gems, **_: self.receive(self.get_trade(peerid), gems))
        endp.bind(TradeEvent.ERROR, lambda peerid, **_: self.error(self.get_trade(peerid)))
        endp.bind(TradeEvent.CLOSE, lambda peerid, **_: self.close(self.get_trade(peerid)))

    def bind(self, ev: TradeEvent, cb):
        listeners = self.__listeners[ev]
        i = len(listeners)
        listeners.append(cb)
        return i
    
    def unbind(self, ev: TradeEvent, i: int):
        ls = self.__listeners[ev]
        if not 0 <= i < len(ls):
            return
        self.__listeners[ev] = ls[:i] + ls[i+1:]
    
    def __emit(self, ev: TradeEvent, **args):
        for cb in self.__listeners[ev]:
            cb(**args)

    def list(self):
        trades = self.__trades.values()
        return sorted(trades, key=lambda t: t.last_update_at)
    
    def count_unseen(self):
        return sum(t.unseen for t in self.__trades.values())
    
    def get_trade(self, peerid: str):
        return self.__trades.get(peerid, None)
    
    def add_trade(self, trade: Trade):
        if trade.peerid in self.__trades:
            self.__endpoint.reject(trade)
        trade.self_gems = self.__collection_ctrl.get_gallery()
        self.__trades[trade.peerid] = trade
        return trade
    
    def remove_trade(self, trade: Trade):
        if not trade:
            return
        self.__trades.pop(trade.peerid, None)

    def start_trade(self, sr: SearchResult, from_self: bool = True):
        if from_self or sr.id not in self.__trades:
            trade = self.add_trade(Trade.from_search_result(sr))
            self.__endpoint.start(trade)
            if not from_self:
                self.__emit(TradeEvent.UPDATE, trade=self.get_trade(sr.id))
        return self.get_trade(sr.id)

    def update(self, trade: Trade, gems: GemList, from_self: bool = True):
        if not trade:
            return
        if from_self:
            gl = GemList(gems.wanted, [g.name for g in gems.offered])
            self.__endpoint.update(trade, gl)
            trade.self_gems = gems
            trade.last_update_at = datetime.now()
        else:
            trade.last_update_at = datetime.now()
            trade.peer_gems = gems
            trade.unseen = True
            self.__emit(TradeEvent.UPDATE, trade=trade)

    def accept(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            self.__endpoint.accept(trade)
            trade.self_accepted = True
            trade.last_update_at = datetime.now()
        else:
            trade.last_update_at = datetime.now()
            trade.peer_accepted = True
            trade.unseen = True
            self.__emit(TradeEvent.ACCEPT, trade=trade)
        if trade.self_accepted and trade.peer_accepted:
            gems = [gem.payload for gem in trade.self_gems.offered]
            self.__endpoint.send_gems(trade, gems)
            for gem in trade.self_gems.offered:
                self.__collection_ctrl.remove_gem(gem)

    def reject(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            try:
                self.__endpoint.reject(trade)
            finally:
                self.remove_trade(trade)
        else:
            self.remove_trade(trade)
            self.__emit(TradeEvent.REJECT, trade=None)
    
    def error(self, trade: Trade):
        self.remove_trade(trade)
        self.__emit(TradeEvent.ERROR, trade=None)

    def close(self, trade: Trade):
        self.remove_trade(trade)
        self.__emit(TradeEvent.CLOSE, trade=None)

    def fuse(self, trade: Trade, from_self: bool = True):
        if not trade:
            return
        if from_self:
            self.__endpoint.fuse(trade)
            trade.self_fusion = True
            trade.last_update_at = datetime.now()
        else:
            trade.last_update_at = datetime.now()
            trade.peer_fusion = True
            trade.unseen = True
            self.__emit(TradeEvent.FUSION, trade=trade)
        if trade.self_fusion and trade.peer_fusion:
            # TODO
            pass
    
    def receive(self, trade: Trade, gems):
        gems = [self.__collection_ctrl.new_gem(g) for g in gems]
        for gem in gems:
            self.__collection_ctrl.add_gem(gem)
        self.__emit(TradeEvent.GEMS, sender=trade.peername, gems=gems)