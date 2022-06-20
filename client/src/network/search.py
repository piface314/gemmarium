from nacl.public import PrivateKey, PublicKey
from model.misc import GemList, SearchResult


class SearchEndpoint:

    def __init__(self, gallery_key: PublicKey):
        self.__gallery_key = gallery_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey
    
    def listen(self):
        pass
    
    def reply(self):
        pass
    
    def local_search(self):
        return []

    def global_search(self, query: str, owned: bool):
        pass
    
    def sync_gallery(self, gems: GemList):
        self.__gallery = gems
