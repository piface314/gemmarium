from model.misc import GemList
from nacl.public import PrivateKey
from network.search import SearchEndpoint
from sys import argv

if __name__ == '__main__':
    skey = PrivateKey.generate()
    pkey = skey.public_key
    if argv[1] == '1':
        endp = SearchEndpoint(None, 7520, None)
        endp.set_username("alice")
        endp.set_keys(skey, pkey)
        endp.sync_gallery(GemList(['Ruby', 'Sapphire'], ['Amethyst', 'Pearl']))
        endp.local_search(lambda s: print(f'Found: {s}'))
    else:
        endp = SearchEndpoint(None, 7525, None)
        endp.set_username("bob")
        endp.set_keys(skey, pkey)
        endp.sync_gallery(GemList(['Pearl', 'Rose Quartz'], ['Sapphire']))
        endp.listen()