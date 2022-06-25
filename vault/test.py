import socket
import json

import src.keys

from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder

skey = PrivateKey.generate()
pkey = skey.public_key

print(f'PrivateKey: {skey}')
print(f'PublicKey: {pkey}')

vault_pkey = PublicKey(src.keys.vault_pkey)

def request_key(username):
    with socket.socket() as s:
        s.connect(("127.0.0.1", 7513))
        payload = json.dumps(['key', dict(username=username)]).encode('utf-8')
        box = Box(skey, vault_pkey)
        msg = box.encrypt(payload)
        s.sendall(SealedBox(vault_pkey).encrypt(pkey.encode()))
        s.sendall(msg)
        data = s.recv(1024)
        print(f'data: {data}')
        op, args = json.loads(box.decrypt(data))
        print(f'op: {op}')
        if op == 'key':
            key = PublicKey(args['key'], Base64Encoder)
            print(key, type(key))
        else:
            print(args)

def request_signup(username):
    with socket.socket() as s:
        s.connect(("127.0.0.1", 7513))
        key = pkey.encode(Base64Encoder).decode()
        payload = json.dumps(['signup', dict(username=username, key=key)]).encode('utf-8')
        box = Box(skey, vault_pkey)
        msg = box.encrypt(payload)
        s.sendall(SealedBox(vault_pkey).encrypt(pkey.encode()))
        s.sendall(msg)
        data = s.recv(1024)
        print(f'data: {data}')
        op, args = json.loads(box.decrypt(data))
        print(f'op: {op} args: {args}')

request_key('alice')
