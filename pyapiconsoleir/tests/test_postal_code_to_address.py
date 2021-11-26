from pyapiconsoleir.tests.helper import ApiClientTestCase
from pyapiconsoleir.tests.mock_api_server import valid_mock_postal_code


class PostalCodeToAddressTestCase(ApiClientTestCase):

    def test_postal_code_to_address(self):
        result = self.api_client.postalcode_to_address(valid_mock_postal_code)
        self.assertIsNotNone(result.postal_code)
        self.assertIsNotNone(result.address)
