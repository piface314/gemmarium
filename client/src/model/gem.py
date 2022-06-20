from model import Model


class Gem(Model):

    def __init__(self,
                 gem_id,
                 name,
                 desc,
                 sprite,
                 created_for,
                 created_by,
                 created_at,
                 obtained_at,
                 is_public,
                 payload
                 ):
        self.id = gem_id
        self.name = name
        self.desc = desc
        self.sprite = sprite
        self.created_for = created_for
        self.created_by = created_by
        self.created_at = created_at
        self.obtained_at = obtained_at
        self.is_public = is_public
        self.payload = payload
