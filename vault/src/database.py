from collections import namedtuple
import sqlite3
import threading
import uuid


User = namedtuple('User', ['id', 'username', 'public_key'])


class Database:

    def __init__(self):
        db = self.__connect()
        self.__lock = threading.Lock()
        with open('res/create.sql') as f:
            sql = f.read()
            db.executescript(sql)
            db.commit()
    
    def __connect(self):
        return sqlite3.connect('vault.db')

    def add_user(self, username, public_key):
        db = self.__connect()
        u = User(str(uuid.uuid4()), username, public_key)
        with self.__lock:
            try:
                db.execute('INSERT INTO user VALUES (?, ?, ?)', u)
                db.commit()
                db.close()
                return u
            except sqlite3.IntegrityError:
                return None
            finally:
                db.close()

    def get_user(self, uid: str):
        db = self.__connect()
        c = db.execute('SELECT * FROM user WHERE id = ?', (uid,))
        u = c.fetchone()
        db.close()
        return None if u is None else User(*u)
