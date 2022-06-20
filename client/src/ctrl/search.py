from network.search import SearchEndpoint


class SearchCtrl:

    def __init__(self, search_endp: SearchEndpoint):
        self.__search_endp = search_endp

    def search(self, query, owned, is_local):
        return []