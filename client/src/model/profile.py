from model import Model


class Profile(Model):

    def __init__(self, username, pkey, skey, last_sync):
        self.username = username
        self.public_key = pkey
        self.private_key = skey
        self.last_sync_at = last_sync

