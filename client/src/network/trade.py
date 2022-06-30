from enum import Enum
from model.misc import GemList
from model.gem import Gem
from nacl.public import PublicKey
from network.endpoint import Endpoint
from exceptions import UnknownError
import socket
import threading


class TradeEvent(Enum):

    TRADE = 0
    ACCEPT = 1
    REJECT = 2
    FUSION = 3
    GEMS = 4
    FINISH = 5


class TradeEndpoint(Endpoint):

    OFFSET = 5

    def __init__(self, trade_port: int, forge_addr, forge_key: PublicKey):
        self.__trade_port = trade_port
        self.__forge_addr = forge_addr
        self.__forge_key = forge_key
        self.__listeners = ([], [], [], [], [])
    
    def set_username(self, username: str):
        self.__username = username
    
    def bind(self, ev: TradeEvent, cb):
        self.__listeners[ev.value].append(cb)

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", self.__trade_port))
            s.listen()
            while True:
                print("TradeEndpoint: Listening...")
                conn, addr = s.accept()
                worker = threading.Thread(
                    target=self.handle,
                    args=(conn, addr)
                )
                worker.start()
    
    def handle(self, conn: socket.socket, addr):
        print(f"Thread@{addr}: connected")
        try:
            with conn:
                pkey = self.recv_key(conn)
                if not pkey:
                    conn.sendall(self.enc_msg(None, None))
                    return
                try:
                    size = self.recv_size(conn, pkey)
                    payload = conn.recv(size)
                    op, args = self.dec_msg(pkey, payload)
                    ev = TradeEvent[op.upper()]
                    print(f"Thread@{addr}: {ev}")
                    for cb in self.__listeners[ev.value]:
                        cb(addr=addr, key=pkey, **args)
                    conn.sendall(self.enc_msg(pkey, "ack"))
                except AttributeError:
                    conn.sendall(self.enc_msg(pkey, "error", code="UnknownOperation"))
                except Exception as e:
                    print(e)
                    conn.sendall(self.enc_msg(pkey, "error", code="UnknownError"))
        except BrokenPipeError:
            print(f"Thread@{addr}: disconnected")

    def update(self, ip: str, pkey: PublicKey, gems: GemList):
        username = self.__username
        wanted = list(gems.wanted)
        offered = list(gems.offered)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, self.__trade_port + self.OFFSET))
            msg = self.enc_msg(pkey, "trade",
                username=username, wanted=wanted, offered=offered)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            self.__ack(s, pkey)

    def accept(self, ip: str, pkey: PublicKey):
        username = self.__username
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, self.__trade_port + self.OFFSET))
            msg = self.enc_msg(pkey, "accept", username=username)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            self.__ack(s, pkey)

    def reject(self, ip: str, pkey: PublicKey):
        username = self.__username
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, self.__trade_port + self.OFFSET))
            msg = self.enc_msg(pkey, "reject", username=username)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            self.__ack(s, pkey)

    def fuse(self, ip: str, pkey: PublicKey):
        username = self.__username
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, self.__trade_port + self.OFFSET))
            msg = self.enc_msg(pkey, "fusion", username=username)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            self.__ack(s, pkey)
    
    def send_gems(self, ip: str, pkey: PublicKey, gems):
        username = self.__username
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, self.__trade_port + self.OFFSET))
            msg = self.enc_msg(pkey, "gems", username=username, gems=gems)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            self.__ack(s, pkey)
    
    def __ack(self, conn, pkey: PublicKey):
        data = conn.recv(1024)
        try:
            op, args = self.dec_msg(pkey, data)
            if op != 'ack':
                raise UnknownError(args)
        except:
            raise UnknownError()

    def fuse_to_forge(self, gems: list[Gem]):
        pass
