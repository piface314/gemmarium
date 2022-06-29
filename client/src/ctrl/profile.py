from model.profile import Profile
from network.profile import ProfileEndpoint
from network.search import SearchEndpoint


class ProfileCtrl:

    def __init__(self, endpoint: ProfileEndpoint, search_endp: SearchEndpoint):
        self.__endpoint = endpoint
        self.__profile: Profile = None
        self.__search_endp = search_endp
        self.load()
    
    def load(self):
        self.__profile = Profile.load()
        self.__search_endp.set_identity(self.get_id(), self.get_username())
    
    def get_keys(self):
        p = self.__profile
        return p.private_key, p.public_key
    
    def get_id(self):
        return self.__profile.id
    
    def get_username(self):
        return self.__profile.username

    def signup(self, username: str):
        try:
            uid = self.__endpoint.signup(username, self.__profile.public_key)
            self.__profile.id = uid
            self.__profile.username = username
            self.__search_endp.set_identity(uid, username)
            self.__profile.save()
        except Exception as e:
            raise e

    def is_logged_in(self):
        return self.__profile.id is not None

