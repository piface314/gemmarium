from datetime import datetime
from exceptions import QuotaError, InvalidGemError
from model.gem import Gem
from nacl.encoding import Base64Encoder
from nacl.exceptions import CryptoError
from nacl.public import PrivateKey, PublicKey, SealedBox, Box
from nacl.signing import VerifyKey
import json
import socket


class CollectionEndpoint:

    def __init__(self, forge_addr, forge_key: PublicKey, verify_key: VerifyKey):
        self.__forge_addr = forge_addr
        self.__forge_key = forge_key
        self.__verify_key = verify_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey
    
    def request_gem(self, username: str):
        skey = self.__private_key
        pkey = self.__public_key
        forge_pkey = self.__forge_key
        forge_vkey = self.__verify_key
        with socket.socket() as s:
            s.connect(self.__forge_addr)
            payload = json.dumps(['request', dict(username=username)]).encode('utf-8')
            box = Box(skey, forge_pkey)
            msg = box.encrypt(payload)
            s.sendall(SealedBox(forge_pkey).encrypt(pkey.encode()))
            s.sendall(msg)
            data = s.recv(4096)
        op, args = json.loads(box.decrypt(data))
        if op == 'gem':
            gem_raw = args['gem']
            try:
                gem_bytes = forge_vkey.verify(gem_raw, encoder=Base64Encoder)
            except CryptoError:
                raise InvalidGemError()
            gem = json.loads(gem_bytes)
            return Gem(gem['id'], gem['name'], gem['desc'],
                Base64Encoder.decode(gem['sprite']), gem['created_for'], gem['created_by'],
                datetime.fromisoformat(gem['created_at']), datetime.now(),
                False, gem_raw)
        else:
            raise QuotaError(args['wait'])
