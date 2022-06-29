from auth_ctrl import AuthCtrl
from auth_endpoint import AuthEndpoint
from database import Database
from nacl.public import PrivateKey, PublicKey
from sys import argv
import keys

if __name__ == '__main__':
    vault_port, forge_ip, forge_port = argv[1:4]
    db = Database()
    auth_ctrl = AuthCtrl(db)
    auth_endp = AuthEndpoint(
        port=int(vault_port),
        private_key=PrivateKey(keys.vault_skey),
        public_key=PublicKey(keys.vault_pkey),
        ctrl=auth_ctrl
    )
    forge_addr = (forge_ip, int(forge_port))
    auth_endp.trust_host(forge_addr, PublicKey(keys.forge_pkey))
    auth_endp.listen()
