from exceptions import AuthError, QuotaError, UnknownError
from network.endpoint import Endpoint
from network.profile import ProfileEndpoint
import base64
import requests


class CollectionEndpoint(Endpoint):

    def __init__(self, forge_addr, profile_endp: ProfileEndpoint):
        self.forge_addr = f'http://{forge_addr[0]}:{forge_addr[1]}'
        self.profile_endp = profile_endp

    def request_gem(self):
        token = self.profile_endp.auth()
        res = requests.get(self.forge_addr+'/gem', params=dict(token=token))
        if res.status_code != 200:
            body = res.json()
            if body['error'] == 'AuthError':
                raise AuthError()
            if body['error'] == 'QuotaExceeded':
                raise QuotaError(body['wait'])
            raise UnknownError()
        return base64.b64decode(res.json()['gem'])
