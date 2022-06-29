from exceptions import QuotaError
from nacl.public import PublicKey
from network.endpoint import Endpoint
import socket


class CollectionEndpoint(Endpoint):

    def __init__(self, forge_addr, forge_key: PublicKey):
        self.__forge_addr = forge_addr
        self.__forge_key = forge_key

    def request_gem(self, username: str):
        forge_pkey = self.__forge_key
        with socket.socket() as s:
            s.connect(self.__forge_addr)
            msg = self.enc_msg(forge_pkey, 'request', username=username)
            self.send_key(s, forge_pkey)
            self.send_size(s, forge_pkey, msg)
            s.sendall(msg)
            data = s.recv(4096)
        op, args = self.dec_msg(forge_pkey, data)
        if op == 'gem':
            return args['gem']
        else:
            raise QuotaError(args['wait'])
