from database import Database
from datetime import datetime
from nacl.signing import SigningKey, VerifyKey
from random import choices, choice
import base64
import json
import threading
import uuid

class FusionRequest:

    def __init__(self):
        self.user_a: str = None
        self.user_b: str = None
        self.gems_a = None
        self.gems_b = None
        self.fusion = None
    
    def is_complete(self):
        return self.gems_a is not None and self.gems_b is not None
    
    def has_fusion_set(self):
        return self.fusion is not None
    
    def get_gems(self, vkey: VerifyKey):
        # return self.gems_a, self.gems_b
        gems_a = [json.loads(vkey.verify(raw)) for raw in self.gems_a]
        gems_b = [json.loads(vkey.verify(raw)) for raw in self.gems_b]
        return gems_a, gems_b


class ForgeCtrl:

    def __init__(self,
            db: Database,
            gem_time: int,
            sign_key: SigningKey,
            verify_key: VerifyKey,
            vault_vkey: VerifyKey):
        self.db = db
        self.gem_time = gem_time
        self.sign_key = sign_key
        self.verify_key = verify_key
        self.vault_vkey = vault_vkey
        self.fusion_requests = {}
        self.__load_gems()
        self.__lock = threading.Lock()

    def __load_gems(self):
        data = json.load(open('res/gems.json'))
        self.fusions = {k: set(v) for k, v in data['fusions'].items()}
        self.gems = data['gems']
        self.gem_list = []
        self.gem_rarity = []
        for gem_id, gem_data in self.gems.items():
            self.gem_list.append(gem_id)
            self.gem_rarity.append(gem_data['rarity'])
    
    def auth(self, token: bytes):
        try:
            token = json.loads(self.vault_vkey.verify(token))
            expire = datetime.fromisoformat(token['expire'])
            if datetime.now() >= expire:
                return None, None
            return token['id'], token['username']
        except:
            return None, None

    def check_quota(self, uid):
        q = self.db.get_quota(uid)
        if not q:
            return True, 0
        diff = (datetime.now() - q.last_request_at).seconds
        return diff >= self.gem_time, self.gem_time - diff
    
    def set_quota(self, uid):
        self.db.set_quota(uid, datetime.now())
    
    def load_sprite(self, gem_id):
        with open(f'res/gems/{gem_id}.png', 'rb') as f:
            blob = f.read()
        return base64.b64encode(blob).decode('utf-8')
    
    def create_gem(self, gem_id, username):
        gem_data = self.gems[gem_id]
        return {
            'id': str(uuid.uuid4()),
            'tag': gem_id,
            'name': gem_data['name'],
            'desc': gem_data['desc'],
            'sprite': self.load_sprite(gem_id),
            'created_by': 'The Forge',
            'created_for': username,
            'created_at': str(datetime.now())
        }
    
    def sign_gem(self, gem):
        gem_json = json.dumps(gem).encode('utf-8')
        return self.sign_key.sign(gem_json)

    def choose_gem(self, username):
        gem_id = choices(self.gem_list, weights=self.gem_rarity, k=1)[0]
        gem = self.create_gem(gem_id, username)
        return self.sign_gem(gem)

    def basic_material(self, gems):
        done = set()
        gems = gems.copy()
        while gems:
            m = gems.pop()
            if m in self.fusions:
                gems.update(self.fusions[m])
            else:
                done.add(m)
        return done
    
    def materials(self, tag, fusion, material):
        return {m for m in material if m != tag and self.basic_material({m}).issubset(fusion)}
    
    def can_fuse(self, tag, fusion, mat_a, mat_b):
        am = self.materials(tag, fusion, mat_a)
        bm = self.materials(tag, fusion, mat_b)
        abm = self.basic_material(am)
        bbm = self.basic_material(bm)
        return am and bm and abm & fusion and bbm & fusion \
            and self.basic_material(am | bm) == fusion

    def find_fusion(self, gems_a, gems_b):
        a = {gem['tag'] for gem in gems_a}
        b = {gem['tag'] for gem in gems_b}
        possible = [k for k, f in self.fusions.items() if self.can_fuse(k, f, a, b)]
        if not possible:
            return None, set(), set()
        k = choice(possible)
        f = self.fusions[k]
        am = self.materials(k, f, a)
        bm = self.materials(k, f, b)
        for m in am | bm:
            if m not in self.fusions:
                continue
            mat = self.fusions[m]
            am = am - mat
            bm = bm - mat
        shared = am & bm
        am, bm = am - shared, bm - shared
        while shared:
            m = shared.pop()
            if len(am) < len(bm):
                am.add(m)
            elif len(bm) < len(am):
                bm.add(m)
            else:
                choice([am, bm]).add(m)
        return k, am, bm
    
    def fuse(self, ida, idb, req: FusionRequest):
        user_a, user_b = req.user_a, req.user_b
        gems_a, gems_b = req.get_gems(self.verify_key)
        tag, tags_a, tags_b = self.find_fusion(gems_a, gems_b)
        gem = self.sign_gem(self.create_gem(tag, f'{user_a}+{user_b}')) \
            if tag else None
        from_a = {choice([i for i, g in enumerate(gems_a) if g['tag'] == t])
            for t in tags_a}
        from_b = {choice([i for i, g in enumerate(gems_b) if g['tag'] == t])
            for t in tags_b}
        raw_gems_a = req.gems_a
        raw_gems_b = req.gems_b
        to_a = [g for i, g in enumerate(raw_gems_b) if i not in from_b]
        to_b = [g for i, g in enumerate(raw_gems_a) if i not in from_a]
        return gem, {ida: to_a, idb: to_b}

    def get_req_key(self, ida, idb):
        return (ida, idb) if ida < idb else (idb, ida)

    def get_fusion_request(self, ida, idb):
        return self.fusion_requests.get(self.get_req_key(ida, idb), None)

    def update_fusion_request(self, ida, idb, sender, name, gems):
        ida, idb = self.get_req_key(ida, idb)
        with self.__lock:
            req = self.fusion_requests.get((ida, idb), None)
            if req is None:
                req = FusionRequest()
                self.fusion_requests[(ida, idb)] = req
            if sender == ida:
                req.user_a = name
                req.gems_a = gems
            else:
                req.user_b = name
                req.gems_b = gems
            if req.is_complete() and not req.has_fusion_set():
                req.fusion = self.fuse(ida, idb, req)
    
    def remove_fusion_request(self, ida, idb):
        self.fusion_requests.pop(self.get_req_key(ida, idb), None)