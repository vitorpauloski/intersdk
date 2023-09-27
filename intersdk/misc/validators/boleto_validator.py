from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intersdk.cobranca import Boleto

from datetime import date, timedelta

from intersdk.cobranca.components import ComponenteFinanceiro, Pessoa
from intersdk.misc.exceptions import BoletoJaEmitido

from .componente_financeiro_validator import ComponenteFinanceiroValidator
from .pessoa_validator import PessoaValidator


class BoletoValidator:
    def __init__(self, boleto: "Boleto") -> None:
        self.boleto = boleto

    def validate_emitido(self) -> None:
        if self.boleto.emitido:
            raise BoletoJaEmitido

    def validate_seu_numero(self) -> None:
        if not isinstance(self.boleto.seu_numero, str):
            raise TypeError("seu_numero deve ser uma string")
        if not self.boleto.seu_numero.isnumeric():
            raise ValueError("seu_numero deve ser numérico")
        if len(self.boleto.seu_numero) < 1:
            raise ValueError("seu_numero deve ter pelo menos 1 caractere")
        if len(self.boleto.seu_numero) > 15:
            raise ValueError("seu_numero deve ter no máximo 15 caracteres")

    def validate_valor_nominal(self) -> None:
        if not isinstance(self.boleto.valor_nominal, (int, float)):
            raise TypeError("valor_nominal deve ser um inteiro ou float")
        if len(str(float(self.boleto.valor_nominal)).split(".")[1]) > 2:
            raise ValueError("valor_nominal deve ter no máximo 2 casas decimais")
        if self.boleto.valor_nominal < 2.5:
            raise ValueError("valor_nominal deve ser maior ou igual a 2.5")

    def validate_data_vencimento(self) -> None:
        if not isinstance(self.boleto.data_vencimento, date):
            raise TypeError("data_vencimento deve ser do tipo date")
        if self.boleto.data_vencimento < date.today():
            raise ValueError("data_vencimento deve ser maior ou igual a data atual")
        if self.boleto.data_vencimento > date.today() + timedelta(1000):
            raise ValueError("data_vencimento deve ser menor ou igual a data atual + 1000 dias")

    def validate_num_dias_agenda(self) -> None:
        if not isinstance(self.boleto.num_dias_agenda, int):
            raise TypeError("num_dias_agenda deve ser um inteiro")
        if self.boleto.num_dias_agenda > 60:
            raise ValueError("num_dias_agenda deve ser menor ou igual a 60")

    def validate_pagador(self) -> None:
        if not isinstance(self.boleto.pagador, Pessoa):
            raise TypeError("pagador deve ser uma instância de Pessoa")
        PessoaValidator(self.boleto.pagador).validate()

    def validate_beneficiario_final(self) -> None:
        if self.boleto.beneficiario_final is None:
            return
        if not isinstance(self.boleto.beneficiario_final, Pessoa):
            raise TypeError("beneficiario_final deve ser uma instância de Pessoa")
        PessoaValidator(self.boleto.beneficiario_final).validate()

    def validate_mensagem(self) -> None:
        if self.boleto.mensagem is None:
            return
        if not isinstance(self.boleto.mensagem, (list, tuple)):
            raise TypeError("mensagem deve ser uma lista ou tupla")
        if len(self.boleto.mensagem) < 1:
            raise ValueError("mensagem deve ter pelo menos 1 linha")
        if len(self.boleto.mensagem) > 5:
            raise ValueError("mensagem deve ter no máximo 5 linhas")
        for linha in self.boleto.mensagem:
            if not isinstance(linha, str):
                raise TypeError("cada linha de mensagem deve ser uma string")
            if len(linha) < 1:
                raise ValueError("cada linha de mensagem deve ter pelo menos 1 caractere")
            if len(linha) > 78:
                raise ValueError("cada linha de mensagem deve ter no máximo 78 caracteres")

    def validate_descontos(self) -> None:
        if self.boleto.descontos is None:
            return
        if not isinstance(self.boleto.descontos, (list, tuple)):
            raise TypeError("descontos deve ser uma lista ou tupla")
        if len(self.boleto.descontos) < 1:
            raise ValueError("descontos deve ter pelo menos 1 componente financeiro")
        if len(self.boleto.descontos) > 3:
            raise ValueError("descontos deve ter no máximo 3 componentes financeiros")
        for desconto in self.boleto.descontos:
            if not isinstance(desconto, ComponenteFinanceiro):
                raise TypeError("cada item de descontos deve ser uma instância de ComponenteFinanceiro")
            ComponenteFinanceiroValidator(desconto).validate()
            if desconto.data > self.boleto.data_vencimento:
                raise ValueError("a data de desconto deve ser menor ou igual a data de vencimento")
        if len(self.boleto.descontos) > 1:
            for desconto in self.boleto.descontos:
                if desconto.tipo != self.boleto.descontos[0].tipo:
                    raise ValueError("todos os descontos devem ser do mesmo tipo")

    def validate_multa(self) -> None:
        if self.boleto.multa is None:
            return
        if not isinstance(self.boleto.multa, ComponenteFinanceiro):
            raise TypeError("multa deve ser uma instância de ComponenteFinanceiro")
        ComponenteFinanceiroValidator(self.boleto.multa).validate()
        if self.boleto.multa.data <= self.boleto.data_vencimento:
            raise ValueError("a data de multa deve ser maior que a data de vencimento")
        if self.boleto.multa.data > self.boleto.data_limite:
            raise ValueError("a data de multa deve ser menor ou igual a data limite")

    def validate_mora(self) -> None:
        if self.boleto.mora is None:
            return
        if not isinstance(self.boleto.mora, ComponenteFinanceiro):
            raise TypeError("mora deve ser uma instância de ComponenteFinanceiro")
        ComponenteFinanceiroValidator(self.boleto.mora).validate()
        if self.boleto.mora.data <= self.boleto.data_vencimento:
            raise ValueError("a data de mora deve ser maior que a data de vencimento")
        if self.boleto.mora.data > self.boleto.data_limite:
            raise ValueError("a data de mora deve ser menor ou igual a data limite")

    def validate(self) -> None:
        self.validate_emitido()
        self.validate_seu_numero()
        self.validate_valor_nominal()
        self.validate_data_vencimento()
        self.validate_num_dias_agenda()
        self.validate_pagador()
        self.validate_beneficiario_final()
        self.validate_mensagem()
        self.validate_descontos()
        self.validate_multa()
        self.validate_mora()
