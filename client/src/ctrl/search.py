from model.misc import SearchResult, GemList
from network.search import SearchEndpoint


class SearchCtrl:

    def __init__(self, search_endp: SearchEndpoint):
        self.__search_endp = search_endp

    def search(self, query: str, owned: bool, is_local: bool = True, wait: int = 1):
        if is_local:
            results = self.__search_endp.local_search(wait=wait)
        else:
            results = self.__search_endp.global_search(query, owned)
        return sorted(results, key=lambda res: (
            query.lower() not in ','.join(res.gems.offered if owned else res.gems.wanted).lower(),
            res.peername
            ))
        