from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass
class ComponenteFinanceiro:
    tipo: Literal["TAXA", "VALOR"]
    data: date
    taxa_valor: int | float

    @staticmethod
    def empty_dict(_type: Literal["DESCONTO", "MULTA", "MORA"]) -> dict[str, str | int | float]:
        data = {}
        if _type == "DESCONTO":
            data["codigoDesconto"] = "NAOTEMDESCONTO"
        elif _type == "MULTA":
            data["codigoMulta"] = "NAOTEMMULTA"
        elif _type == "MORA":
            data["codigoMora"] = "ISENTO"
        return data | {"taxa": 0, "valor": 0}

    def to_dict(self, _type: Literal["DESCONTO", "MULTA", "MORA"]) -> dict[str, str | int | float]:
        data = {}
        if _type == "DESCONTO":
            data["codigoDesconto"] = "PERCENTUALDATAINFORMADA" if self.tipo == "TAXA" else "VALORFIXODATAINFORMADA"
        elif _type == "MULTA":
            data["codigoMulta"] = "PERCENTUAL" if self.tipo == "TAXA" else "VALORFIXO"
        elif _type == "MORA":
            data["codigoMora"] = "TAXAMENSAL" if self.tipo == "TAXA" else "VALORDIA"
        return data | {
            "data": self.data.strftime("%Y-%m-%d"),
            "taxa": self.taxa_valor if self.tipo == "TAXA" else 0,
            "valor": self.taxa_valor if self.tipo == "VALOR" else 0,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ComponenteFinanceiro | None":
        if data["codigo"] in ("NAOTEMDESCONTO", "NAOTEMMULTA", "ISENTO"):
            return None
        tipo: Literal["TAXA", "VALOR"] = (
            "TAXA" if data["codigo"] in ("PERCENTUALDATAINFORMADA", "PERCENTUAL", "TAXAMENSAL") else "VALOR"
        )
        return cls(
            tipo=tipo,
            data=date.fromisoformat(data["data"]),
            taxa_valor=data["taxa"] if tipo == "TAXA" else data["valor"],
        )
