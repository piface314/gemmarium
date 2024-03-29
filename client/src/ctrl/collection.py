from ctrl.profile import ProfileCtrl
from datetime import datetime
from exceptions import InvalidGemError
from model.gem import Gem
from model.misc import GemList
from model.wanted import Wanted
from network.collection import CollectionEndpoint
from network.search import SearchEndpoint
from nacl.encoding import Base64Encoder
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
import json

class CollectionCtrl:

    def __init__(self,
                 col_endp: CollectionEndpoint, search_endp: SearchEndpoint,
                 forge_vkey: VerifyKey):
        self.__collection_endp = col_endp
        self.__search_endp = search_endp
        self.__gems = {}
        self.__verify_key = forge_vkey
        self.__wanted: Wanted = None

    def load(self):
        self.__gems = Gem.load_all()
        self.__wanted = Wanted.load()
    
    def set_identity(self, id, username):
        self.__id = id
        self.__username = username

    def list_gems(self):
        gems = sorted(self.__gems.values(), key=lambda g: g.name)
        return sorted(gems, key=lambda g: g.obtained_at, reverse=True)

    def set_visibility(self, gem: Gem, is_public: bool):
        gem.is_public = is_public
        gem.save()

    def add_wanted(self, gem):
        self.__wanted.add(gem)

    def remove_wanted(self, gem):
        self.__wanted.remove(gem)

    def list_wanted(self):
        return sorted(self.__wanted.gems)
    
    def get_gallery(self):
        offered = [gem for gem in self.__gems.values() if gem.is_public]
        return GemList(self.list_wanted(), offered)

    def sync_gallery(self):
        gl = self.get_gallery()
        gl = GemList(gl.wanted, [g.name for g in gl.offered])
        self.__search_endp.sync_gallery(gl)

    def add_gem(self, gem: Gem):
        gem.save()
        self.__gems[gem.id] = gem
    
    def remove_gem(self, gem: Gem):
        gem.delete()
        self.__gems.pop(gem.id, None)

    def request_gem(self):
        uid = self.__id
        gem_raw = self.__collection_endp.request_gem(uid)
        gem = self.new_gem(gem_raw)
        self.add_gem(gem)
        return gem

    def new_gem(self, gem_raw: str):
        vkey = self.__verify_key
        try:
            gem_bytes = vkey.verify(gem_raw, encoder=Base64Encoder)
        except BadSignatureError:
            raise InvalidGemError()
        gem = json.loads(gem_bytes)
        return Gem(gem['id'], gem['name'], gem['desc'],
            Base64Encoder.decode(gem['sprite']), gem['created_for'], gem['created_by'],
            datetime.fromisoformat(gem['created_at']), datetime.now(),
            False, gem_raw)
