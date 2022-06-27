from nacl.public import PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder, RawEncoder
from nacl.exceptions import CryptoError
import json
import socket
import threading


class UnauthorizedError(Exception):

    pass


class Server:

    def __init__(self, private_key, public_key):
        self.__private_key = private_key
        self.__public_key = public_key
        self.__buffer_size = 1024
        self.__trusted_keys = {}
        self.__known_keys = {}
        self.__known_hosts = set()

    def set_buffer_size(self, size):
        self.__buffer_size = size

    def __set_key(self, d, addr, pkey, encoder):
        if encoder is None:
            d[addr] = pkey
        else:
            d[addr] = PublicKey(pkey, encoder)

    def trust_key(self, addr, pkey, encoder=None):
        self.__set_key(self.__trusted_keys, addr, pkey, encoder)

    def learn_key(self, addr, pkey, encoder=None):
        self.__set_key(self.__known_keys, addr, pkey, encoder)

    def learn_host(self, addr):
        self.__known_hosts.add(addr)

    def get_key(self, addr):
        return ({**self.__known_keys, **self.__trusted_keys}).get(addr, None)

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(self.addr)
                s.listen()
                while True:
                    print("Listening...")
                    conn, addr = s.accept()
                    keep = addr in self.__known_hosts
                    worker = threading.Thread(
                        target=self.handle,
                        args=(conn, addr, keep)
                    )
                    worker.start()
        finally:
            self.close()

    def close(self):
        pass
    
    def enc_msg(self, addr, op, **args):
        pkey = self.get_key(addr)
        if pkey:
            payload = json.dumps([op, args]).encode('utf-8')
            box = Box(self.__private_key, pkey)
            return box.encrypt(payload)
        else:
            return json.dumps(["error", {"code": "UnknownError"}]).encode('utf-8')

    def dec_msg(self, addr, payload):
        pkey = self.get_key(addr)
        skey = self.__private_key
        box = SealedBox(skey) if pkey is None else Box(skey, pkey)
        try:
            msg = json.loads(box.decrypt(payload))
        except CryptoError:
            raise UnauthorizedError()
        return msg

    def recv_key(self, conn, addr):
        box = SealedBox(self.__private_key)
        key = box.decrypt(conn.recv(80))
        self.learn_key(addr, key, RawEncoder)

    def handle(self, conn, addr, keep):
        print(f"Thread@{addr}: connected")
        try:
            with conn:
                while True:
                    try:
                        if not keep:
                            self.recv_key(conn, addr)
                        payload = conn.recv(self.__buffer_size)
                        op, args = self.dec_msg(addr, payload)
                        handler = self.__getattribute__("handle_" + op)
                        handler(conn, addr, **args)
                    except AttributeError:
                        conn.sendall(self.enc_msg(addr, "error", code="UnknownOperation"))
                    except UnauthorizedError:
                        conn.sendall(self.enc_msg(addr, "error", code="Unauthorized"))
                    except Exception as e:
                        print(e)
                        conn.sendall(self.enc_msg(addr, "error", code="UnknownError"))
                    if not keep:
                        break
        except BrokenPipeError:
            print(f"Thread@{addr}: disconnected")
