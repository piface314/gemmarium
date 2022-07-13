from database import Database, User
from datetime import datetime, timedelta
from nacl.secret import SecretBox
from nacl.public import PrivateKey, PublicKey, SealedBox, Box
from nacl.exceptions import CryptoError
from random import randint
import json
import re


class AuthCtrl:

    def __init__(self, db, auth_key: bytes, skey: PrivateKey):
        self.db: Database = db
        self.box = SecretBox(auth_key)
        self.private_key = skey
    
    def is_username_valid(self, username: str):
        return bool(re.match(r'^[-_.a-zA-Z0-9]{1,32}$', username))
    
    def add_user(self, username: str, key: bytes):
        return self.db.add_user(username, key)

    def get_user(self, uid: str):
        return self.db.get_user(uid)

    def get_secret(self, pkey: PublicKey):
        box = SealedBox(pkey)
        secret = randint(0, (1 << 32) - 1).to_bytes(4, 'big')
        return secret, box.encrypt(secret)

    def chk_secret(self, ref: bytes, enc: bytes, pkey: PublicKey):
        box = Box(self.private_key, pkey)
        try:
            return ref == box.decrypt(enc)
        except CryptoError:
            return False

    def get_token(self, u: User):
        token = json.dumps({
            'id': u.id,
            'username': u.username,
            'expire': str(datetime.now() + timedelta(minutes=3))
        })
        return self.box.encrypt(token.encode())