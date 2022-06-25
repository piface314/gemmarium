from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder
import json
import socket
import src.keys

skey = PrivateKey(b't\x05\xb3\xd4\x199b*Q\xb4\t\x9eC_az@\xf4#y\xbbD\xe4\xe1$\x942\x89\xe0-\xbd\xe7')
pkey = PublicKey(b'\xc1\x8a\xe8D1\xb9Q:\xcf\x88o\x1b\x8f\xea\xad\nv4\xce\xa2\xf0J\xcb\xa5\x9b\x0b\xa6\x80_$\xbds')

forge_pkey = PublicKey(src.keys.forge_pkey)
forge_vkey = VerifyKey(src.keys.forge_vkey)

def request(username):
    with socket.socket() as s:
        s.connect(("127.0.0.1", 7514))
        payload = json.dumps(['request', dict(username=username)]).encode('utf-8')
        box = Box(skey, forge_pkey)
        msg = box.encrypt(payload)
        s.sendall(SealedBox(forge_pkey).encrypt(pkey.encode()))
        s.sendall(msg)
        data = s.recv(4096)
        print(f'len(data): {len(data)}')
        op, args = json.loads(box.decrypt(data))
        print(f'op: {op}')
        if op == 'gem':
            gem_raw = args['gem']
            print(f'raw: {gem_raw}')
            gem_bytes = forge_vkey.verify(gem_raw, encoder=Base64Encoder)
            gem = json.loads(gem_bytes)
            print(f'gem: {gem}')
        else:
            print(args)

request('tuershen')
