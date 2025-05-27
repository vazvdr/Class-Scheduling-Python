class Agendamento:
    def __init__(self, nome: str, data: str, horario: str, endereco: str, professor: str, id: int = None):
        self._id = id
        self._nome = nome
        self._data = data
        self._horario = horario
        self._endereco = endereco
        self._professor = professor

    # Getter e Setter para id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
    # Getter e Setter para nome
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    # Getter e Setter para data
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    # Getter e Setter para horario
    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, value):
        self._horario = value

    # Getter e Setter para endereco
    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    # Getter e Setter para professor
    @property
    def professor(self):
        return self._professor

    @professor.setter
    def professor(self, value):
        self._professor = value
