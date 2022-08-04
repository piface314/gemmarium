from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.encoding import Base64Encoder
import keys
import requests

skey = PrivateKey.generate()
pkey = skey.public_key

skey2 = PrivateKey(b't\x05\xb3\xd4\x199b*Q\xb4\t\x9eC_az@\xf4#y\xbbD\xe4\xe1$\x942\x89\xe0-\xbd\xe7')
pkey2 = PublicKey(b'\xc1\x8a\xe8D1\xb9Q:\xcf\x88o\x1b\x8f\xea\xad\nv4\xce\xa2\xf0J\xcb\xa5\x9b\x0b\xa6\x80_$\xbds')

print(f'PrivateKey: {skey}')
print(f'PublicKey: {pkey}')

vault_pkey = PublicKey(keys.vault_pkey)

def request_auth(uid):
    res = requests.get('http://127.0.0.1:7513/auth', params=dict(id=uid))
    print(res)
    secret = res.json()['secret']
    secret = SealedBox(skey2).decrypt(secret, Base64Encoder)
    secret = Box(skey2, vault_pkey).encrypt(secret, encoder=Base64Encoder).decode()
    res2 = requests.post('http://127.0.0.1:7513/auth', params=dict(id=uid), json=dict(
        secret = secret
    ))
    print(res2)
    print(res2.json())

def request_signup(username):
    res = requests.post('http://127.0.0.1:7513/signup', json=
        dict(username=username, key=pkey.encode(Base64Encoder).decode()))
    print(res)
    print(res.json())


request_auth('322d85b6-2188-4494-aba1-be9519c5f729')
# request_signup('bob')
