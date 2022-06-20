from database import Database
from forge_ctrl import ForgeCtrl
from forge_endpoint import ForgeEndpoint
from sys import argv
import keys


if __name__ == '__main__':
    vault_client_port = int(argv[4])
    db = Database()
    ctrl = ForgeCtrl(gem_time=int(argv[1]), db=db)
    endp = ForgeEndpoint(
        addr=(argv[2], int(argv[3])),
        private_key=keys.forge_skey,
        public_key=keys.forge_pkey,
        vault_addr=(argv[5], int(argv[6])),
        vault_pkey=keys.vault_pkey,
        ctrl=ctrl
    )
    endp.connect_vault(vault_client_port)
    endp.run()

    
