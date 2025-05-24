class User:
    def __init__(self, name: str, email: str, password: str):
        self._name = name
        self._email = email
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password