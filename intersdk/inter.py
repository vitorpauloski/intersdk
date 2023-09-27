from .autenticacao import Autenticacao
from .cobranca import Cobranca


class Inter:
    def __init__(self, autenticacao: Autenticacao) -> None:
        self.autenticacao = autenticacao
        self.cobranca = Cobranca(self.autenticacao)
