from pyapiconsoleir.tests.helper import ApiClientTestCase
from pyapiconsoleir.tests.mock_api_server import valid_mock_national_code, valid_mock_phone_number


class MatchPhoneToNationalCodeTestCase(ApiClientTestCase):

    def test_match_phone_to_national_code(self):
        result = self.api_client.match_phone_to_national_code(valid_mock_national_code, valid_mock_phone_number)
        self.assertTrue(result.is_matched)

        result = self.api_client.match_phone_to_national_code('4737543783', '09748356374')
        self.assertFalse(result.is_matched)
