from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder, RawEncoder
from nacl.exceptions import CryptoError
import json
import socket
import threading
import traceback


class AuthError(Exception):

    pass

class PublicKeyError(Exception):

    pass


class Server:

    def __init__(self, private_key: PrivateKey, public_key: PublicKey):
        self.__private_key = private_key
        self.__public_key = public_key
        self.__trusted_hosts = {}

    def trust_host(self, addr, pkey):
        self.__trusted_hosts[addr] = pkey

    def get_key(self, addr):
        return self.__trusted_hosts.get(addr, None)

    def close(self):
        pass
    
    def enc_msg(self, pkey: PublicKey, op: str, **args):
        payload = json.dumps([op, args]).encode('utf-8')
        box = Box(self.__private_key, pkey)
        return box.encrypt(payload)

    def dec_msg(self, pkey: PublicKey, payload: bytes):
        box = Box(self.__private_key, pkey)
        return json.loads(box.decrypt(payload))

    def recv_key(self, conn, addr, keep: bool):
        if keep:
            return self.get_key(addr)
        try:
            box = SealedBox(self.__private_key)
            payload = box.decrypt(conn.recv(80))
            return PublicKey(payload)
        except:
            raise PublicKeyError()
    
    def recv_size(self, conn, pkey: PublicKey):
        box = Box(self.__private_key, pkey)
        size = box.decrypt(conn.recv(44))
        return int.from_bytes(size, 'little')
    
    def send_size(self, conn, pkey: PublicKey, msg: bytes):
        size = len(msg).to_bytes(4, 'little')
        box = Box(self.__private_key, pkey)
        conn.sendall(box.encrypt(size))
    
    def send(self, conn, pkey: PublicKey, op: str, **args):
        conn.sendall(self.enc_msg(pkey, op, **args))
    
    def listen(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(self.addr)
                s.listen()
                while True:
                    print("Listening...")
                    conn, addr = s.accept()
                    # conn.settimeout(5)
                    keep = addr in self.__trusted_hosts
                    worker = threading.Thread(
                        target=self.handle,
                        args=(conn, addr, keep)
                    )
                    worker.start()
        finally:
            s.close()
            self.close()

    def handle(self, conn, addr, keep):
        print(f"Thread@{addr}: connected")
        try:
            try:
                pkey = self.recv_key(conn, addr, keep)
                run = True
                while run:
                    if not keep:
                        run = False
                    size = self.recv_size(conn, pkey)
                    payload = conn.recv(size)
                    op, args = self.dec_msg(pkey, payload)
                    handler = self.__getattribute__("handle_" + op)
                    handler(conn, addr, pkey, **args)
            except AttributeError:
                conn.sendall(self.enc_msg(pkey, "error", code="UnknownOperation"))
            except AuthError:
                conn.sendall(self.enc_msg(pkey, "error", code="AuthError"))
            except PublicKeyError:
                msg = json.dumps(["error", {"code": "BadPublicKey"}]).encode('utf-8')
                conn.sendall(msg)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                conn.sendall(self.enc_msg(pkey, "error", code="UnknownError"))
        except BrokenPipeError:
            print(f"Thread@{addr}: disconnected")
        finally:
            conn.close()