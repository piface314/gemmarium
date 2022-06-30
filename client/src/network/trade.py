from enum import Enum
from model.gem import Gem
from model.misc import GemList
from model.trade import Trade
from nacl.public import PublicKey
from network.endpoint import Endpoint
from exceptions import UnknownError
import socket
import threading
import traceback


class TradeEvent(Enum):

    TRADE = 0
    UPDATE = 1
    ACCEPT = 2
    REJECT = 3
    FUSION = 4
    GEMS = 5
    FINISH = 6

class BadTradeStart(Exception):

    pass

class TradeNotStarted(Exception):

    pass

class TradeEndpoint(Endpoint):

    def __init__(self, trade_port: int, forge_addr, forge_key: PublicKey):
        self.__trade_port = trade_port
        self.__forge_addr = forge_addr
        self.__forge_key = forge_key
        self.__listeners = ([], [], [], [], [], [])
        self.__connections = {}
    
    def set_identity(self, id: str, username: str):
        self.__id = id
        self.__username = username
    
    def bind(self, ev: TradeEvent, cb):
        self.__listeners[ev.value].append(cb)
    
    def get_connection(self, peerid: str):
        try:
            return self.__connections[peerid]
        except:
            raise TradeNotStarted()

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", self.__trade_port))
            s.listen()
            while True:
                print("TradeEndpoint: Listening...")
                conn, addr = s.accept()
                worker = threading.Thread(
                    target=self.handle,
                    args=(conn, addr),
                    daemon=True
                )
                worker.start()
    
    def handle(self, conn: socket.socket, addr):
        print(f"TradeEndpoint@{addr}: connected")
        peerid = None
        try:
            try:
                pkey = self.recv_key(conn)
                while True:
                    size = self.recv_size(conn, pkey)
                    payload = conn.recv(size)
                    op, args = self.dec_msg(pkey, payload)
                    if peerid is None:
                        if op != 'trade':
                            raise BadTradeStart()
                        print(f"TradeEndpoint@{addr}: trade start")
                        for cb in self.__listeners[TradeEvent.TRADE.value]:
                            cb(ip=addr[0], key=pkey, **args)
                        peerid = args['peerid']
                        self.__send_ack(conn, pkey)
                        continue
                    ev = TradeEvent[op.upper()]
                    print(f"TradeEndpoint@{addr}: {ev}")
                    for cb in self.__listeners[ev.value]:
                        cb(peerid=peerid,**args)
                    self.__send_ack(conn, pkey)
            except BrokenPipeError:
                raise BrokenPipeError()
            except BadTradeStart:
                conn.sendall(self.enc_msg(pkey, "error", code="BadTradeStart"))
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                conn.sendall(self.enc_msg(pkey, "error", code="UnknownError"))
        except BrokenPipeError:
            print(f"TradeEndpoint@{addr}: disconnected")
        finally:
            conn.close()

    def start(self, trade: Trade):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((trade.ip, trade.port))
        peerid = self.__id
        peername = self.__username
        port = self.__trade_port
        msg = self.enc_msg(trade.key, "trade", peerid=peerid, peername=peername, port=port)
        self.send_key(s, trade.key)
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)
        self.__connections[trade.peerid] = s

    def update(self, trade: Trade, gems: GemList):
        wanted = list(gems.wanted)
        offered = list(gems.offered)
        s: socket.socket = self.get_connection(trade.peerid)
        msg = self.enc_msg(trade.key, "update", wanted=wanted, offered=offered)
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)

    def accept(self, trade: Trade):
        s: socket.socket = self.get_connection(trade.peerid)
        msg = self.enc_msg(trade.key, "accept")
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)

    def reject(self, trade: Trade):
        s: socket.socket = self.get_connection(trade.peerid)
        msg = self.enc_msg(trade.key, "reject")
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)
        self.__connections.pop(trade.peerid, None)
        s.close()
    
    def send_gems(self, trade: Trade, gems):
        s: socket.socket = self.get_connection(trade.peerid)
        msg = self.enc_msg(trade.key, "gems", gems=gems)
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)
        self.__connections.pop(trade.peerid, None)
        s.close()
    
    def __send_ack(self, conn, pkey: PublicKey):
        conn.sendall(self.enc_msg(pkey, "ack"))

    def __ack(self, conn, pkey: PublicKey):
        data = conn.recv(1024)
        try:
            op, args = self.dec_msg(pkey, data)
            if op != 'ack':
                raise UnknownError(args)
        except:
            raise UnknownError()

    def fuse(self, trade: Trade):
        s: socket.socket = self.get_connection(trade.peerid)
        msg = self.enc_msg(trade.key, "fusion")
        self.send_size(s, trade.key, msg)
        s.sendall(msg)
        self.__ack(s, trade.key)

    def fuse_to_forge(self, gems: list[Gem]):
        pass
