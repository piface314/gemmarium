from datetime import datetime
from model.misc import GemList, SearchResult
from nacl.public import PublicKey

class Trade:

    @staticmethod
    def from_search_result(sr: SearchResult):
        return Trade(sr.peername, sr.ip, sr.port, sr.key)

    def __init__(self,
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
    
    def add_gem(self, from_self: bool, offered: bool, gem: str):
        g = self.self_gems if from_self else self.peer_gems
        g[offered].add(gem)

    def remove_gem(self, from_self: bool, offered: bool, gem: str):
        g = self.self_gems if from_self else self.peer_gems
        g[offered].remove(gem)

    