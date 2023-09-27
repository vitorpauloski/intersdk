from dataclasses import dataclass

from intersdk.misc.typing import Uf


@dataclass
class Endereco:
    logradouro: str
    numero: str | None
    bairro: str
    cidade: str
    estado: Uf
    cep: str
    complemento: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "endereco": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.estado,
            "cep": self.cep,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Endereco":
        return cls(
            logradouro=data["endereco"],
            numero=data.get("numero"),
            bairro=data["bairro"],
            cidade=data["cidade"],
            estado=data["uf"],
            cep=data["cep"],
            complemento=data.get("complemento") or None,
        )
