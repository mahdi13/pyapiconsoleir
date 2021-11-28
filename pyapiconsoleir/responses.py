class BaseApiconsoleResponse:
    def __init__(self, payload):
        self.payload = payload

    def __repr__(self) -> str:
        return str(self.payload)


class PostalCodeToAddress(BaseApiconsoleResponse):

    @property
    def postal_code(self):
        return self.payload.get('postalCode', None)

    @property
    def address(self):
        return self.payload.get('address', None)
