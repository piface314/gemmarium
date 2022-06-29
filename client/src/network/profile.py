from nacl.public import PublicKey
from nacl.encoding import Base64Encoder
from network.endpoint import Endpoint
from exceptions import InvalidUsernameError, UnknownError, UsernameTakenError
import json
import socket


class ProfileEndpoint(Endpoint):

    def __init__(self, vault_addr, vault_key: PublicKey):
        self.__vault_addr = vault_addr
        self.__vault_key = vault_key

    def signup(self, username: str, key: PublicKey):
        vault_pkey = self.__vault_key
        with socket.socket() as s:
            s.connect(self.__vault_addr)
            key = self.get_pkey().encode(Base64Encoder).decode()
            msg = self.enc_msg(vault_pkey, 'signup', username=username, key=key)
            self.send_key(s, vault_pkey)
            s.sendall(msg)
            data = s.recv(1024)
        op, args = self.dec_msg(vault_pkey, data)
        if op != 'ack':
            code = args['code']
            if code == 'UsernameTaken':
                raise UsernameTakenError()
            elif code == 'InvalidUsername':
                raise InvalidUsernameError()
            else:
                raise UnknownError()
            
