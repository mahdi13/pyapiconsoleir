import re

import requests
import logging

from pyapiconsoleir.const import URL_MAINNET
from pyapiconsoleir.exceptions import ApiconsoleHttpException
from pyapiconsoleir.responses import PostalCodeToAddress, MatchPhoneToNationalCode, IdentityInquiry
from pyapiconsoleir.token import ClientCredentialToken


class ApiconsoleClient:

    def ensure_access_token(self):
        if not (self._token.access_token and self._token.is_valid):
            self._token.refresh(self)
        return self._token.access_token

    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 logger: logging.Logger = None,
                 requests_extra_kwargs: dict = None,
                 base_url: str = None,
                 ):
        self._token = ClientCredentialToken(consumer_key=consumer_key, consumer_secret=consumer_secret)
        self.logger = logger or logging.getLogger('apiconsole')
        self.requests_extra_kwargs = requests_extra_kwargs or {}
        self.base_url = base_url or URL_MAINNET

    def _request(self, resource: str, method='post', params: dict = None, json: dict = None, data: dict = None,
                 headers: dict = None, auth=True):
        method = method.upper()
        url = ''.join([self.base_url, resource])
        headers = headers or dict()
        if auth:
            self.ensure_access_token()
            headers = {**headers, **self._token.generate_authorization_header()}
        response = requests.request(
            method,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers
        )
        if response.status_code != 200:
            raise ApiconsoleHttpException(
                response=response,
                logger=self.logger
            )
        return response.json()

    def postalcode_to_address_v1(self, postal_code) -> PostalCodeToAddress:
        from warnings import warn
        warn('Deprecated: postalcode_to_address_v1, please use postalcode_to_address_v2')
        return PostalCodeToAddress(
            self._request('/kyc/address/v1.0/postalCodeToAddress', json={'postalCode': str(postal_code)})
        )

    def postalcode_to_address_v2(self, postal_code) -> PostalCodeToAddress:
        return PostalCodeToAddress(
            self._request(
                '/ide/postalcode/v2.0/services/postal',
                method='get',
                params={'code': str(postal_code)}
            ).get('addressInfo')
        )

    def match_phone_to_national_code(self, national_code, mobile_number) -> MatchPhoneToNationalCode:
        if national_code is None or not re.match('^[0-9]{10}$', national_code):
            raise ValueError(f'Bad national id: {national_code}')

        if mobile_number is None or not re.match('^[0-9]{11}$', mobile_number):
            raise ValueError(f'Bad phone number: {mobile_number}')

        return MatchPhoneToNationalCode(
            self._request(
                '/kyc/match/number/v2.0/matching',
                method='get',
                params={'nationalCode': str(national_code), 'mobileNumber': mobile_number}
            )
        )

    def identity_inquiry(self, national_code, birth_date) -> IdentityInquiry:

        if national_code is None or not re.match('^[0-9]{10}$', national_code):
            raise ValueError(f'Bad national id: {national_code}')

        if birth_date is None or not re.match('^[0-9]{8}$', birth_date):
            raise ValueError(f'Bad birthdate (sample: 13600101): {birth_date}')

        return IdentityInquiry(
            self._request(
                '/ide/identity/v1/services/identity',
                method='get',
                params={'nationalCode': str(national_code), 'birthDate': birth_date}
            )
        )
