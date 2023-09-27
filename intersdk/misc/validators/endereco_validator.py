from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intersdk.cobranca import Endereco

import typing

from intersdk.misc.typing import Uf


class EnderecoValidator:
    def __init__(self, endereco: "Endereco") -> None:
        self.endereco = endereco

    def validate_logradouro(self) -> None:
        if not isinstance(self.endereco.logradouro, str):
            raise TypeError("logradouro deve ser uma string")
        if len(self.endereco.logradouro) < 1:
            raise ValueError("logradouro deve conter ao menos 1 caractere")
        if len(self.endereco.logradouro) > 100:
            raise ValueError("logradouro deve conter até 100 caracteres")

    def validate_numero(self) -> None:
        if not isinstance(self.endereco.numero, str):
            raise TypeError("numero deve ser uma string")
        if len(self.endereco.numero) < 1:
            raise ValueError("numero deve conter ao menos 1 caractere")
        if len(self.endereco.numero) > 10:
            raise ValueError("numero deve conter até 10 caracteres")

    def validate_bairro(self) -> None:
        if not isinstance(self.endereco.bairro, str):
            raise TypeError("bairro deve ser uma string")
        if len(self.endereco.bairro) < 1:
            raise ValueError("bairro deve conter ao menos 1 caractere")
        if len(self.endereco.bairro) > 60:
            raise ValueError("bairro deve conter até 60 caracteres")

    def validate_cidade(self) -> None:
        if not isinstance(self.endereco.cidade, str):
            raise TypeError("cidade deve ser uma string")
        if len(self.endereco.cidade) < 1:
            raise ValueError("cidade deve conter ao menos 1 caractere")
        if len(self.endereco.cidade) > 60:
            raise ValueError("cidade deve conter até 60 caracteres")

    def validate_estado(self) -> None:
        uf_list = list(typing.get_args(Uf))
        if not isinstance(self.endereco.estado, str):
            raise TypeError("estado deve ser uma string")
        if self.endereco.estado not in uf_list:
            raise ValueError(f"estado deve ser uma das opções: {uf_list}")

    def validate_cep(self) -> None:
        if not isinstance(self.endereco.cep, str):
            raise TypeError("cep deve ser uma string")
        if not self.endereco.cep.isnumeric():
            raise ValueError("cep deve conter apenas números")
        if len(self.endereco.cep) != 8:
            raise ValueError("cep deve conter 8 caracteres")

    def validate_complemento(self) -> None:
        if self.endereco.complemento is None:
            return
        if not isinstance(self.endereco.complemento, str):
            raise TypeError("complemento deve ser uma string")
        if len(self.endereco.complemento) < 1:
            raise ValueError("complemento deve conter ao menos 1 caractere")
        if len(self.endereco.complemento) > 30:
            raise ValueError("complemento deve conter até 30 caracteres")

    def validate(self) -> None:
        self.validate_logradouro()
        self.validate_numero()
        self.validate_bairro()
        self.validate_cidade()
        self.validate_estado()
        self.validate_cep()
        self.validate_complemento()
