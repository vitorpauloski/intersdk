from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intersdk.cobranca import ComponenteFinanceiro

from datetime import date


class ComponenteFinanceiroValidator:
    def __init__(self, componente_financeiro: "ComponenteFinanceiro") -> None:
        self.componente_financeiro = componente_financeiro

    def validate_tipo(self) -> None:
        tipo_list = ["TAXA", "VALOR"]
        if not isinstance(self.componente_financeiro.tipo, str):
            raise TypeError("tipo deve ser uma string")
        if self.componente_financeiro.tipo not in tipo_list:
            raise ValueError(f"tipo deve ser uma das opções: {tipo_list}")

    def validate_data(self) -> None:
        if not isinstance(self.componente_financeiro.data, date):
            raise TypeError("data deve ser do tipo date")
        if self.componente_financeiro.data < date.today():
            raise ValueError("data deve ser maior ou igual a data atual")

    def validate_taxa_valor(self) -> None:
        if not isinstance(self.componente_financeiro.taxa_valor, (int, float)):
            raise TypeError("taxa_valor deve ser um inteiro ou float")
        if len(str(float(self.componente_financeiro.taxa_valor)).split(".")[1]) > 2:
            raise ValueError("taxa_valor deve ter no máximo 2 casas decimais")
        if self.componente_financeiro.taxa_valor < 0.01:
            raise ValueError("taxa_valor deve ser maior ou igual a 0.01")
        if self.componente_financeiro.tipo == "TAXA" and self.componente_financeiro.taxa_valor >= 100:
            raise ValueError("taxa deve ser menor que 100")

    def validate(self) -> None:
        self.validate_tipo()
        self.validate_data()
        self.validate_taxa_valor()
