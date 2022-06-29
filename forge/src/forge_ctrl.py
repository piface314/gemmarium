from database import Database
from datetime import datetime
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey, VerifyKey
from random import choices
import base64
import json
import uuid


class ForgeCtrl:

    def __init__(self, gem_time: int, db: Database, sign_key: SigningKey, verify_key: VerifyKey):
        self.db = db
        self.gem_time = gem_time
        self.sign_key = sign_key
        self.verify_key = verify_key
        self.__load_gems()

    def __load_gems(self):
        data = json.load(open('res/gems.json'))
        self.fusions = data['fusions']
        self.gems = data['gems']
        self.gem_list = []
        self.gem_rarity = []
        for gem_id, gem_data in self.gems.items():
            self.gem_list.append(gem_id)
            self.gem_rarity.append(gem_data['rarity'])

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
        signed_gem = self.sign_key.sign(gem_json, Base64Encoder)
        return signed_gem.decode('utf-8')

    def choose_gem(self, username):
        gem_id = choices(self.gem_list, weights=self.gem_rarity, k=1)[0]
        print(f"Thread@{username}: chose gem {gem_id}")
        gem = self.create_gem(gem_id, username)
        return self.sign_gem(gem)

