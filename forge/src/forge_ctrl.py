from datetime import datetime
from random import choices
import base64
import json
import uuid


class ForgeCtrl:

    def __init__(self, gem_time, db):
        self.db = db
        self.gem_time = gem_time
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

    def check_quota(self, username):
        q = self.db.get_quota(username)
        if not q:
            return True, 0
        diff = (datetime.now() - q.last_request_at).seconds
        return diff >= self.gem_time, self.gem_time - diff
    
    def set_quota(self, username):
        self.db.set_quota(username, datetime.now())

    def choose_gem(self, username):
        gem_id = choices(self.gem_list, weights=self.gem_rarity, k=1)[0]
        gem_data = self.gems[gem_id]
        return {
            'id': self.get_uuid(),
            'name': gem_data['name'],
            'desc': gem_data['desc'],
            'sprite': self.load_sprite(gem_id),
            'created_by': 'The Forge',
            'created_for': username,
            'created_at': str(datetime.now())
        }

    def load_sprite(self, gem_id):
        with open(f'res/gems/{gem_id}.png', 'rb') as f:
            blob = f.read()
        return base64.b64encode(blob).decode('utf-8')

    def get_uuid(self):
        return base64.b64encode(uuid.uuid4().bytes).decode('utf-8')

