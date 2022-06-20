from model.profile import Profile
from network.profile import ProfileEndpoint


class ProfileCtrl:

    def __init__(self, endpoint: ProfileEndpoint):
        self.__endpoint = endpoint
        self.__profile = None
        self.__is_logged_in = False
    
    def load(self):
        pass

    def signup(self, username):
        pass
