from pyapiconsoleir.token import ClientCredentialToken


class ApiconsoleClient:
    __base_url__ = 'https://gw.apiconsole.ir'

    def ensure_access_token(self):
        if not (self._token.access_token and self._token.is_valid):
            self._token.refresh(self)
        return self._token.access_token

    def __init__(self, consumer_key: str, consumer_secret: str):
        self._token = ClientCredentialToken(consumer_key=consumer_key, consumer_secret=consumer_secret)
