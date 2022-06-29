from collections import namedtuple
from datetime import datetime
import sqlite3
import threading

Quota = namedtuple('Quota', ['id', 'last_request_at'])


class Database:

    def __init__(self):
        self.__lock = threading.Lock()
        db = self.__connect()
        with open('res/create.sql') as f:
            sql = f.read()
            db.executescript(sql)
            db.commit()

    def __connect(self):
        return sqlite3.connect('forge.db')

    def set_quota(self, uid, last_request_at):
        with self.__lock:
            db = self.__connect()
            db.execute('REPLACE INTO quota VALUES (?, ?)',
                       (uid, last_request_at))
            db.commit()
            db.close()

    def get_quota(self, uid):
        db = self.__connect()
        c = db.execute('SELECT * FROM quota WHERE id = ?', (uid,))
        q = c.fetchone()
        db.close()
        return None if q is None else Quota(q[0], datetime.fromisoformat(q[1]))