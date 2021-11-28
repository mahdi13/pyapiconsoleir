import base64
import functools

from nanohttp import RestController, json, context, HttpUnauthorized

valid_mock_consumer_key = 'mock-app'
valid_mock_consumer_secret = 'mock-secret'

valid_mock_client_credential_tokens = [
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Im1vY2stYXBwIn0.maxHiBX70CtQM_p_hNsv0RLmfhj_eg7bmRuN6We9HEU'
]

invalid_mock_client_credential_tokens = [
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsInZhbGlkIjpmYWxzZX0.eyJpZCI6Im1vY2stYXBwIn0'
    '.9AxqC62m5tRc9Jxy5Mfj58YpgO2ANfcWhsm6LNMtgpo'
]

valid_mock_postal_code = '1417994411'


def authorize_client_credential(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in context.environ:
            raise HttpUnauthorized()

        encoded_token = context.environ['HTTP_AUTHORIZATION']
        if encoded_token is None or not encoded_token.strip().strip('Bearer').strip():
            raise HttpUnauthorized()
        encoded_token = encoded_token.strip().strip('Bearer').strip()

        if encoded_token in valid_mock_client_credential_tokens:
            return func(*args, **kwargs)

        if encoded_token in invalid_mock_client_credential_tokens:
            raise HttpUnauthorized()
        raise HttpUnauthorized()

    return wrapper


def authorize_basic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in context.environ:
            raise HttpUnauthorized()

        encoded_token = context.environ['HTTP_AUTHORIZATION']
        if encoded_token is None or not encoded_token.strip().strip('Basic').strip():
            raise HttpUnauthorized()
        encoded_token = encoded_token.strip().strip('Basic').strip()

        try:
            credential = base64.decodebytes(encoded_token.encode()).decode().split(":")
            if credential[0] == valid_mock_consumer_key and credential[1] == valid_mock_consumer_secret:
                return func(*args, **kwargs)
        except:
            raise HttpUnauthorized()

        raise HttpUnauthorized()

    return wrapper


class MockPostalCodeToAddressV1(RestController):

    @json
    @authorize_client_credential
    def post(self):
        return {
            'postalCode': '1417994411',
            'address': 'استان تهران، شهر تهران، دانشگاه تهران/14179، خيابان 16 آذر، پلاک 78، طبقه 10، واحد 1009، کد پستی:1417994411'
        }


class MockPostalCodeToAddressV2(RestController):

    @json
    @authorize_client_credential
    def get(self):
        return {
            'code': '1417994411',
            'addressInfo': {
                'postalCode': '1417994411',
                'address': 'استان تهران، شهر تهران، دانشگاه تهران/14179، خيابان 16 آذر، پلاک 78، طبقه 10، واحد 1009، کد پستی:1417994411'
            }
        }


class MockTokenController(RestController):

    @json
    @authorize_basic
    def post(self):
        return {
            'access_token': valid_mock_client_credential_tokens[0],
            'scope': 'default',
            'token_type': 'Bearer',
            'expires_in': 3600
        }


class ApiconsoleClientRootMockController(RestController):
    token = MockTokenController()
    postalCodeToAddress = MockPostalCodeToAddressV1()
    postal = MockPostalCodeToAddressV2()

    def __call__(self, *remaining_paths):
        if list(remaining_paths) == 'kyc/address/v1.0/postalCodeToAddress'.split('/'):
            return super().__call__(*remaining_paths[-1:])

        if list(remaining_paths) == 'ide/postalcode/v2.0/services/postal'.split('/'):
            return super().__call__(*remaining_paths[-1:])

        return super(ApiconsoleClientRootMockController, self).__call__(*remaining_paths)
