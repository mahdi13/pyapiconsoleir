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


class MatchPhoneToNationalCode(BaseApiconsoleResponse):

    @property
    def is_matched(self) -> bool:
        return self.payload.get('matched', False) is True


class IdentityInquiry(BaseApiconsoleResponse):

    @property
    def national_code(self) -> str:
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('nationalCode', None)
        return str(result) if result is not None else None

    @property
    def first_name(self) -> str:
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('firstName', None)
        return str(result) if result is not None else None

    @property
    def last_name(self) -> str:
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('lastName', None)
        return str(result) if result is not None else None

    @property
    def father_name(self) -> str:
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('fatherName', None)
        return str(result) if result is not None else None

    @property
    def birth_date(self) -> str:
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('birthDate', None)
        return str(result) if result is not None else None

    @property
    def alive(self) -> bool:
        return (self.payload.get('identityInfo', None) and
                self.payload.get('identityInfo', None).get('alive', None)) is True

    @property
    def gender(self) -> str:  # MALE or FEMALE
        result = \
            self.payload.get('identityInfo', None) and self.payload.get('identityInfo', None).get('gender', None)
        return str(result) if result is not None else None
