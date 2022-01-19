from pyapiconsoleir.tests.helper import ApiClientTestCase
from pyapiconsoleir.tests.mock_api_server import valid_mock_national_code, valid_mock_birth_date


class IdentityInquiryTestCase(ApiClientTestCase):

    def test_identity_inquiry(self):
        result = self.api_client.identity_inquiry(valid_mock_national_code, valid_mock_birth_date)
        self.assertEqual('تست', result.first_name)
        self.assertEqual('تست', result.last_name)
        self.assertEqual('تست', result.father_name)
        self.assertEqual('13600101', result.birth_date)
        self.assertEqual('1111111111', result.national_code)
        self.assertTrue(result.alive)
