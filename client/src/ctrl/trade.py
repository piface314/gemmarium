from ctrl.collection import CollectionCtrl
from model.misc import GemList, SearchResult
from model.trade import Trade
from network.trade import TradeEndpoint


class TradeCtrl:

    def __init__(self, col_ctrl: CollectionCtrl, endp: TradeEndpoint):
        self.__collection_ctrl = col_ctrl
        self.__endpoint = endp
        self.__trades = {}

    def load(self):
        pass

    def list(self):
        return []
    
    def create(sr: SearchResult):
        pass

    def update(trade: Trade, from_self: bool, gems: GemList):
        pass

    def accept(trade: Trade, from_self: bool):
        pass

    def reject(trade: Trade, from_self: bool):
        pass

    def fuse(trade: Trade, from_self: bool):
        pass
