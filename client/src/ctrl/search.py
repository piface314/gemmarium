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
        results = [self.matches_query(sr, query, owned) for sr in results]
        return sorted(results, key=lambda sr: (not sr.matches, sr.peername))
        
    def matches_query(self, sr: SearchResult, query: str, owned: bool):
        query = query.strip().lower()
        match = False
        if query:
            for name in sr.gems.offered if owned else sr.gems.wanted:
                if query in name.strip().lower():
                    match = True
                    break
        return SearchResult(sr.id, sr.peername, sr.ip, sr.port, sr.key, sr.gems, match)
        