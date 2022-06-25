from nacl.public import PrivateKey, PublicKey, SealedBox, Box
from nacl.encoding import Base64Encoder
from exceptions import InvalidUsernameError, UnknownError, UsernameTakenError
import json
import socket


class ProfileEndpoint:

    def __init__(self, vault_addr, vault_key: PublicKey):
        self.__vault_addr = vault_addr
        self.__vault_key = vault_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey

    def signup(self, username: str, key: PublicKey):
        skey = self.__private_key
        pkey = self.__public_key
        vault_pkey = self.__vault_key
        with socket.socket() as s:
            s.connect(self.__vault_addr)
            key = pkey.encode(Base64Encoder).decode()
            payload = json.dumps(['signup', dict(username=username, key=key)]).encode('utf-8')
            box = Box(skey, vault_pkey)
            msg = box.encrypt(payload)
            s.sendall(SealedBox(vault_pkey).encrypt(pkey.encode()))
            s.sendall(msg)
            data = s.recv(1024)
        op, args = json.loads(box.decrypt(data))
        if op != 'ack':
            code = args['code']
            if code == 'UsernameTaken':
                raise UsernameTakenError()
            elif code == 'InvalidUsername':
                raise InvalidUsernameError()
            else:
                raise UnknownError()
            
