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
    
    def enc_msg(self, pkey: PublicKey, op: str, **args):
        payload = json.dumps([op, args]).encode('utf-8')
        box = Box(self.__private_key, pkey)
        return box.encrypt(payload)

    def dec_msg(self, pkey: PublicKey, payload: bytes):
        box = Box(self.__private_key, pkey)
        return json.loads(box.decrypt(payload))

    def recv_key(self, conn):
        try:
            box = SealedBox(self.__private_key)
            payload = box.decrypt(conn.recv(80))
            return PublicKey(payload)
        except:
            raise PublicKeyError()

    def send_key(self, conn, pkey: PublicKey):
        box = SealedBox(pkey)
        conn.sendall(box.encrypt(self.__public_key.encode()))
    
    def recv_size(self, conn, pkey: PublicKey):
        box = Box(self.__private_key, pkey)
        size = box.decrypt(conn.recv(44))
        return int.from_bytes(size, 'little')
    
    def recvall(self, conn, pkey: PublicKey):
        size = self.recv_size(conn, pkey)
        payload = b''
        while size - len(payload) > 0:
            payload += conn.recv(size - len(payload))
        return payload
    
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
                    worker = threading.Thread(
                        target=self.handle,
                        args=(conn, addr)
                    )
                    worker.start()
        finally:
            s.close()

    def handle(self, conn, addr):
        print(f"Thread@{addr}: connected")
        try:
            try:
                pkey = self.recv_key(conn)
                payload = self.recvall(conn, pkey)
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