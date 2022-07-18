from database import Database, User
from datetime import datetime, timedelta
from nacl.exceptions import CryptoError
from nacl.public import PrivateKey, PublicKey, SealedBox, Box
from nacl.signing import SigningKey
from nacl.utils import random
import json
import re


class AuthCtrl:

    def __init__(self, db: Database, sign_key: SigningKey, skey: PrivateKey):
        self.db = db
        self.sign_key = sign_key
        self.private_key = skey
    
    def is_username_valid(self, username: str):
        return bool(re.match(r'^[-_.a-zA-Z0-9]{1,32}$', username))
    
    def add_user(self, username: str, key: bytes):
        return self.db.add_user(username, key)

    def get_user(self, uid: str):
        return self.db.get_user(uid)

    def get_secret(self, pkey: PublicKey):
        box = SealedBox(pkey)
        secret = random(32)
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
            'expire': str(datetime.now() + timedelta(minutes=1))
        })
        return self.sign_key.sign(token.encode())