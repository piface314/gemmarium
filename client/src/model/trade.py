from model.misc import GemList
from model import Model



class Trade(Model):

    def __init__(self,
                 peername,
                 ip,
                 port,
                 key,
                 unseen,
                 last_update_at,
                 self_accepted,
                 peer_accepted,
                 self_fusion,
                 peer_fusion,
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
