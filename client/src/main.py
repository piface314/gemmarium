from ctrl.collection import CollectionCtrl
from ctrl.profile import ProfileCtrl
from ctrl.search import SearchCtrl
from ctrl.trade import TradeCtrl
from kivy.config import Config
from model import Model
from nacl.public import PublicKey, PrivateKey
from nacl.signing import VerifyKey
from network.collection import CollectionEndpoint
from network.profile import ProfileEndpoint
from network.search import SearchEndpoint
from network.trade import TradeEndpoint
from sys import argv
from view.client import ClientApp
import keys
import threading

if __name__ == '__main__':
    vault_addr = (argv[1], int(argv[2]))
    forge_addr = (argv[3], int(argv[4]))
    gallery_addr = ("", 0)
    search_addr = (argv[5], int(argv[6]))
    
    vault_pkey = PublicKey(keys.vault_pkey)
    forge_pkey = PublicKey(keys.forge_pkey)
    forge_vkey = VerifyKey(keys.forge_vkey)

    Model.set_db_fp(argv[7])
    Model.create_db('res/create.sql')

    collection_endp = CollectionEndpoint(forge_addr, forge_pkey, forge_vkey)
    profile_endp = ProfileEndpoint(vault_addr, vault_pkey)
    search_endp = SearchEndpoint(gallery_addr, search_addr[1], None)
    trade_endp = TradeEndpoint(forge_vkey)
    profile_ctrl = ProfileCtrl(profile_endp, search_endp)
    search_ctrl = SearchCtrl(search_endp)
    collection_ctrl = CollectionCtrl(profile_ctrl, collection_endp, search_endp)
    trade_ctrl = TradeCtrl(collection_ctrl, trade_endp)

    profile_ctrl.load()
    skey, pkey = profile_ctrl.get_keys()
    collection_endp.set_keys(skey, pkey)
    profile_endp.set_keys(skey, pkey)
    search_endp.set_keys(skey, pkey)
    trade_endp.set_keys(skey, pkey)

    collection_ctrl.load()
    collection_ctrl.sync_gallery()

    threading.Thread(target=search_endp.listen, daemon=True).start()

    Config.read('config.ini')
    Config.set('graphics', 'width', 378)
    Config.set('graphics', 'height', 672)
    Config.set('kivy', 'default_font', [
        'res/regular.ttf',
        'res/bold.ttf',
    ])
    Config.write()
    ClientApp(
        collection_ctrl,
        profile_ctrl,
        search_ctrl,
        trade_ctrl
    ).run()


