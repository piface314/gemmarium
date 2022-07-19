from model.misc import GemList, SearchResult
from nacl.public import PublicKey, SealedBox
from network.endpoint import Endpoint
from time import time
import json
import socket
import threading
import traceback


class SearchEndpoint(Endpoint):

    def __init__(self, search_port: int, gallery_addr, offset: int = 0):
        self.__search_port = search_port
        self.__trade_port = 0
        self.__gallery_addr = gallery_addr
        self.__gallery = GemList([], [])
        self.__lock = threading.Lock()
        self.__offset = offset
    
    def set_trade_port(self, port: int):
        self.__trade_port = port

    def sync_gallery(self, gems: GemList):
        self.__gallery = gems
    
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("", self.__search_port))
            while True:
                try:
                    print("SearchEndpoint: Listening...")
                    data, addr = s.recvfrom(1024)
                    print(f"SearchEndpoint: datagram from {addr}...")
                    pkey_raw, data = data[:32], data[32:]
                    pkey = PublicKey(pkey_raw)
                    op, args = json.loads(data)
                    if op != 'search' or args['id'] == self.uid:
                        continue
                    print(f"SearchEndpoint: sending gallery to {addr}...")
                    reply = self.enc_msg(pkey, 'gallery',
                        id=self.uid,
                        username=self.username,
                        port=self.__trade_port,
                        wanted=self.__gallery.wanted,
                        offered=self.__gallery.offered
                    )
                    box = SealedBox(pkey)
                    my_pkey = box.encrypt(self.public_key.encode())
                    s.sendto(my_pkey + reply, addr)
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
    
    def local_search(self, wait=1):
        results = []
        msg = self.public_key.encode() + json.dumps(['search', dict(id=self.uid)]).encode()
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        ips = {ip[-1][0] for ip in interfaces}
        ips.add("")
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
        s.sendto(msg, ("255.255.255.255", self.__search_port + self.__offset))
        t0 = time()
        while time() - t0 <= wait:
            try:
                s.settimeout(wait)
                data, addr = s.recvfrom(16384)
                pkey_raw, data = data[:80], data[80:]
                pkey = PublicKey(SealedBox(self.private_key).decrypt(pkey_raw))
                op, args = self.dec_msg(pkey, data)
                if op != 'gallery':
                    continue
                gl = GemList(args['wanted'], args['offered'])
                res = SearchResult(args['id'], args['username'], addr[0], args['port'], pkey, gl, False)
                with self.__lock:
                    results.append(res)
                wait += 0.2
            except Exception as e:
                pass
        s.close()

    def global_search(self, query: str, owned: bool):
        return []

