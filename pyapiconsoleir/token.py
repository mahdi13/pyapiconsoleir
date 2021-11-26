import base64
import time

import ujson


class Token:
    def __init__(self):
        pass

    @property
    def is_valid(self):
        raise NotImplementedError()

    def revoke(self):
        raise NotImplementedError()

    def refresh(self, *args, **kwargs):
        raise NotImplementedError()

    def generate_authorization_header(self):
        raise NotImplementedError()

    @classmethod
    def build_basic_authentication_token(cls, username, password):
        return base64 \
            .encodebytes(f'{username}:{password}'.encode()) \
            .decode().strip()


class ClientCredentialToken(Token):
    __token_type__ = 'CODE'

    def __init__(self, **kwargs):
        super().__init__()
        self._consumer_key = kwargs.get('consumer_key', None)
        self._consumer_secret = kwargs.get('consumer_secret', None)
        self.access_token = None
        self.expires_in = None
        self.issued_in = None
        self.scope = None
        self.payload = None

    @property
    def is_valid(self):
        return time.time() - self.issued_in < self.expires_in

    def revoke(self):
        raise NotImplementedError()

    def refresh(self, http_client):
        new_token = self.fetch(http_client)
        self.access_token = new_token['access_token']
        self.expires_in = new_token['expires_in']
        self.scope = new_token['scope']
        self.issued_in = time.time()

    @classmethod
    def load(cls, raw_token, refresh_token=None):
        payload = ujson.loads(base64.decodebytes((raw_token.split('.')[1] + '==').encode()).decode())
        payload.setdefault('refreshToken', refresh_token)
        return cls(value=raw_token, **payload)

    def generate_authorization_header(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    # noinspection PyProtectedMember
    def fetch(self, http_client):
        url = '/token'

        encoded_basic_authentication = self.build_basic_authentication_token(self._consumer_key, self._consumer_secret)
        return http_client._request(
            resource=url,
            data={"grant_type": "client_credentials"},
            method='post',
            headers={'Authorization': f'Basic {encoded_basic_authentication}'},
            auth=False
        )
