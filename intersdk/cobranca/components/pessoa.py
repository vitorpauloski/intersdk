from dataclasses import dataclass
from typing import Literal

from .endereco import Endereco


@dataclass
class Pessoa:
    tipo: Literal["FISICA", "JURIDICA"]
    cpf_cnpj: str
    nome: str
    endereco: Endereco | None = None
    email: str | None = None
    telefone: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "cpfCnpj": self.cpf_cnpj,
            "tipoPessoa": self.tipo,
            "nome": self.nome,
            "endereco": None,
            "numero": None,
            "complemento": None,
            "bairro": None,
            "cidade": None,
            "uf": None,
            "cep": None,
            "email": self.email,
            "ddd": self.telefone[:2] if self.telefone is not None else None,
            "telefone": self.telefone[2:] if self.telefone is not None else None,
        } | (self.endereco.to_dict() if self.endereco is not None else {})

    @classmethod
    def from_dict(cls, data: dict) -> "Pessoa":
        return cls(
            tipo=data["tipoPessoa"],
            cpf_cnpj=data["cpfCnpj"],
            nome=data["nome"],
            endereco=Endereco.from_dict(data) if data.get("endereco") else None,
            email=data.get("email") or None,
            telefone=f"{data['ddd']}{data['telefone']}" if data.get("telefone") else None,
        )
