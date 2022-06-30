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
    search_port, vault_ip, vault_port, forge_ip, forge_port, db_fp, offset = argv[1:8]
    vault_addr = (vault_ip, int(vault_port))
    forge_addr = (forge_ip, int(forge_port))
    gallery_addr = ("", 0)
    search_port = int(search_port)
    offset = int(offset)
    
    vault_pkey = PublicKey(keys.vault_pkey)
    forge_pkey = PublicKey(keys.forge_pkey)
    forge_vkey = VerifyKey(keys.forge_vkey)

    Model.set_db_fp(db_fp)
    Model.create_db('res/create.sql')

    collection_endp = CollectionEndpoint(forge_addr, forge_pkey)
    profile_endp = ProfileEndpoint(vault_addr, vault_pkey)
    search_endp = SearchEndpoint(search_port, gallery_addr, None, offset)
    trade_endp = TradeEndpoint(search_endp, forge_addr, forge_pkey)
    profile_ctrl = ProfileCtrl(profile_endp)
    search_ctrl = SearchCtrl(search_endp)
    collection_ctrl = CollectionCtrl(collection_endp, search_endp, forge_vkey)
    trade_ctrl = TradeCtrl(collection_ctrl, trade_endp)

    profile_ctrl.observe(lambda p: collection_ctrl.set_identity(p.id, p.username))
    profile_ctrl.observe(lambda p: search_endp.set_identity(p.id, p.username))
    profile_ctrl.observe(lambda p: trade_endp.set_identity(p.id, p.username))

    profile_ctrl.load()
    skey, pkey = profile_ctrl.get_keys()
    collection_endp.set_keys(skey, pkey)
    profile_endp.set_keys(skey, pkey)
    search_endp.set_keys(skey, pkey)
    trade_endp.set_keys(skey, pkey)

    collection_ctrl.load()
    collection_ctrl.sync_gallery()

    threading.Thread(target=search_endp.listen, daemon=True).start()
    threading.Thread(target=trade_endp.listen, daemon=True).start()

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


