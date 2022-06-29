from database import Database, User
import base64
import re

class AuthCtrl:

    def __init__(self, db):
        self.db: Database = db
    
    def is_username_valid(self, username: str):
        return bool(re.match(r'^[-_.a-zA-Z0-9]{1,32}$', username))
    
    def add_user(self, username: str, key: bytes):
        return self.db.add_user(username, key)

    def get_user(self, uid: str):
        u = self.db.get_user(uid)
        if u is None:
            return None
        pkey = base64.b64encode(u.public_key).decode()
        return User(u.id, u.username, pkey)