from model import Model
from datetime import datetime
import threading


class Gem(Model):

    __lock = threading.Lock()

    @classmethod
    def load_all(cls):
        db = cls.connect()
        gems = {row[0]: cls.__from_row(row)
            for row in db.execute('SELECT * FROM gem')}
        return gems

    @classmethod
    def __from_row(cls, row):
        (gem_id, name, desc, sprite, created_by, created_for,
            created_at, obtained_at, offered, payload) = row
        return Gem(
            gem_id, name, desc, sprite, created_by, created_for,
            datetime.fromisoformat(created_at),
            datetime.fromisoformat(obtained_at),
            bool(offered), payload
        )

    def __init__(self,
                 gem_id: str,
                 name: str,
                 desc: str,
                 sprite: bytes,
                 created_for: str,
                 created_by: str,
                 created_at: datetime,
                 obtained_at: datetime,
                 is_public: bool,
                 payload: bytes
                 ):
        self.id = gem_id
        self.name = name
        self.desc = desc
        self.sprite = sprite
        self.created_for = created_for
        self.created_by = created_by
        self.created_at = created_at
        self.obtained_at = obtained_at
        self.is_public = is_public
        self.payload = payload
    
    def save(self):
        db = self.connect()
        data = (self.id, self.name, self.desc, self.sprite,
            self.created_for, self.created_by, self.created_at,
            self.obtained_at, self.is_public, self.payload)
        n = len(data)-1
        with self.__lock:
            db.execute(f'REPLACE INTO gem VALUES (?{", ?"*n})', data)
            db.commit()
        db.close()
