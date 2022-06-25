from datetime import datetime
import sqlite3
from model.misc import GemList
from model import Model
from nacl.public import PublicKey
import threading


class Trade(Model):

    __lock = threading.Lock()

    @classmethod
    def load_all(cls):
        db = cls.connect()
        trades = {row[0]: cls.__from_row(row, db)
            for row in db.execute('SELECT * FROM trade')}
        for peername, lists in cls.__load_gem_lists(db):
            trades[peername].peer_gems = GemList(lists[0], lists[1])
            trades[peername].self_gems = GemList(lists[2], lists[3])
        return trades

    @classmethod
    def __from_row(cls, row):
        (peername, ip, port, key, unseen, last_update_at,
            self_accepted, peer_accepted, self_fusion, peer_fusion) = row
        return Trade(peername, ip, port, key, bool(unseen),
            datetime.fromisoformat(last_update_at),
            bool(self_accepted),
            bool(peer_accepted),
            bool(self_fusion),
            bool(peer_fusion),
            None, None
        )

    @classmethod
    def __load_gem_lists(cls, db: sqlite3.Connection):
        lists = {}
        for row in db.execute('SELECT * FROM trade_state'):
            peername, from_self, offered, gem = row
            if peername not in lists:
                lists[peername] = (set(), set(), set(), set())
            lists[peername][from_self*2 + offered].add(gem)
        return lists

    def __init__(self,
                 peername: str,
                 ip: str,
                 port: int,
                 key: PublicKey,
                 unseen: bool,
                 last_update_at: datetime,
                 self_accepted: bool,
                 peer_accepted: bool,
                 self_fusion: bool,
                 peer_fusion: bool,
                 self_gems: GemList,
                 peer_gems: GemList):
        self.peername = peername
        self.ip = ip
        self.port = port
        self.key = key
        self.unseen = unseen
        self.last_update_at = last_update_at
        self.self_accepted = self_accepted
        self.peer_accepted = peer_accepted
        self.self_fusion = self_fusion
        self.peer_fusion = peer_fusion
        self.self_gems = self_gems
        self.peer_gems = peer_gems

    def save(self, with_lists: bool = False):
        db = self.connect()
        trade = (self.peername, self.ip, self.port, self.key, self.unseen,
            self.last_update_at, self.self_accepted, self.peer_accepted,
            self.self_fusion, self.peer_fusion)
        n = len(trade)-1
        if with_lists:
            trade_state = (
                [(self.peername, False, False, gem) for gem in self.peer_gems.wanted]
                + [(self.peername, False, True, gem) for gem in self.peer_gems.offered]
                + [(self.peername, True, False, gem) for gem in self.self_gems.wanted]
                + [(self.peername, True, True, gem) for gem in self.self_gems.offered])
        with self.__lock:
            db.execute(f'REPLACE INTO trade VALUES (?{", ?"*n})', trade)
            if with_lists:
                db.executemany('REPLACE INTO trade_state VALUES (?, ?, ?, ?)', trade_state)
            db.commit()
        db.close()
    
    def add_gem(self, from_self: bool, offered: bool, gem: str):
        g = self.self_gems if from_self else self.peer_gems
        g[offered].add(gem)
        data = (self.peername, from_self, offered, gem)
        db = self.connect()
        with self.__lock:
            db.execute('REPLACE INTO trade_state VALUES (?, ?, ?, ?)', data)
            db.commit()
        db.close()

    def remove_gem(self, from_self: bool, offered: bool, gem: str):
        g = self.self_gems if from_self else self.peer_gems
        g[offered].remove(gem)
        data = (self.peername, from_self, offered, gem)
        db = self.connect()
        with self.__lock:
            db.execute('''
            DELETE FROM trade_state
            WHERE peername=? AND from_self=? AND offered=? AND gem=?
            ''', data)
            db.commit()
        db.close()

    