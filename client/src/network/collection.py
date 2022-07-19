from exceptions import AuthError, QuotaError, UnknownError
from network.endpoint import Endpoint
from network.profile import ProfileEndpoint

import grpc
from rmi.forge_pb2 import GemRequest
from rmi.forge_pb2_grpc import ForgeStub

class CollectionEndpoint(Endpoint):

    def __init__(self, forge_addr, profile_endp: ProfileEndpoint):
        self.forge_addr = f'{forge_addr[0]}:{forge_addr[1]}'
        self.profile_endp = profile_endp

    def request_gem(self):
        token = self.profile_endp.auth()
        channel = grpc.insecure_channel(self.forge_addr)
        stub = ForgeStub(channel)
        req = GemRequest(token=token)
        res = stub.gem(req)
        if res.error == 'AuthError':
            raise AuthError()
        if res.error == 'QuotaExceeded':
            raise QuotaError(res.wait)
        if res.error:
            raise UnknownError()
        return res.gem
