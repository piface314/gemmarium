from model.misc import GemList
from nacl.public import PrivateKey
from network.search import SearchEndpoint
from network.trade import TradeEndpoint, TradeEvent
from sys import argv
import threading
from time import sleep

from collections import namedtuple
Gem = namedtuple('Gem', ["payload"])
Trade = namedtuple('Trade', ["ip", "port", "key", "self_gems", "peer_gems"])

gems_a = [
    Gem("HOpoIZZb0fSDafU5gef0k7TRyGEB6QA0ctaHr0aLYuqHFcwOp3GiUuidqhGqzXrZUTsM1vCr1uYwtrzr69vVD3siaWQiOiAiZTAzMmM2ZjAtYjkzOS00ZjMwLWI2YTEtNjEzNTdjMDNhMGI4IiwgInRhZyI6ICJqYWRlIiwgIm5hbWUiOiAiSmFkZSIsICJkZXNjIjogIiAiLCAic3ByaXRlIjogImlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFJQUFBQUFRQ0FNQUFBRHBob2U2QUFBQU1GQk1WRVVBQUFBQUFBQUFPQ29BY3prQW8xd0FBQUFBQUFBQUFBRC8vLysxLytOTi83SUF4M3NBQUFBQUFBQUFBQUFBQUFEbWEyRmdBQUFBRUhSU1RsTUEvLy8vLy8vLy8vLy8vLy8vLy8vL3dGQ0xRd0FBQVVsSlJFRlVTSW5GbGNGeXhDQU1RelBBUWVELy85KzFReExMNm5aUG5TMm5QR3dKQlRMa09NN1JmQncwdnM3V3U5Rk1nNC8yb2Y3WDNHME02ODlNZzdEWEl4RzRQeEtDOVhCQzhZUDRLMU9nc1h5R0FteEcxbkd1Z093SEtrZWd3aU1ZekxXZi9mdWFjNDExUjJvUTdnc25JL3VCNE8yNDlRaG12MmZCbTFrZmZzOGh0ejZIemJYc0NTRGNKNFFIZ2tGNllOMW5zdjE4aXhyWUg2d1B2d3dRSitJenVRUENCbUYvdThyeHVvWE5sQ2VFT1lBdk1PZklIUkRXdXNYNnRRNW9QMVFQOWFzQmJJN09BWmkxSGdHa0hnRnFQMVFQOWFOdjRId2pPZ0pocmI5aEQxRHJmQ1M3SDZvdkFYeEgrQWdxU3gyRnNhK3RyT1BzaCtyeHc0OENSS1RSTTBEbHdHUi9MdXdUVlg4MXNQN2NrdlMvK3ZPdWJWdHdNeXBqancvY21PUEtWUDFiZjdycm04Vm5SVmR2WlZSR3JjY0ZET21QUUwvenBkZWZUZjhteTgvdVAzL0hML0tsR2s4WmRRUjdBQUFBQUVsRlRrU3VRbUNDIiwgImNyZWF0ZWRfYnkiOiAiVGhlIEZvcmdlIiwgImNyZWF0ZWRfZm9yIjogInBpZmFjZTMxNCIsICJjcmVhdGVkX2F0IjogIjIwMjItMDYtMjYgMTk6MjA6NTQuMjYwNDY1In0="),
    Gem("mAhmrXpm5CzpeyMztn4rtWwMnS2UAku9p/KtWOSczHg8YYU6MV2VIE9qunkutsxTmLfTK6mcvF6Q0lyt4IX9DHsiaWQiOiAiNGQzMWVjNDMtZGRmZS00ZTVlLWE4MzEtOGFjZTBlMGEzOTY3IiwgInRhZyI6ICJzYXBwaGlyZSIsICJuYW1lIjogIlNhZmlyYSIsICJkZXNjIjogIiAiLCAic3ByaXRlIjogImlWQk9SdzBLR2dvQUFBQU5TVWhFVWdBQUFJQUFBQUFRQ0FNQUFBRHBob2U2QUFBQU1GQk1WRVVBQUFBQUFBQUFBRFVBQUlBQUFJd0FBQUFBQUFBQUFBRC8vLzk5b3Y4bUp2OEFBQUFBQUFBQUFBQUFBQUFBQUFDWUg3NVlBQUFBRUhSU1RsTUEvLy8vLy8vLy8vLy8vLy8vLy8vL3dGQ0xRd0FBQVBOSlJFRlVTSW5ObGMwV2hTQUloQlUzaysvL3dJR0dDYVkzVjExV2ZjendjenhsSWZ4RlVJa3YrWkNnT1FQQ01Eb293UGlaWU9yaCtubHUvVE5SU29sd1pmaWhNcHgrSlNyRHNkY0xZNjIzQlZMa3dMMkFZOVhoV1FjMDl2cTYvdTVQbEROcGh1ZGJ6cktzWmE4cnd6SisrZHNDTWFYY0d6eGoxTEh5NzdLY2lXYWVHS1BPWnpMMzczQ2dJMm9pUm5yTHdKNS96cHBKa1dKK3pUeC8wTEZSMzNOSnlFdlJHNVlNWHVCbUVOOElyRU1Yd0dhL2tpa3hZeGptZDl2cWxkdDhNYXpxeC82Y2tJdUJ0Mm9GaGlHZkZ5eGIzZmpSR005KzM3OThDQkkwWTVuZk1hcU9pK1VDOXY0MUQvTysveGw5R1NjTVF4U0VjU0tTaGdBQUFBQkpSVTVFcmtKZ2dnPT0iLCAiY3JlYXRlZF9ieSI6ICJUaGUgRm9yZ2UiLCAiY3JlYXRlZF9mb3IiOiAicGlmYWNlMzE0IiwgImNyZWF0ZWRfYXQiOiAiMjAyMi0wNi0yNiAxOToyMTowNi42MDM2NjEifQ=="),
]

gems_b = [
    Gem("xwsATxD3s0JqSEjCDcOUJ0bGOqfJBsg22Q5gxLbwVzWLm7PaFCpvKj8H0CYJiE7+UpahOZOnC67UaItD6LdpBXsiaWQiOiAiNjFhOGEyMDctOGZmZS00OWUyLTg0OTAtNDk5MTllNTg0Njg3IiwgInRhZyI6ICJnYXJuZXQiLCAibmFtZSI6ICJHcmFuYWRhIiwgImRlc2MiOiAiICIsICJzcHJpdGUiOiAiaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUlBQUFBQVFDQU1BQUFEcGhvZTZBQUFBTUZCTVZFVUFBQUFBQUFBMkFBQTJBQldQQUNFQUFBQUFBQUFBQUFELy8vLy9iSWovS2xvQUFBQUFBQUFBQUFBQUFBQUFBQUFkaGUycUFBQUFFSFJTVGxNQS8vLy8vLy8vLy8vLy8vLy8vLy8vd0ZDTFF3QUFBUXhKUkVGVVNJbk5sVXNTaERBSVJCUElvaWYzUC9CQUZBdzR4bkxsc0h0cFBsMnBpS1g4UmRDSUY1ay9HblRvbVFGbEJCMVVFUEtGRU9xUittWDIvcDI1dGNiWVR3aEV3akxWZEdOTWpNUlpINHkxN2daYWxjQmhJTEhweUd3RG5MTytyai82TS9mT2RpTHppWG9uNTY1bUkyZmRHSkZ4bCs4R2FtdDlUc2lNczQ1Vi9rTm12Uk03VVQwenpycmN5WFgrRXk3MHFXYWdWaHBNOXd3OHk3OW1jOUFxMTI1TXlyUmdtWC9TOGFCKzVtRkFIK0ZzUUI4SlhUSEV3TUVnMlFpaXd3emdyajd4T0JseHhRZ3NienZxRy90OFRWalZuL3ZMZ1M0aXVRVXYwRVVoTHIyaFhubmdxSWQ4T09OM2Z1NC9QZ1FOVHV6TFd1ZFBqRTNIenJxQWMvNmFjLy95L3Mvb3pmZ0NxS0VWSFRoUGpZQUFBQUFBU1VWT1JLNUNZSUk9IiwgImNyZWF0ZWRfYnkiOiAiVGhlIEZvcmdlIiwgImNyZWF0ZWRfZm9yIjogInBpZmFjZTMxNCIsICJjcmVhdGVkX2F0IjogIjIwMjItMDYtMjYgMTk6MjI6NDguNzgxODQ2In0="),
    Gem("Ovg5EPW9Vs6OwdoOaRPwg+wSodaTOyK4D2cGwIZ3LjjIB9MSZNiFHogSYjUmzRKlPOrcTMhUQoZtGSeK7DseC3siaWQiOiAiYjY3YjU1MzUtMjdiOC00YmI2LWI2OWItNTYwODM0MjlkZTUwIiwgInRhZyI6ICJsYXBpcy1sYXp1bGkiLCAibmFtZSI6ICJMXHUwMGUxcGlzLUxhelx1MDBmYWxpIiwgImRlc2MiOiAiICIsICJzcHJpdGUiOiAiaVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUlBQUFBQVFDQU1BQUFEcGhvZTZBQUFBTUZCTVZFVUFBQUFBQUFBQUFDb0FDbUFBQ29rQUFBQUFBQUFBQUFELy8vK3p0ZjlLVC84QUFNZ0FBQUFBQUFBQUFBQUFBQUFwVnFXT0FBQUFFSFJTVGxNQS8vLy8vLy8vLy8vLy8vLy8vLy8vd0ZDTFF3QUFBVTlKUkVGVVNJbkZsY21Td3lBTVJGMFdod2Y4Ly8rTzVBMnBKOGxwRnNxSFBFdmRkR0VDMjNhTTNjZVd4cCt6RGJQMFpzZkgvcUgrMHp6R25HTThiM2FFdlI2SnlQMlJrS3pIaWVLSCtDdXZBTE8zTm5PQWsxbDFXc3pBNm9mS0xRSm1uc0ZrcnYzSjMyeTIxbWMzdXhoaG14ek02b2ZnMC9IVUU1ejluZ2x2enZyd3c1NEFIcWoxRkVEWWZBRXFONEpKZWdoRGxoK1lrZjNKK3ZCYkFVWnZZN1ErVW9EQ0ErSHVINkN3VDBmaE1aUWJ3am1BTi90SDZVOEFZYTJQbUwvV1FmdFJQZXBYQXB4cnZnSVUxcm9IMERwb1A2cEgvZEllT0daTWUwQlk2eTg0QXBTNlA5S1A2aVZBbHdCZERCWlRtTzJhLzY1ekJsQzlCaXFiME5lMDk3a0NWRDcrOFE5RFpYOVI5WGREMGtlZDVYLzFQd0dPaitwNzVqNklxTXc1UHJCbDlwL2Y5Qy85MDFsdnZod2VjSC9EVktiVzR3QkcrbzlBYi9uUzU4dkdGeVVmemIvUGN0bjk1M1g4QmRHTEc3ZklyVUUzQUFBQUFFbEZUa1N1UW1DQyIsICJjcmVhdGVkX2J5IjogIlRoZSBGb3JnZSIsICJjcmVhdGVkX2ZvciI6ICJwaWZhY2UzMTQiLCAiY3JlYXRlZF9hdCI6ICIyMDIyLTA2LTI2IDE5OjIzOjAxLjQ0OTk5NyJ9")
]

skey = PrivateKey.generate()
pkey = skey.public_key

skey2 = PrivateKey.generate()
pkey2 = skey2.public_key

def local_search():
    if argv[1] == '1':
        endp = SearchEndpoint(None, 7515, None)
        endp.set_username("alice")
        endp.set_keys(skey, pkey)
        endp.sync_gallery(GemList(['Ruby', 'Sapphire'], ['Amethyst', 'Pearl']))
        endp.local_search(lambda s: print(f'Found: {s}'))
    else:
        endp = SearchEndpoint(None, 7520, None)
        endp.set_username("bob")
        endp.set_keys(skey, pkey)
        endp.sync_gallery(GemList(['Pearl', 'Rose Quartz'], ['Sapphire']))
        endp.listen()

def trade():
    def t1():
        gl = GemList(['Gema3', 'Gema4'], ['Gema1', 'Gema2'])
        trade = Trade("127.0.0.1", 7520, pkey2, gl, GemList([], []))
        endp = TradeEndpoint(None, None, 7515)
        endp.set_username("alice")
        endp.set_keys(skey, pkey)
        endp.update(trade.ip, trade.key, gl)
    def t2():
        endp = TradeEndpoint(None, None, 7520)
        endp.set_username("bob")
        endp.set_keys(skey2, pkey2)
        endp.bind(TradeEvent.TRADE, lambda **args: print(args))
        endp.bind(TradeEvent.ACCEPT, lambda **args: print(args))
        endp.bind(TradeEvent.REJECT, lambda **args: print(args))
        endp.bind(TradeEvent.FUSION, lambda **args: print(args))
        endp.bind(TradeEvent.GEMS, lambda **args: print("Received gems: ", args))
        endp.listen()
    threading.Thread(target=t2).start()
    sleep(2)
    threading.Thread(target=t1).start()


trade()