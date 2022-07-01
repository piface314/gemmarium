from nacl.public import PrivateKey, PublicKey, Box, SealedBox
import json


class Endpoint:

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey
    
    def get_pkey(self):
        return self.__public_key
    
    def get_skey(self):
        return self.__private_key

    def enc_msg(self, pkey: PublicKey, op, **args):
        if pkey:
            payload = json.dumps([op, args]).encode('utf-8')
            box = Box(self.__private_key, pkey)
            return box.encrypt(payload)
        else:
            return json.dumps(["error", {"code": "UnknownError"}]).encode('utf-8')

    def dec_msg(self, pkey: PublicKey, payload):
        box = Box(self.__private_key, pkey)
        return json.loads(box.decrypt(payload))

    def recv_key(self, conn):
        try:
            box = SealedBox(self.__private_key)
            payload = box.decrypt(conn.recv(80))
            return PublicKey(payload)
        except:
            return None
        
    def send_key(self, conn, pkey: PublicKey):
        box = SealedBox(pkey)
        conn.sendall(box.encrypt(self.__public_key.encode()))
    
    def recv_size(self, conn, pkey: PublicKey):
        box = Box(self.__private_key, pkey)
        payload = conn.recv(44)
        if not payload:
            raise BrokenPipeError
        size = box.decrypt(payload)
        return int.from_bytes(size, 'little')

    def send_size(self, conn, pkey: PublicKey, msg: bytes):
        size = len(msg).to_bytes(4, 'little')
        box = Box(self.__private_key, pkey)
        conn.sendall(box.encrypt(size))
        