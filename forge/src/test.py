from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.signing import VerifyKey, SigningKey
from nacl.encoding import Base64Encoder
import json
import socket
from database import Database
from forge_ctrl import ForgeCtrl, FusionRequest
import keys

skey = PrivateKey(b't\x05\xb3\xd4\x199b*Q\xb4\t\x9eC_az@\xf4#y\xbbD\xe4\xe1$\x942\x89\xe0-\xbd\xe7')
pkey = PublicKey(b'\xc1\x8a\xe8D1\xb9Q:\xcf\x88o\x1b\x8f\xea\xad\nv4\xce\xa2\xf0J\xcb\xa5\x9b\x0b\xa6\x80_$\xbds')

forge_pkey = PublicKey(keys.forge_pkey)
forge_vkey = VerifyKey(keys.forge_vkey)
forge_signkey = SigningKey(keys.forge_sign_key)

def request(id):
    with socket.socket() as s:
        s.connect(("127.0.0.1", 7514))
        payload = json.dumps(['request', dict(id=id)]).encode('utf-8')
        box = Box(skey, forge_pkey)
        msg = box.encrypt(payload)
        s.sendall(SealedBox(forge_pkey).encrypt(pkey.encode()))
        s.sendall(box.encrypt(len(msg).to_bytes(4, 'little')))
        s.sendall(msg)
        data = s.recv(1024)
        op, args = json.loads(box.decrypt(data))
        if op != 'auth':
            print(f"!!! {op}, {args}")
            return
        print(f"It's a secret: {args['secret']}")
        msg = json.dumps([op, {'secret': args['secret']}]).encode('utf-8')
        s.sendall(box.encrypt(msg))
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

def find_fusion():
    db = Database()
    ctrl = ForgeCtrl(10, db, forge_signkey, forge_vkey)
    gems_a = [{'tag': 'alexandrite'}, {'tag': 'sapphire'}]
    gems_b = [{'tag': 'rose-quartz'}, {'tag': 'ruby'}]
    req = FusionRequest()
    req.user_a = 'alice'
    req.user_b = 'bob'
    req.gems_a = gems_a
    req.gems_b = gems_b
    print(ctrl.fuse(req))
    

# request('322d85b6-2188-4494-aba1-be9519c5f729')
find_fusion()