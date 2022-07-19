from enum import Enum
from model.misc import GemList
from model.trade import Trade
from network.endpoint import Endpoint
from network.profile import ProfileEndpoint
from exceptions import UnknownError, InvalidGemError, FusionTimeout
import re
import traceback

import grpc
from rmi.client_pb2_grpc import TradeServicer, TradeStub
from rmi.client_pb2 import TradeEvent as TradeEventMsg
from rmi.client_pb2 import TradeGems, TradeResponse
from rmi.forge_pb2 import FusionRequest
from rmi.forge_pb2_grpc import ForgeStub


class TradeEvent(Enum):

    TRADE = 0
    UPDATE = 1
    ACCEPT = 2
    REJECT = 3
    FUSION = 4
    GEMS = 5
    ERROR = 7
    CLOSE = 8

class BadTradeStart(Exception): pass
class TradeNotStarted(Exception): pass

class TradeEndpoint(TradeServicer, Endpoint):

    @staticmethod
    def grpc_ip(addr: str):
        m = re.match(r'(.*):\d+$', addr)
        return m.group(1) if m else None

    def __init__(self, forge_addr, profile_endp: ProfileEndpoint):
        self.__port = 0
        self.__forge_addr = f'{forge_addr[0]}:{forge_addr[1]}'
        self.__listeners = {ev: [] for ev in TradeEvent}
        self.__connections = {}
        self.profile_endp = profile_endp

    def set_port(self, port: int):
        self.__port = port
    
    def bind(self, ev: TradeEvent, cb):
        self.__listeners[ev].append(cb)

    def __emit(self, ev: TradeEvent, **kwargs):
        for cb in self.__listeners[ev]:
            cb(**kwargs)
        
    def __error(self, peerid: str):
        self.__emit(TradeEvent.ERROR, peerid=peerid)
        self.remove_connection(peerid)
    
    def get_connection(self, peerid: str):
        try:
            return self.__connections[peerid]
        except:
            raise TradeNotStarted()
        
    def add_connection(self, peerid, conn):
        self.__connections[peerid] = conn
    
    def remove_connection(self, peerid: str):
        self.__connections.pop(peerid, None)
        self.__emit(TradeEvent.CLOSE, peerid=peerid)

    def send_trade(self, trade: Trade):
        try:
            channel = grpc.insecure_channel(f'{trade.ip}:{trade.port}')
            stub = TradeStub(channel)
            req = TradeEventMsg(peerid=self.uid, peername=self.username, port=self.__port)
            res = stub.trade(req)
            if not res.ack:
                raise BadTradeStart()
            self.add_connection(trade.peerid, stub)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.remove_connection(trade.peerid)
            raise e

    def send_update(self, trade: Trade, gems: GemList):
        try:
            wanted = list(gems.wanted)
            offered = list(gems.offered)
            stub = self.get_connection(trade.peerid)
            req = TradeEventMsg(peerid=self.uid, wanted=wanted, offered=offered)
            res = stub.update(req)
            if not res.ack:
                raise UnknownError()
        except Exception as e:
            self.remove_connection(trade.peerid)
            raise e

    def send_accept(self, trade: Trade):
        try:
            stub = self.get_connection(trade.peerid)
            req = TradeEventMsg(peerid=self.uid)
            res = stub.accept(req)
            if not res.ack:
                raise UnknownError()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.remove_connection(trade.peerid)
            raise e

    def send_reject(self, trade: Trade):
        try:
            stub = self.get_connection(trade.peerid)
            req = TradeEventMsg(peerid=self.uid)
            res = stub.reject(req)
            if not res.ack:
                raise UnknownError()
            self.remove_connection(trade.peerid)
        except Exception as e:
            self.remove_connection(trade.peerid)
            raise e

    def send_fuse(self, trade: Trade):
        try:
            stub = self.get_connection(trade.peerid)
            req = TradeEventMsg(peerid=self.uid)
            res = stub.fuse(req)
            if not res.ack:
                raise UnknownError()
        except Exception as e:
            self.remove_connection(trade.peerid)
            raise e

    def send_gems(self, trade: Trade):
        try:
            stub = self.get_connection(trade.peerid)
            gems = [gem.payload for gem in trade.self_gems.offered]
            req = TradeGems(sender=self.username, gems=gems)
            res = stub.gems(req)
            if not res.ack:
                raise UnknownError()
            self.remove_connection(trade.peerid)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.remove_connection(trade.peerid)
            raise e

    def trade(self, request, context):
        try:
            ip = self.grpc_ip(context.peer())
            self.__emit(TradeEvent.TRADE, peerid=request.peerid, peername=request.peername,
                    ip=ip, port=request.port, key=None)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)

    def update(self, request, context):
        try:
            self.__emit(TradeEvent.UPDATE, peerid=request.peerid,
                wanted=request.wanted, offered=request.offered)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)

    def accept(self, request, context):
        try:
            self.__emit(TradeEvent.ACCEPT, peerid=request.peerid)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)

    def reject(self, request, context):
        try:
            self.__emit(TradeEvent.REJECT, peerid=request.peerid)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)
        finally:
            self.remove_connection(request.peerid)

    def fuse(self, request, context):
        try:
            self.__emit(TradeEvent.FUSION, peerid=request.peerid)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)

    def gems(self, request, context):
        try:
            self.__emit(TradeEvent.GEMS, sender=request.sender, gems=request.gems)
            return TradeResponse(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(request.peerid)
            return TradeResponse(ack=False)
    
    def send_fusion_to_forge(self, trade: Trade):
        try:
            token = self.profile_endp.auth()
            gems = [gem.payload for gem in trade.self_gems.offered]
            channel = grpc.insecure_channel(self.__forge_addr)
            stub = ForgeStub(channel)
            req = FusionRequest(token=token, peerid=trade.peerid, gems=gems)
            res = stub.fuse(req)
            if res.error == 'InvalidGems':
                raise InvalidGemError()
            if res.error == 'Timeout':
                raise FusionTimeout()
            if res.error:
                raise UnknownError()
            self.__emit(TradeEvent.GEMS, sender='The Forge', gems=res.gems)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise e
        finally:
            self.remove_connection(trade.peerid)
