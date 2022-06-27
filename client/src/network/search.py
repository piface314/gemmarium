from model.misc import GemList, SearchResult
from nacl.public import PrivateKey, PublicKey, Box
from time import time
import json
import socket
import threading


class SearchEndpoint:

    # apenas para fins de teste
    OFFSET = 5

    def __init__(self, gallery_addr, search_port: int, gallery_key: PublicKey):
        self.__gallery_addr = gallery_addr
        self.__search_port = search_port
        self.__gallery_key = gallery_key
        self.__gallery = GemList([], [])
        self.__username = ""
        self.__lock = threading.Lock()

    def set_username(self, username: str):
        self.__username = username

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey
    
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("", self.__search_port))
            while True:
                print("SearchEndpoint: Listening...")
                data, addr = s.recvfrom(42)
                if data[:10] != b'gemsearch?':
                    continue
                pkey = PublicKey(data[10:])
                reply = (self.__username,) + self.__gallery
                reply = json.dumps(reply).encode('utf-8')
                reply = Box(self.__private_key, pkey).encrypt(reply)
                print(f"SearchEndpoint: sending gallery to {addr}...")
                s.sendto(self.__public_key.encode() + reply, addr)
    
    def local_search(self, wait=1):
        results: list[SearchResult] = []
        msg = b'gemsearch?' + self.__public_key.encode()
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        ips = {ip[-1][0] for ip in interfaces}
        workers = [threading.Thread(target=self.__local_search_request, args=(ip, wait, msg, results))
            for ip in ips]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
        return results

        
    def __local_search_request(self, ip, wait, msg, results):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((ip, 0))
        s.sendto(msg, ("255.255.255.255", self.__search_port + self.OFFSET))
        t0 = time()
        while time() - t0 <= wait:
            try:
                s.settimeout(wait)
                data, addr = s.recvfrom(16384)
                skey = self.__private_key
                pkey = PublicKey(data[:32])
                reply = Box(skey, pkey).decrypt(data[32:])
                reply = json.loads(reply.decode('utf-8'))
                peername, wanted, offered = reply
                gl = GemList(wanted, offered)
                res = SearchResult(peername, addr[0], addr[1], pkey, gl)
                with self.__lock:
                    results.append(res)
                wait += 0.2
            except Exception as e:
                print(f'SearchEndpoint: {e}')
                pass
        s.close()

    def global_search(self, query: str, owned: bool):
        return []
    
    def sync_gallery(self, gems: GemList):
        self.__gallery = gems
