from database import Database
from forge_ctrl import ForgeCtrl
from forge_endpoint import ForgeEndpoint
from nacl.public import PrivateKey, PublicKey
from nacl.signing import SigningKey, VerifyKey
from sys import argv
import keys


if __name__ == '__main__':
    forge_port, vault_ip, vault_port, vault_client_port, gem_time = argv[1:6]
    db = Database()
    ctrl = ForgeCtrl(
        gem_time=int(gem_time),
        db=db,
        sign_key=SigningKey(keys.forge_sign_key),
        verify_key=VerifyKey(keys.forge_vkey)
    )
    endp = ForgeEndpoint(
        port=int(forge_port),
        private_key=PrivateKey(keys.forge_skey),
        public_key=PublicKey(keys.forge_pkey),
        vault_addr=(vault_ip, int(vault_port)),
        vault_pkey=PublicKey(keys.vault_pkey),
        ctrl=ctrl
    )
    endp.connect_vault(int(vault_client_port))
    endp.listen()

    
