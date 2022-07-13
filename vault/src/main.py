from auth_ctrl import AuthCtrl
from auth_endpoint import AuthEndpoint
from database import Database
from nacl.public import PrivateKey, PublicKey
from sys import argv
import keys


from concurrent.futures import ThreadPoolExecutor
from rmi.vault_pb2_grpc import add_AuthServicer_to_server
import grpc


if __name__ == '__main__':
    vault_port = argv[1]
    db = Database()
    auth_ctrl = AuthCtrl(db, keys.auth_key, PrivateKey(keys.vault_skey))
    auth_endp = AuthEndpoint(int(vault_port), auth_ctrl)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_AuthServicer_to_server(auth_endp, server)
    server.add_insecure_port(f'[::]:{vault_port}')
    print(f"Vault started!")
    server.start()
    server.wait_for_termination()

    
