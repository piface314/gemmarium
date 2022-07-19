from nacl.public import PrivateKey, PublicKey, SealedBox, Box
import json


class Endpoint:

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.private_key = skey
        self.public_key = pkey

    def set_identity(self, uid: str, username: str):
        self.uid = uid
        self.username = username

    def enc_msg(self, pkey: PublicKey, op, **args):
        if pkey:
            payload = json.dumps([op, args]).encode('utf-8')
            box = Box(self.private_key, pkey)
            return box.encrypt(payload)
        else:
            return json.dumps(["error", {"code": "UnknownError"}]).encode('utf-8')

    def dec_msg(self, pkey: PublicKey, payload):
        box = Box(self.private_key, pkey)
        return json.loads(box.decrypt(payload))

    def recv_key(self, conn):
        try:
            box = SealedBox(self.private_key)
            payload = box.decrypt(conn.recv(80))
            return PublicKey(payload)
        except:
            return None
