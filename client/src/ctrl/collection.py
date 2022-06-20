from model.gem import Gem
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
        self.__wanted = set()

    def load(self):
        pass

    def list_gems(self):
        pass

    def set_visibility(self, gem, is_public):
        pass

    def add_wanted(self, gem):
        self.wanted.add(gem)

    def remove_wanted(self, gem):
        self.wanted.remove(gem)

    def list_wanted(self):
        return sorted(self.wanted)

    def sync_gallery(self):
        pass

    def add_gem(self, gem):
        pass

    def request_gem(self):
        pass
