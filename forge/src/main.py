from database import Database
from forge_ctrl import ForgeCtrl
from forge_endpoint import ForgeEndpoint
from nacl.signing import SigningKey, VerifyKey
from sys import argv
import keys

from concurrent.futures import ThreadPoolExecutor
from rmi.forge_pb2_grpc import add_ForgeServicer_to_server
import grpc


if __name__ == '__main__':
    port, gem_time = argv[1:5]
    db = Database()
    ctrl = ForgeCtrl(
        db=db,
        gem_time=int(gem_time),
        sign_key=SigningKey(keys.forge_sign_key),
        verify_key=VerifyKey(keys.forge_vkey),
        vault_vkey=VerifyKey(keys.vault_vkey)
    )
    endp = ForgeEndpoint(ctrl)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_ForgeServicer_to_server(endp, server)
    server.add_insecure_port(f'[::]:{port}')
    print(f"Forge started!")
    server.start()
    server.wait_for_termination()

    
