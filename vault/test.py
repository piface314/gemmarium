from nacl.public import PrivateKey, PublicKey, Box, SealedBox

import src.keys
import grpc
from src.rmi.vault_pb2 import SignupRequest, AuthRequest
from src.rmi.vault_pb2_grpc import AuthStub

skey = PrivateKey.generate()
pkey = skey.public_key

skey2 = PrivateKey(b't\x05\xb3\xd4\x199b*Q\xb4\t\x9eC_az@\xf4#y\xbbD\xe4\xe1$\x942\x89\xe0-\xbd\xe7')
pkey2 = PublicKey(b'\xc1\x8a\xe8D1\xb9Q:\xcf\x88o\x1b\x8f\xea\xad\nv4\xce\xa2\xf0J\xcb\xa5\x9b\x0b\xa6\x80_$\xbds')

# print(f'PrivateKey: {skey}')
# print(f'PublicKey: {pkey}')

vault_pkey = PublicKey(src.keys.vault_pkey)

def request_auth(uid):
    channel = grpc.insecure_channel('localhost:7513')
    stub = AuthStub(channel)
    res = [None, None]
    def auth():
        req = AuthRequest(id=uid)
        print(f"sending {req}")
        yield req
        while not res[0]:
            pass
        print(f"res[0] = {res[0]}")
        if res[0].error:
            print(res[0].error)
            return
        secret = SealedBox(skey2).decrypt(res[0].secret)
        secret = Box(skey2, vault_pkey).encrypt(secret)
        yield AuthRequest(secret=secret)

    for i, r in enumerate(stub.auth(auth())):
        res[i] = r
    print(res[1])

def request_signup(username):
    channel = grpc.insecure_channel('localhost:7513')
    stub = AuthStub(channel)
    req = SignupRequest(username=username, key=pkey.encode())
    res = stub.signup(req)
    print(res)


request_auth('322d85b6-2188-4494-aba1-be9519c5f729')
# request_signup('galeraGRPC')
