import uuid
from ctrl.trade import TradeCtrl
from ctrl.collection import CollectionCtrl
from model.misc import GemList, SearchResult
from model.trade import Trade
from nacl.public import PrivateKey
from network.search import SearchEndpoint
from network.trade import TradeEndpoint, TradeEvent
from sys import argv
import threading
from time import sleep

from collections import namedtuple
Gem = namedtuple('Gem', ["name", "payload"])

gems_a = [
    Gem("GemA", "HOpoIZZb0fSDafU5gef0k7TRyGEB6QA0ctaHr0aLYuqHFcwOp3GiUuidqhGqzXrZUTsM1vCr1uYwtrzr69vVD3siaWQiOiAiZTAzMmM2ZjAtYjkzOS00ZjMwLWI2YTEtNjEzNTdjMDNhMGI4IiwgInRhZyI6ICJqYWRlIiwgIm5hbWUiOiAiSmFkZSIsICJkZXNjIjogIiAiLCAic3ByaXRlIjogImlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFJQUFBQUFRQ0FNQUFBRHBob2U2QUFBQU1GQk1WRVVBQUFBQUFBQUFPQ29BY3prQW8xd0FBQUFBQUFBQUFBRC8vLysxLytOTi83SUF4M3NBQUFBQUFBQUFBQUFBQUFEbWEyRmdBQUFBRUhSU1RsTUEvLy8vLy8vLy8vLy8vLy8vLy8vL3dGQ0xRd0FBQVVsSlJFRlVTSW5GbGNGeXhDQU1RelBBUWVELy85KzFReExMNm5aUG5TMm5QR3dKQlRMa09NN1JmQncwdnM3V3U5Rk1nNC8yb2Y3WDNHME02ODlNZzdEWEl4RzRQeEtDOVhCQzhZUDRLMU9nc1h5R0FteEcxbkd1Z093SEtrZWd3aU1ZekxXZi9mdWFjNDExUjJvUTdnc25JL3VCNE8yNDlRaG12MmZCbTFrZmZzOGh0ejZIemJYc0NTRGNKNFFIZ2tGNllOMW5zdjE4aXhyWUg2d1B2d3dRSitJenVRUENCbUYvdThyeHVvWE5sQ2VFT1lBdk1PZklIUkRXdXNYNnRRNW9QMVFQOWFzQmJJN09BWmkxSGdHa0hnRnFQMVFQOWFOdjRId2pPZ0pocmI5aEQxRHJmQ1M3SDZvdkFYeEgrQWdxU3gyRnNhK3RyT1BzaCtyeHc0OENSS1RSTTBEbHdHUi9MdXdUVlg4MXNQN2NrdlMvK3ZPdWJWdHdNeXBqancvY21PUEtWUDFiZjdycm04Vm5SVmR2WlZSR3JjY0ZET21QUUwvenBkZWZUZjhteTgvdVAzL0hML0tsR2s4WmRRUjdBQUFBQUVsRlRrU3VRbUNDIiwgImNyZWF0ZWRfYnkiOiAiVGhlIEZvcmdlIiwgImNyZWF0ZWRfZm9yIjogInBpZmFjZTMxNCIsICJjcmVhdGVkX2F0IjogIjIwMjItMDYtMjYgMTk6MjA6NTQuMjYwNDY1In0="),
    Gem("GemB","mAhmrXpm5CzpeyMztn4rtWwMnS2UAku9p/KtWOSczHg8YYU6MV2VIE9qunkutsxTmLfTK6mcvF6Q0lyt4IX9DHsiaWQiOiAiNGQzMWVjNDMtZGRmZS00ZTVlLWE4MzEtOGFjZTBlMGEzOTY3IiwgInRhZyI6ICJzYXBwaGlyZSIsICJuYW1lIjogIlNhZmlyYSIsICJkZXNjIjogIiAiLCAic3ByaXRlIjogImlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFJQUFBQUFRQ0FNQUFBRHBob2U2QUFBQU1GQk1WRVVBQUFBQUFBQUFBRFVBQUlBQUFJd0FBQUFBQUFBQUFBRC8vLzk5b3Y4bUp2OEFBQUFBQUFBQUFBQUFBQUFBQUFDWUg3NVlBQUFBRUhSU1RsTUEvLy8vLy8vLy8vLy8vLy8vLy8vL3dGQ0xRd0FBQVBOSlJFRlVTSW5ObGMwV2hTQUloQlUzaysvL3dJR0dDYVkzVjExV2ZjendjenhsSWZ4RlVJa3YrWkNnT1FQQ01Eb293UGlaWU9yaCtubHUvVE5SU29sd1pmaWhNcHgrSlNyRHNkY0xZNjIzQlZMa3dMMkFZOVhoV1FjMDl2cTYvdTVQbEROcGh1ZGJ6cktzWmE4cnd6SisrZHNDTWFYY0d6eGoxTEh5NzdLY2lXYWVHS1BPWnpMMzczQ2dJMm9pUm5yTHdKNS96cHBKa1dKK3pUeC8wTEZSMzNOSnlFdlJHNVlNWHVCbUVOOElyRU1Yd0dhL2tpa3hZeGptZDl2cWxkdDhNYXpxeC82Y2tJdUJ0Mm9GaGlHZkZ5eGIzZmpSR005KzM3OThDQkkwWTVuZk1hcU9pK1VDOXY0MUQvTysveGw5R1NjTVF4U0VjU0tTaGdBQUFBQkpSVTVFcmtKZ2dnPT0iLCAiY3JlYXRlZF9ieSI6ICJUaGUgRm9yZ2UiLCAiY3JlYXRlZF9mb3IiOiAicGlmYWNlMzE0IiwgImNyZWF0ZWRfYXQiOiAiMjAyMi0wNi0yNiAxOToyMTowNi42MDM2NjEifQ=="),
]

gems_b = [
    Gem("GemC","xwsATxD3s0JqSEjCDcOUJ0bGOqfJBsg22Q5gxLbwVzWLm7PaFCpvKj8H0CYJiE7+UpahOZOnC67UaItD6LdpBXsiaWQiOiAiNjFhOGEyMDctOGZmZS00OWUyLTg0OTAtNDk5MTllNTg0Njg3IiwgInRhZyI6ICJnYXJuZXQiLCAibmFtZSI6ICJHcmFuYWRhIiwgImRlc2MiOiAiICIsICJzcHJpdGUiOiAiaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUlBQUFBQVFDQU1BQUFEcGhvZTZBQUFBTUZCTVZFVUFBQUFBQUFBMkFBQTJBQldQQUNFQUFBQUFBQUFBQUFELy8vLy9iSWovS2xvQUFBQUFBQUFBQUFBQUFBQUFBQUFkaGUycUFBQUFFSFJTVGxNQS8vLy8vLy8vLy8vLy8vLy8vLy8vd0ZDTFF3QUFBUXhKUkVGVVNJbk5sVXNTaERBSVJCUElvaWYzUC9CQUZBdzR4bkxsc0h0cFBsMnBpS1g4UmRDSUY1ay9HblRvbVFGbEJCMVVFUEtGRU9xUittWDIvcDI1dGNiWVR3aEV3akxWZEdOTWpNUlpINHkxN2daYWxjQmhJTEhweUd3RG5MTytyai82TS9mT2RpTHppWG9uNTY1bUkyZmRHSkZ4bCs4R2FtdDlUc2lNczQ1Vi9rTm12Uk03VVQwenpycmN5WFgrRXk3MHFXYWdWaHBNOXd3OHk3OW1jOUFxMTI1TXlyUmdtWC9TOGFCKzVtRkFIK0ZzUUI4SlhUSEV3TUVnMlFpaXd3emdyajd4T0JseHhRZ3NienZxRy90OFRWalZuL3ZMZ1M0aXVRVXYwRVVoTHIyaFhubmdxSWQ4T09OM2Z1NC9QZ1FOVHV6TFd1ZFBqRTNIenJxQWMvNmFjLy95L3Mvb3pmZ0NxS0VWSFRoUGpZQUFBQUFBU1VWT1JLNUNZSUk9IiwgImNyZWF0ZWRfYnkiOiAiVGhlIEZvcmdlIiwgImNyZWF0ZWRfZm9yIjogInBpZmFjZTMxNCIsICJjcmVhdGVkX2F0IjogIjIwMjItMDYtMjYgMTk6MjI6NDguNzgxODQ2In0="),
    Gem("GemD","Ovg5EPW9Vs6OwdoOaRPwg+wSodaTOyK4D2cGwIZ3LjjIB9MSZNiFHogSYjUmzRKlPOrcTMhUQoZtGSeK7DseC3siaWQiOiAiYjY3YjU1MzUtMjdiOC00YmI2LWI2OWItNTYwODM0MjlkZTUwIiwgInRhZyI6ICJsYXBpcy1sYXp1bGkiLCAibmFtZSI6ICJMXHUwMGUxcGlzLUxhelx1MDBmYWxpIiwgImRlc2MiOiAiICIsICJzcHJpdGUiOiAiaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUlBQUFBQVFDQU1BQUFEcGhvZTZBQUFBTUZCTVZFVUFBQUFBQUFBQUFDb0FDbUFBQ29rQUFBQUFBQUFBQUFELy8vK3p0ZjlLVC84QUFNZ0FBQUFBQUFBQUFBQUFBQUFwVnFXT0FBQUFFSFJTVGxNQS8vLy8vLy8vLy8vLy8vLy8vLy8vd0ZDTFF3QUFBVTlKUkVGVVNJbkZsY21Td3lBTVJGMFdod2Y4Ly8rTzVBMnBKOGxwRnNxSFBFdmRkR0VDMjNhTTNjZVd4cCt6RGJQMFpzZkgvcUgrMHp6R25HTThiM2FFdlI2SnlQMlJrS3pIaWVLSCtDdXZBTE8zTm5PQWsxbDFXc3pBNm9mS0xRSm1uc0ZrcnYzSjMyeTIxbWMzdXhoaG14ek02b2ZnMC9IVUU1ejluZ2x2enZyd3c1NEFIcWoxRkVEWWZBRXFONEpKZWdoRGxoK1lrZjNKK3ZCYkFVWnZZN1ErVW9EQ0ErSHVINkN3VDBmaE1aUWJ3am1BTi90SDZVOEFZYTJQbUwvV1FmdFJQZXBYQXB4cnZnSVUxcm9IMERwb1A2cEgvZEllT0daTWUwQlk2eTg0QXBTNlA5S1A2aVZBbHdCZERCWlRtTzJhLzY1ekJsQzlCaXFiME5lMDk3a0NWRDcrOFE5RFpYOVI5WGREMGtlZDVYLzFQd0dPaitwNzVqNklxTXc1UHJCbDlwL2Y5Qy85MDFsdnZod2VjSC9EVktiVzR3QkcrbzlBYi9uUzU4dkdGeVVmemIvUGN0bjk1M1g4QmRHTEc3ZklyVUUzQUFBQUFFbEZUa1N1UW1DQyIsICJjcmVhdGVkX2J5IjogIlRoZSBGb3JnZSIsICJjcmVhdGVkX2ZvciI6ICJwaWZhY2UzMTQiLCAiY3JlYXRlZF9hdCI6ICIyMDIyLTA2LTI2IDE5OjIzOjAxLjQ0OTk5NyJ9")
]

id1 = str(uuid.uuid4())
skey = PrivateKey.generate()
pkey = skey.public_key

id2 = str(uuid.uuid4())
skey2 = PrivateKey.generate()
pkey2 = skey2.public_key

alice_gallery = GemList(['Ruby', 'Sapphire'], gems_a)
bob_gallery = GemList(['Pearl', 'Rose Quartz'], gems_b)

def local_search():
    if argv[1] == '1':
        endp = SearchEndpoint(7515, 7516, None, None, 5)
        endp.set_identity(id1, 'alice')
        endp.set_keys(skey, pkey)
        endp.sync_gallery(alice_gallery)
        results = endp.local_search()
        print(results)
    else:
        endp = SearchEndpoint(7520, 7521, None, None, -5)
        endp.set_identity(id2, 'bob')
        endp.set_keys(skey2, pkey2)
        endp.sync_gallery(bob_gallery)
        endp.listen()

def trade():
    class ColCtrl:
        def __init__(self, gl):
            self.gallery = gl
        def get_gallery(self):
            return self.gallery
        def new_gem(self, gem):
            return gem
        def add_gem(self, gem):
            print(f'Gem {str(gem)[:15]} was added')
    def t1():
        endp = TradeEndpoint(int(argv[1]), None, None)
        endp.set_identity(id1, "alice")
        endp.set_keys(skey, pkey)
        sr = SearchResult(id2, 'bob', "127.0.0.1", int(argv[2]), pkey2, bob_gallery)
        ctrl = TradeCtrl(ColCtrl(alice_gallery), endp)
        ctrl.bind(TradeEvent.TRADE, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.UPDATE, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.ACCEPT, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.REJECT, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.FUSION, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.FINISH, lambda trade: print(f'Alice <- Bob: {trade}'))
        ctrl.bind(TradeEvent.GEMS, lambda trade, gems: print(f'Alice <- Bob: GEMSSS {trade}'))
        threading.Thread(target=lambda: endp.listen(), daemon=True).start()
        trade = ctrl.start_trade(sr)
        ctrl.update(trade, GemList(alice_gallery.wanted + ['Garnet'], alice_gallery.offered + gems_a))
        ctrl.accept(trade)
    def t2():
        endp = TradeEndpoint(int(argv[2]), None, None)
        endp.set_identity(id2, "bob")
        endp.set_keys(skey2, pkey2)
        ctrl = TradeCtrl(ColCtrl(bob_gallery), endp)
        trades = [None]
        def cb(trade_):
            trades[0] = trade_
            print(f'Bob <- Alice: {trade_}')
        ctrl.bind(TradeEvent.TRADE, cb)
        ctrl.bind(TradeEvent.UPDATE, cb)
        ctrl.bind(TradeEvent.ACCEPT, cb)
        ctrl.bind(TradeEvent.REJECT, cb)
        ctrl.bind(TradeEvent.FUSION, cb)
        ctrl.bind(TradeEvent.FINISH, cb)
        ctrl.bind(TradeEvent.GEMS, lambda trade, gems: print(f'Bob <- Alice: GEMSSSS {trade}'))
        threading.Thread(target=lambda: endp.listen(), daemon=True).start()
        sleep(3)
        ctrl.update(trades[0], bob_gallery)
        ctrl.accept(trades[0])

    threading.Thread(target=t2).start()
    sleep(2)
    threading.Thread(target=t1).start()


trade()