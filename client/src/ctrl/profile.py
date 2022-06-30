from model.profile import Profile
from network.profile import ProfileEndpoint
from network.search import SearchEndpoint


class ProfileCtrl:

    def __init__(self, endpoint: ProfileEndpoint):
        self.__endpoint = endpoint
        self.__profile: Profile = None
        self.__observers = []
    
    def load(self):
        self.__profile = Profile.load()
        self.__emit()
    
    def get_keys(self):
        p = self.__profile
        return p.private_key, p.public_key
    
    def observe(self, cb):
        self.__observers.append(cb)
    
    def __emit(self):
        for cb in self.__observers:
            cb(self.___profile)
    
    def get_username(self):
        return self.__profile.username

    def signup(self, username: str):
        try:
            uid = self.__endpoint.signup(username, self.__profile.public_key)
            self.__profile.id = uid
            self.__profile.username = username
            self.__profile.save()
            self.__emit()
        except Exception as e:
            raise e

    def is_logged_in(self):
        return self.__profile.id is not None

