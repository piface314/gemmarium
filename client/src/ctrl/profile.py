from model.profile import Profile
from network.profile import ProfileEndpoint


class ProfileCtrl:

    def __init__(self, endpoint: ProfileEndpoint):
        self.__endpoint = endpoint
        self.__profile: Profile = None
        self.load()
    
    def load(self):
        self.__profile = Profile.load()
    
    def get_keys(self):
        p = self.__profile
        return p.private_key, p.public_key
    
    def get_username(self):
        return self.__profile.username

    def signup(self, username: str):
        try:
            self.__endpoint.signup(username, self.__profile.public_key)
            self.__profile.username = username
            self.__profile.save()
        except Exception as e:
            raise e

    def is_logged_in(self):
        return self.__profile.username is not None

