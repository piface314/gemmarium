import base64
from enum import Enum
from flask import Flask, request
from model.misc import GemList
from model.trade import Trade
from network.endpoint import Endpoint
from network.profile import ProfileEndpoint
from exceptions import UnknownError, InvalidGemError, FusionTimeout
import re
import requests
import traceback


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

class TradeEndpoint(Endpoint):

    def __init__(self, forge_addr, profile_endp: ProfileEndpoint):
        self.__port = 0
        self.__forge_addr = f'http://{forge_addr[0]}:{forge_addr[1]}'
        self.__listeners = {ev: [] for ev in TradeEvent}
        self.profile_endp = profile_endp
        self.app = Flask(__name__)
        self.app.route("/trade", methods=["POST"])(self.trade)
        self.app.route("/update", methods=["POST"])(self.update)
        self.app.route("/accept", methods=["POST"])(self.accept)
        self.app.route("/reject", methods=["POST"])(self.reject)
        self.app.route("/fuse", methods=["POST"])(self.fuse)
        self.app.route("/gems", methods=["POST"])(self.gems)


    def set_port(self, port: int):
        self.__port = port
    
    def bind(self, ev: TradeEvent, cb):
        self.__listeners[ev].append(cb)

    def __emit(self, ev: TradeEvent, **kwargs):
        for cb in self.__listeners[ev]:
            cb(**kwargs)
        
    def __error(self, peerid: str):
        self.__emit(TradeEvent.ERROR, peerid=peerid)
        self.__emit(TradeEvent.CLOSE, peerid=peerid)

    def send_trade(self, trade: Trade):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            body = dict(peername=self.username, port=self.__port)
            res = requests.post(addr+"/trade", params=dict(peerid=self.uid), json=body)
            if res.status_code != 200:
                raise BadTradeStart()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def send_update(self, trade: Trade, gems: GemList):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            wanted = list(gems.wanted)
            offered = list(gems.offered)
            body = dict(wanted=wanted, offered=offered)
            res = requests.post(addr+"/update", params=dict(peerid=self.uid), json=body)
            if res.status_code != 200:
                raise UnknownError()
        except Exception as e:
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def send_accept(self, trade: Trade):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            res = requests.post(addr+"/accept", params=dict(peerid=self.uid))
            if res.status_code != 200:
                raise UnknownError()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def send_reject(self, trade: Trade):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            res = requests.post(addr+"/reject", params=dict(peerid=self.uid))
            if res.status_code != 200:
                raise UnknownError()
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
        except Exception as e:
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def send_fuse(self, trade: Trade):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            res = requests.post(addr+"/fuse", params=dict(peerid=self.uid))
            if res.status_code != 200:
                raise UnknownError()
        except Exception as e:
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def send_gems(self, trade: Trade):
        try:
            addr = f'http://{trade.ip}:{trade.port}'
            gems = [base64.b64encode(gem.payload).decode()
                for gem in trade.self_gems.offered]
            body = dict(sender=self.username, gems=gems)
            res = requests.post(addr+"/gems", params=dict(peerid=self.uid), json=body)
            if res.status_code != 200:
                raise UnknownError()
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
            raise e

    def trade(self):
        try:
            ip = request.remote_addr
            body = request.get_json()
            peerid = request.args.get('peerid')
            self.__emit(TradeEvent.TRADE, peerid=peerid, peername=body['peername'],
                    ip=ip, port=body['port'], key=None)
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(peerid)
            return dict(ack=False), 400

    def update(self):
        try:
            body = request.get_json()
            peerid = request.args.get('peerid')
            self.__emit(TradeEvent.UPDATE, peerid=peerid,
                wanted=body['wanted'], offered=body['offered'])
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(body['peerid'])
            return dict(ack=False), 400

    def accept(self):
        try:
            peerid = request.args.get('peerid')
            self.__emit(TradeEvent.ACCEPT, peerid=peerid)
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(peerid)
            return dict(ack=False), 400

    def reject(self):
        try:
            peerid = request.args.get('peerid')
            self.__emit(TradeEvent.REJECT, peerid=peerid)
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(peerid)
            return dict(ack=False), 400
        finally:
            self.__emit(TradeEvent.CLOSE, peerid=peerid)

    def fuse(self):
        try:
            peerid = request.args.get('peerid')
            self.__emit(TradeEvent.FUSION, peerid=peerid)
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(peerid)
            return dict(ack=False), 400

    def gems(self):
        try:
            peerid = request.args.get('peerid')
            body = request.get_json()
            self.__emit(TradeEvent.GEMS, sender=body['sender'],
                gems=[base64.b64decode(g) for g in body['gems']])
            return dict(ack=True)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.__error(peerid)
            return dict(ack=False), 400
    
    def send_fusion_to_forge(self, trade: Trade):
        try:
            token = self.profile_endp.auth()
            gems = [base64.b64encode(gem.payload).decode()
                for gem in trade.self_gems.offered]
            body = dict(token=token, peerid=trade.peerid, gems=gems)
            res = requests.post(self.__forge_addr+"/fuse", json=body)
            if res.status_code != 200:
                error = res.json()['error']
                if error == 'InvalidGems':
                    raise InvalidGemError()
                if error == 'Timeout':
                    raise FusionTimeout()
                raise UnknownError()
            self.__emit(TradeEvent.GEMS, sender='The Forge', gems=[
                base64.b64decode(g) for g in res.json()['gems']
            ])
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise e
        finally:
            self.__emit(TradeEvent.CLOSE, peerid=trade.peerid)
