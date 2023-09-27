from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intersdk.cobranca import Pessoa

from validate_docbr import CNPJ, CPF  # type: ignore

from intersdk.cobranca.components import Endereco

from .endereco_validator import EnderecoValidator


class PessoaValidator:
    def __init__(self, pessoa: "Pessoa") -> None:
        self.pessoa = pessoa

    def validate_tipo(self) -> None:
        tipo_list = ["FISICA", "JURIDICA"]
        if not isinstance(self.pessoa.tipo, str):
            raise TypeError("tipo deve ser uma string")
        if self.pessoa.tipo not in tipo_list:
            raise ValueError(f"tipo deve ser uma das opções: {tipo_list}")

    def validate_cpf_cnpj(self) -> None:
        if not isinstance(self.pessoa.cpf_cnpj, str):
            raise TypeError("cpf_cnpj deve ser uma string")
        if self.pessoa.tipo == "FISICA" and not CPF().validate(self.pessoa.cpf_cnpj):
            raise ValueError("cpf deve ser válido")
        if self.pessoa.tipo == "JURIDICA" and not CNPJ().validate(self.pessoa.cpf_cnpj):
            raise ValueError("cnpj deve ser válido")

    def validate_nome(self) -> None:
        if not isinstance(self.pessoa.nome, str):
            raise TypeError("nome deve ser uma string")
        if len(self.pessoa.nome) < 1:
            raise ValueError("nome deve conter ao menos 1 caractere")
        if len(self.pessoa.nome) > 100:
            raise ValueError("nome deve conter até 100 caracteres")

    def validate_endereco(self) -> None:
        if not isinstance(self.pessoa.endereco, Endereco):
            raise TypeError("endereco deve ser uma instância de Endereco")
        EnderecoValidator(self.pessoa.endereco).validate()

    def validate_email(self) -> None:
        if self.pessoa.email is None:
            return
        if not isinstance(self.pessoa.email, str):
            raise TypeError("email deve ser uma string")
        if len(self.pessoa.email) < 1:
            raise ValueError("email deve conter ao menos 1 caractere")
        if len(self.pessoa.email) > 50:
            raise ValueError("email deve conter até 50 caracteres")

    def validate_telefone(self) -> None:
        if self.pessoa.telefone is None:
            return
        if not isinstance(self.pessoa.telefone, str):
            raise TypeError("telefone deve ser uma string")
        if not self.pessoa.telefone.isnumeric():
            raise ValueError("telefone deve conter apenas números")
        if len(self.pessoa.telefone) not in (10, 11):
            raise ValueError("telefone deve conter 10 ou 11 dígitos")

    def validate(self) -> None:
        self.validate_tipo()
        self.validate_cpf_cnpj()
        self.validate_nome()
        self.validate_endereco()
        self.validate_email()
        self.validate_telefone()
