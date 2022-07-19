from nacl.public import PublicKey, SealedBox, Box
from network.endpoint import Endpoint
from exceptions import InvalidUsernameError, UnknownError, UsernameTakenError, AuthError

import grpc
from rmi.vault_pb2 import SignupRequest, AuthRequest
from rmi.vault_pb2_grpc import AuthStub

class ProfileEndpoint(Endpoint):

    def __init__(self, vault_addr, vault_key: PublicKey):
        self.vault_addr = f'{vault_addr[0]}:{vault_addr[1]}'
        self.vault_key = vault_key

    def signup(self, username: str):
        channel = grpc.insecure_channel(self.vault_addr)
        stub = AuthStub(channel)
        req = SignupRequest(username=username, key=self.public_key.encode())
        res = stub.signup(req)
        if res.error == 'InvalidUsername':
            raise InvalidUsernameError()
        if res.error == 'UsernameTaken':
            raise UsernameTakenError()
        if res.error:
            raise UnknownError()
        return res.id

    def auth(self):
        channel = grpc.insecure_channel(self.vault_addr)
        stub = AuthStub(channel)
        res = [None, None]

        def auth():
            req = AuthRequest(id=self.uid)
            yield req
            while not res[0]:
                pass
            if res[0].error:
                raise AuthError()
            secret = SealedBox(self.private_key).decrypt(res[0].secret)
            secret = Box(self.private_key, self.vault_key).encrypt(secret)
            yield AuthRequest(secret=secret)

        for i, r in enumerate(stub.auth(auth())):
            res[i] = r

        if res[1].error:
            raise AuthError()
        return res[1].token
