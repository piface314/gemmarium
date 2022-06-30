from datetime import datetime
from model.misc import GemList, SearchResult
from nacl.public import PublicKey

class Trade:

    @staticmethod
    def from_search_result(sr: SearchResult):
        return Trade(sr.id, sr.peername, sr.ip, sr.port, sr.key)
    
    @classmethod
    def empty(cls):
        return Trade("", "", "", 0, None)

    def __init__(self,
                 peerid: str,
                 peername: str,
                 ip: str,
                 port: int,
                 key: PublicKey,
                 unseen: bool = False,
                 last_update_at: datetime = None,
                 self_accepted: bool = False,
                 peer_accepted: bool = False,
                 self_fusion: bool = False,
                 peer_fusion: bool = False,
                 self_gems: GemList = None,
                 peer_gems: GemList = None):
        self.peerid = peerid
        self.peername = peername
        self.ip = ip
        self.port = port
        self.key = key
        self.unseen = unseen
        self.last_update_at = datetime.now() if last_update_at is None else last_update_at
        self.self_accepted = self_accepted
        self.peer_accepted = peer_accepted
        self.self_fusion = self_fusion
        self.peer_fusion = peer_fusion
        self.self_gems = GemList(set(), set()) if self_gems is None else self_gems
        self.peer_gems = GemList(set(), set()) if peer_gems is None else peer_gems

    def copy(self):
        return Trade(self.peerid, self.peername, self.ip, self.port,
                self.key, self.unseen, self.last_update_at,
                self.self_accepted, self.peer_accepted,
                self.self_fusion,self.peer_fusion, 
                self.self_gems, self.peer_gems)

    def __repr__(self):
        addr = f', {self.ip}:{self.port}'
        unseen = ", unseen" if self.unseen else ""
        acc = f', accepted={"T" if self.self_accepted else "F"}{"T" if self.peer_accepted else "F"}'
        fus = f', fusion={"T" if self.self_fusion else "F"}{"T" if self.peer_fusion else "F"}'
        gl = GemList(self.self_gems.wanted, [f"*{g.name}" for g in self.self_gems.offered])
        gems = f', self_gems={gl}, peer_gems={self.peer_gems}'
        return f'Trade(peerid={self.peerid}, peername={self.peername}{addr}{unseen}, last_update_at={self.last_update_at}{acc}{fus}{gems})'