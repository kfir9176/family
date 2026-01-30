class Person:
    def __init__(
        self,
        id,
        name,
        family,
        birthday="לא ידוע",
        phone="לא ידוע",
        address="לא ידוע",
        family_id=None,
    ):
        self.id = id
        self.name = name
        self.family = family
        self.birthday = birthday
        self.phone = phone
        self.address = address
        self.family_id = family_id
