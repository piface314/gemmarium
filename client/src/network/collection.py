from exceptions import QuotaError, UnknownError
from nacl.public import PublicKey
from network.endpoint import Endpoint
import socket


class CollectionEndpoint(Endpoint):

    def __init__(self, forge_addr, forge_key: PublicKey):
        self.__forge_addr = forge_addr
        self.__forge_key = forge_key

    def request_gem(self, id: str, username: str):
        pkey = self.__forge_key
        with socket.socket() as s:
            # request
            s.connect(self.__forge_addr)
            msg = self.enc_msg(pkey, 'request', id=id)
            self.send_key(s, pkey)
            self.send_size(s, pkey, msg)
            s.sendall(msg)
            
            # auth
            data = s.recv(1024)
            op, args = self.dec_msg(pkey, data)
            if op != 'auth':
                raise UnknownError()
            msg = self.enc_msg(pkey, 'auth', secret=args['secret'])
            s.sendall(msg)
            
            # recv
            data = s.recv(4096)
        op, args = self.dec_msg(pkey, data)
        if op == 'gem':
            return args['gem']
        else:
            raise QuotaError(args['wait'])
