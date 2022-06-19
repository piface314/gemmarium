from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder
import json
import socket
import threading


class Server:

    def __init__(self, private_key, public_key):
        self.__private_key = PrivateKey(private_key)
        self.__public_key = PublicKey(public_key)
        self.__buffer_size = 1024
        self.__trusted_keys = {}
        self.__known_keys = {}

    def set_buffer_size(self, size):
        self.__buffer_size = size

    def trust_key(self, addr, pkey):
        self.__trusted_keys[addr] = PublicKey(pkey)

    def learn_key(self, addr, pkey, encoder=Base64Encoder):
        self.__known_keys[addr] = PublicKey(pkey, encoder)

    def get_key(self, addr):
        return (self.__known_keys | self.__trusted_keys).get(addr, None)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.addr)
            s.listen()
            while True:
                print("Listening...")
                conn, addr = s.accept()
                worker = threading.Thread(
                    target=self.handle, args=(conn, addr))
                worker.start()

    def send_msg(self, addr, op, **args):
        pkey = self.get_key(addr)
        if pkey:
            payload = json.dumps([op, args]).encode('utf-8')
            box = Box(self.__private_key, pkey)
            return box.encrypt(payload)
        else:
            return json.dumps(["error", {"code": "UnknownError"}]).encode('utf-8')

    def recv_msg(self, addr, payload):
        pkey = self.get_key(addr)
        skey = self.__private_key
        box = SealedBox(skey) if pkey is None else Box(skey, pkey)
        msg = json.loads(box.decrypt(payload))
        if 'key' in msg[1]:
            self.learn_key(addr, msg[1]['key'])
        return msg

    def handle(self, conn, addr):
        with conn:
            print(f"Thread@{addr}: connected")
            try:
                payload = conn.recv(self.__buffer_size)
                op, args = self.recv_msg(addr, payload)
                handler = self.__getattribute__("handle_" + op)
                handler(conn, addr, **args)
            except AttributeError:
                conn.sendall(self.send_msg(addr, "error", code="UnknownOperation"))
            except Exception as e:
                print(e)
                conn.sendall(self.send_msg(addr, "error", code="UnknownError"))
