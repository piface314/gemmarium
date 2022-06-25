from exceptions import QuotaError, InvalidGemError
from model.gem import Gem
from model.misc import GemList
from model.wanted import Wanted
from ctrl.profile import ProfileCtrl
from network.collection import CollectionEndpoint
from network.search import SearchEndpoint

class CollectionCtrl:

    def __init__(self, profile_ctrl: ProfileCtrl,
                 col_endp: CollectionEndpoint, search_endp: SearchEndpoint):
        self.__profile_ctrl = profile_ctrl
        self.__collection_endp = col_endp
        self.__search_endp = search_endp
        self.__gems = {}
        self.__wanted: Wanted = None

    def load(self):
        self.__gems = Gem.load_all()
        self.__wanted = Wanted.load()

    def list_gems(self):
        return sorted(self.__gems.values(),
            key=lambda g: (g.name, g.obtained_at))

    def set_visibility(self, gem: Gem, is_public: bool):
        gem.is_public = is_public
        gem.save()

    def add_wanted(self, gem):
        self.__wanted.add(gem)

    def remove_wanted(self, gem):
        self.__wanted.remove(gem)

    def list_wanted(self):
        return sorted(self.__wanted.gems)

    def sync_gallery(self):
        offered = [gem.name for gem in self.__gems.values()]
        gl = GemList(self.list_wanted(), offered)
        self.__search_endp.sync_gallery(gl)

    def add_gem(self, gem: Gem):
        self.__gems[gem.id] = gem
        gem.save()

    def request_gem(self):
        username = self.__profile_ctrl.get_username()
        gem = self.__collection_endp.request_gem(username)
        self.add_gem(gem)
        return gem

