from database import Database
from forge_ctrl import ForgeCtrl
from forge_ctrl import FusionRequest as FusionReqModel
from nacl.public import PrivateKey, PublicKey, Box, SealedBox
from nacl.signing import VerifyKey, SigningKey
import keys
import threading

import grpc
from rmi.forge_pb2 import GemRequest, FusionRequest
from rmi.forge_pb2_grpc import ForgeStub
from rmi.vault_pb2 import AuthRequest
from rmi.vault_pb2_grpc import AuthStub

forge_vkey = VerifyKey(keys.forge_vkey)
forge_signkey = SigningKey(keys.forge_sign_key)
vault_pkey = PublicKey(keys.vault_pkey)
vault_vkey = VerifyKey(keys.vault_vkey)

client_keys = {
    '322d85b6-2188-4494-aba1-be9519c5f729': (
        PrivateKey(b't\x05\xb3\xd4\x199b*Q\xb4\t\x9eC_az@\xf4#y\xbbD\xe4\xe1$\x942\x89\xe0-\xbd\xe7'),
        PublicKey(b'\xc1\x8a\xe8D1\xb9Q:\xcf\x88o\x1b\x8f\xea\xad\nv4\xce\xa2\xf0J\xcb\xa5\x9b\x0b\xa6\x80_$\xbds')
    ),
    '3b089561-0033-4b79-b691-1f0842898e7a': (
        PrivateKey(b'\xb1\xc1(\xcf6\xf7\xeb\x84p=\xf9\xcf\x0bS\x81\xa73xp\xb9\x98\xe8\xe5\xb7\xcc1J\x16\x88n\xc78'),
        PublicKey(b'\x1b\x0c\xef\xf6j\x81\x1a\xcb{\xd3\xf5-\x13\x9d]H\xec\xdc-\x0f\x9e\xda`-f\xa9\x01\xcc\xb7\x1b\x884')
    )
}

client_gems = {
    '322d85b6-2188-4494-aba1-be9519c5f729': [
        b'i2\x90\x1a\xca\x02\xe0\xfc"x\xd7\xee\x04\x0f\xb8v",.Zr\xe3\xa2E\xa3H\xc9J@V\xeb\x0fQp\xa6N\xfc\xcdk\xb0\xb9@vv\xdcj\x8f\xeat\xcd\xbd\xe0\xd2\xd1U\xc4O\xe5c@G\xb3~\r{"id": "57d02ac1-5560-45e7-8405-07fa1f15aba3", "tag": "aquamarine", "name": "\\u00c1gua-Marinha", "desc": "Variedade do berilo, esta gema costuma ser quase transparente, como a \\u00e1gua.", "sprite": "iVBORw0KGgoAAAANSUhEUgAAAIAAAAAQCAMAAADphoe6AAAAMFBMVEUAAAAAAAAoTHMOKjYbdJQAAAAAAAAAAAD////j9/+o4f9HyP8AAAAAAAAAAAAAAAAx/MUPAAAAEHRSTlMA////////////////////wFCLQwAAATBJREFUSInFlcFuxCAMBSPMYQL//7/F0F3sR7tVpWrLbWL7MXKk5LrmKeNc4byd+zjhSWGc8qL+19x6vcOTgvCouxGx3w2J8wwi5SH5ykGgVrujwOI9UDG/gd0Pmc0FI9/ORM79Kb9Vs61UEG6Nyex+cF6Ja57en/fNeRCO8573fMlTyPYK5gIi+wIy12mUF3A/3snKGysqxHzivOf9QoBDCBXylaQLlF8JdKs1CQh3hA1hN0pco8DKR1gExkkCkV0gsSE8BDKPnQhXhGsUmIFtC2TuCGt9vHCkPh5IPzofBOZ8EBCWOonRfmY/Os+RpwJNBJpc+MmQ+Tp5Hp2niUDb31q/0exRv8i88l5x6ocv5znyw7d+KJn1Vr5hMpPrzCty/8mc+W/92fzws/vP3/EHl5wZ33ykWgcAAAAASUVORK5CYII=", "created_by": "The Forge", "created_for": "alice", "created_at": "2022-07-17 23:24:50.706614"}',
        b'\x8dL\x12\xe4\x8f\x04\xba\x11\x8a\xb5eP\xe0\xb5\xf566SaR\xc1\x83\x94VI\x8b\xf6\x0e\xc0\xe7\xfa\xd4\xdeTy\'\xdcNY,\xef\xf9\xc2\xb4\xab\xbe\x17\xf8-\xc4zp\x12sH\x87\xdde\xd7\xc7@\xeb\xf4\x0b{"id": "892074ba-f577-4bf8-83a0-4fa7810c3298", "tag": "garnet", "name": "Granada", "desc": "Uma gema muito diversa em sua composi\\u00e7\\u00e3o qu\\u00edmica e poss\\u00edveis cores, seu nome v\\u00eam do latim, granatus (gr\\u00e3o).", "sprite": "iVBORw0KGgoAAAANSUhEUgAAAIAAAAAQCAMAAADphoe6AAAAMFBMVEUAAAAAAAA2AAA2ABWPACEAAAAAAAAAAAD/////bIj/KloAAAAAAAAAAAAAAAAAAAAdhe2qAAAAEHRSTlMA////////////////////wFCLQwAAAQxJREFUSInNlUsShDAIRBPIoif3P/BAFAw4xnLlsHtpPl2piKX8RdCIF5k/GnTomQFlBB1UEPKFEOqR+mX2/p25tcbYTwhEwjLVdGNMjMRZH4y17gZalcBhILHpyGwDnLO+rj/6M/fOdiLziXon565mI2fdGJFxl+8Gamt9TsiMs45V/kNmvRM7UT0zzrrcyXX+Ey70qWagVhpM9ww8y79mc9Aq125MyrRgmX/S8aB+5mFAH+FsQB8JXTHEwMEg2Qiiwwzgrj7xOBlxxQgsbzvqG/t8TVjVn/vLgS4iuQUv0EUhLr2hXnngqId8OON3fu4/PgQNTuzLWudPjE3HzrqAc/6ac//y/s/ozfgCqKEVHThPjYAAAAAASUVORK5CYII=", "created_by": "The Forge", "created_for": "bob", "created_at": "2022-07-17 23:33:27.796810"}'
    ],
    '3b089561-0033-4b79-b691-1f0842898e7a': [
        b'u}\x0b\xd0\xd1"k\xab\x13\x88\x9e\xd2\xe2n\x1a\t\xeb\xbfM\xcc^\xcc\xe1Mg6\xbdyXA\xb1two\xb0\n\x00[MQ\x937\x07\x98\xe1A\x10\x1b\xf0\x03\x13\xc8z\xcc\xa8h,\xdb\xa9\x85\x89\xc0W\x04{"id": "230bd9c6-3796-431a-935f-82fc0289ecc1", "tag": "amethyst", "name": "Ametista", "desc": "Variedade violeta do quartzo, cheia de significados m\\u00edsticos desde os tempos antigos.", "sprite": "iVBORw0KGgoAAAANSUhEUgAAAIAAAAAQCAMAAADphoe6AAAAMFBMVEUAAAAAAAAgAEAuAGpQAI0AAAAAAAAAAAD////puv+MAOsAAAAAAAAAAAAAAAAAAADsEAe/AAAAEHRSTlMA////////////////////wFCLQwAAAQBJREFUSInFlNuWgyAMRW3gYdv//+BJHMEQLmOna7X4tHOSQzTgtpUlW7s+zsh3+dlGhkzUaViJZX5X7zmrgXgGCDq8yqx175+S68D2D5wSgZ1j5ajP/Rsugf1KIHC2/feZQa1vG9qZ+rdsE3k8JLuEjnW3pf4eIyIaeMqUodPp8pnXr9kGnqQG7jFEnZfqPSebuD6/gZvM3/nc8rMTZ+dLA1lu8XG/KlN0Tp2Szz2/40jKLvlKCAyetVpfwenGxympTKgvfgz9XSCFghQMK9Pykc/JnA319Yz9rYGs47gaiEzL+ok92wgyg3w8M/Kvt6YE/s0MdFjVW0PuR3iub/APUxkTaqHvQTcAAAAASUVORK5CYII=", "created_by": "The Forge", "created_for": "bob", "created_at": "2022-07-17 23:32:42.991432"}',
    ]
}

def request_auth(uid):
    channel = grpc.insecure_channel('localhost:7513')
    stub = AuthStub(channel)
    res = [None, None]
    def auth():
        req = AuthRequest(id=uid)
        print(f"sending {req}")
        yield req
        while not res[0]:
            pass
        print(f"res[0] = {res[0]}")
        if res[0].error:
            print(res[0].error)
            return
        secret = SealedBox(client_keys[uid][0]).decrypt(res[0].secret)
        secret = Box(client_keys[uid][0], vault_pkey).encrypt(secret)
        yield AuthRequest(secret=secret)

    for i, r in enumerate(stub.auth(auth())):
        res[i] = r
    return res[1].token

def request_gem(uid):
    token = request_auth(uid)
    print(f"my token: {token}")
    channel = grpc.insecure_channel('localhost:7514')
    stub = ForgeStub(channel)
    req = GemRequest(token=token)
    res = stub.gem(req)
    print(res.gem)

def request_fusion(uid, peerid):
    token = request_auth(uid)
    gems = client_gems[uid]
    channel = grpc.insecure_channel('localhost:7514')
    stub = ForgeStub(channel)
    req = FusionRequest(token=token, peerid=peerid, gems=gems)
    res = stub.fuse(req)
    print(res)

def find_fusion():
    db = Database()
    ctrl = ForgeCtrl(db, 10, forge_signkey, forge_vkey, vault_vkey)
    gems_a = [{'tag': 'alexandrite'}, {'tag': 'garnet'}, {'tag': 'sapphire'}]
    gems_b = [{'tag': 'rose-quartz'}, {'tag': 'ruby'}]
    print(ctrl.find_fusion(gems_a, gems_b))
    

find_fusion()
# alice = '322d85b6-2188-4494-aba1-be9519c5f729'
# bob = '3b089561-0033-4b79-b691-1f0842898e7a'
# request_gem(alice)
# threading.Thread(target=request_fusion, args=(alice, bob)).start()
# threading.Thread(target=request_fusion, args=(bob, alice)).start()