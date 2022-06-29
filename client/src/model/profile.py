from datetime import datetime
from model import Model
from nacl.public import PublicKey, PrivateKey
import threading


class Profile(Model):

    __lock = threading.Lock()

    @classmethod
    def load(cls):
        db = cls.connect()
        c = db.execute('SELECT * FROM `profile`')
        data = c.fetchone()
        if data is None:
            skey = PrivateKey.generate()
            pkey = skey.public_key
            p = Profile(None, None, pkey, skey, None)
            p.save()
            return p
        else:
            id, username, pkey, skey, last_sync = data
            last_sync = None if last_sync is None else datetime.fromisoformat(last_sync)
            return Profile(id, username, PublicKey(pkey), PrivateKey(skey), last_sync)


    def __init__(self, id: str, username: str, pkey: PublicKey, skey: PrivateKey, last_sync: datetime):
        self.id = id
        self.username = username
        self.public_key = pkey
        self.private_key = skey
        self.last_sync_at = last_sync

    def save(self):
        data = (
            self.id,
            self.username,
            self.public_key._public_key,
            self.private_key._private_key,
            self.last_sync_at
        )
        db = self.connect()
        with self.__lock:
            db.execute('DELETE FROM `profile`')
            db.execute('INSERT INTO `profile` VALUES (?, ?, ?, ?, ?)', data)
            db.commit()
        db.close()
