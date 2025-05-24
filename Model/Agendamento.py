class Agendamento:
    def __init__(self, nome: str, data: str, horario: str, endereco: str):
        self._nome = nome
        self._data = data
        self._horario = horario
        self._endereco = endereco

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