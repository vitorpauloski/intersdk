from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from intersdk.cobranca import Cobranca

from intersdk.misc.exceptions import (
    BoletoJaEmitido,
    BoletoNaoAtualizado,
    BoletoNaoEmitido,
)
from intersdk.misc.typing import MotivoCancelamento, TipoSituacao

from .componente_financeiro import ComponenteFinanceiro
from .pessoa import Pessoa


class Boleto:
    def __init__(
        self,
        seu_numero: str,
        valor_nominal: int | float,
        data_vencimento: date,
        num_dias_agenda: int,
        pagador: Pessoa,
        beneficiario_final: Pessoa | None = None,
        mensagem: Sequence[str] | None = None,
        descontos: Sequence[ComponenteFinanceiro] | None = None,
        multa: ComponenteFinanceiro | None = None,
        mora: ComponenteFinanceiro | None = None,
    ) -> None:
        self.__emitido = False
        self.__atualizado = False
        self.__seu_numero = seu_numero
        self.__valor_nominal = valor_nominal
        self.__data_vencimento = data_vencimento
        self.__num_dias_agenda = num_dias_agenda
        self.__pagador = pagador
        self.__beneficiario_final = beneficiario_final
        self.__mensagem = mensagem
        self.__descontos = descontos
        self.__multa = multa
        self.__mora = mora
        self.__nosso_numero: str | None = None
        self.__codigo_barras: str | None = None
        self.__linha_digitavel: str | None = None
        self.__data_emissao: date | None = None
        self.__data_hora_atualizacao: datetime | None = None
        self.__situacao: TipoSituacao | None = None
        self.__data_situacao: date | None = None
        self.__origem: str | None = None
        self.__conta_corrente: str | None = None
        self.__codigo_especie: str | None = None
        self.__valor_total_recebimento: int | float | None = None
        self.__motivo_cancelamento: MotivoCancelamento | None = None

    @property
    def emitido(self) -> bool:
        return self.__emitido

    @property
    def atualizado(self) -> bool:
        return self.__atualizado

    @property
    def seu_numero(self) -> str:
        return self.__seu_numero

    @seu_numero.setter
    def seu_numero(self, seu_numero: str) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__seu_numero = seu_numero

    @property
    def valor_nominal(self) -> int | float:
        return self.__valor_nominal

    @valor_nominal.setter
    def valor_nominal(self, valor_nominal: int | float) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__valor_nominal = valor_nominal

    @property
    def data_vencimento(self) -> date:
        return self.__data_vencimento

    @data_vencimento.setter
    def data_vencimento(self, data_vencimento: date) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__data_vencimento = data_vencimento

    @property
    def num_dias_agenda(self) -> int:
        return self.__num_dias_agenda

    @num_dias_agenda.setter
    def num_dias_agenda(self, num_dias_agenda: int) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__num_dias_agenda = num_dias_agenda

    @property
    def pagador(self) -> Pessoa:
        return self.__pagador

    @pagador.setter
    def pagador(self, pagador: Pessoa) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__pagador = pagador

    @property
    def beneficiario_final(self) -> Pessoa | None:
        return self.__beneficiario_final

    @beneficiario_final.setter
    def beneficiario_final(self, beneficiario_final: Pessoa | None) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__beneficiario_final = beneficiario_final

    @property
    def mensagem(self) -> Sequence[str] | None:
        return self.__mensagem

    @mensagem.setter
    def mensagem(self, mensagem: Sequence[str] | None) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__mensagem = mensagem

    @property
    def descontos(self) -> Sequence[ComponenteFinanceiro] | None:
        return self.__descontos

    @descontos.setter
    def descontos(self, descontos: Sequence[ComponenteFinanceiro] | None) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__descontos = descontos

    @property
    def multa(self) -> ComponenteFinanceiro | None:
        return self.__multa

    @multa.setter
    def multa(self, multa: ComponenteFinanceiro | None) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__multa = multa

    @property
    def mora(self) -> ComponenteFinanceiro | None:
        return self.__mora

    @mora.setter
    def mora(self, mora: ComponenteFinanceiro | None) -> None:
        if self.__emitido:
            raise BoletoJaEmitido
        self.__mora = mora

    @property
    def data_limite(self) -> date:
        return self.__data_vencimento + timedelta(self.__num_dias_agenda)

    @property
    def nosso_numero(self) -> str:
        if not self.__emitido or not self.__nosso_numero:
            raise BoletoNaoEmitido
        return self.__nosso_numero

    @property
    def codigo_barras(self) -> str:
        if not self.__emitido or not self.__codigo_barras:
            raise BoletoNaoEmitido
        return self.__codigo_barras

    @property
    def linha_digitavel(self) -> str:
        if not self.__emitido or not self.__linha_digitavel:
            raise BoletoNaoEmitido
        return self.__linha_digitavel

    @property
    def data_emissao(self) -> date:
        if not self.__atualizado or not self.__data_emissao:
            raise BoletoNaoAtualizado
        return self.__data_emissao

    @property
    def data_hora_atualizacao(self) -> datetime:
        if not self.__atualizado or not self.__data_hora_atualizacao:
            raise BoletoNaoAtualizado
        return self.__data_hora_atualizacao

    @property
    def situacao(self) -> TipoSituacao:
        if not self.__atualizado or not self.__situacao:
            raise BoletoNaoAtualizado
        return self.__situacao

    @property
    def data_situacao(self) -> date:
        if not self.__atualizado or not self.__data_situacao:
            raise BoletoNaoAtualizado
        return self.__data_situacao

    @property
    def origem(self) -> str:
        if not self.__atualizado or not self.__origem:
            raise BoletoNaoAtualizado
        return self.__origem

    @property
    def conta_corrente(self) -> str:
        if not self.__atualizado or not self.__conta_corrente:
            raise BoletoNaoAtualizado
        return self.__conta_corrente

    @property
    def codigo_especie(self) -> str:
        if not self.__atualizado or not self.__codigo_especie:
            raise BoletoNaoAtualizado
        return self.__codigo_especie

    @property
    def valor_total_recebimento(self) -> int | float | None:
        if not self.__atualizado:
            raise BoletoNaoAtualizado
        return self.__valor_total_recebimento

    @property
    def motivo_cancelamento(self) -> MotivoCancelamento | None:
        if not self.__atualizado:
            raise BoletoNaoAtualizado
        return self.__motivo_cancelamento

    def set_emissao(self, cobranca: "Cobranca") -> None:
        data = cobranca.boletos_emitidos[self.__seu_numero]
        self.__nosso_numero = data["nossoNumero"]
        self.__codigo_barras = data["codigoBarras"]
        self.__linha_digitavel = data["linhaDigitavel"]
        self.__emitido = True

    def set_atualizacao(self, cobranca: "Cobranca") -> None:
        data = cobranca.boletos_emitidos[self.__seu_numero]
        data_hora_situacao = datetime.fromisoformat(data["dataHoraSituacao"]) + timedelta(hours=3)
        self.__data_emissao = date.fromisoformat(data["dataEmissao"])
        self.__situacao = data["situacao"]
        self.__data_situacao = data_hora_situacao.date()
        self.__origem = data["origem"]
        self.__conta_corrente = data["contaCorrente"]
        self.__codigo_especie = data["codigoEspecie"]
        self.__valor_total_recebimento = data.get("valorTotalRecebimento") or None
        self.__motivo_cancelamento = data.get("motivoCancelamento") or None
        self.__data_hora_atualizacao = datetime.now(timezone.utc).replace(tzinfo=None)
        self.__atualizado = True

    def to_dict(self) -> dict[str, str | float | int | dict | None]:
        mensagem = (
            {f"linha{i + 1}": self.__mensagem[i] if i < len(self.__mensagem) else None for i in range(5)}
            if self.__mensagem is not None
            else None
        )
        multa = self.__multa.to_dict("MULTA") if self.__multa is not None else ComponenteFinanceiro.empty_dict("MULTA")
        mora = self.__mora.to_dict("MORA") if self.__mora is not None else ComponenteFinanceiro.empty_dict("MORA")
        descontos = {f"desconto{i + 1}": ComponenteFinanceiro.empty_dict("DESCONTO") for i in range(3)}
        if self.__descontos is not None:
            descontos = {
                f"desconto{i + 1}": self.__descontos[i].to_dict("DESCONTO")
                if i < len(self.__descontos)
                else ComponenteFinanceiro.empty_dict("DESCONTO")
                for i in range(3)
            }
        return {
            "seuNumero": self.__seu_numero,
            "valorNominal": self.__valor_nominal,
            "dataVencimento": self.__data_vencimento.strftime("%Y-%m-%d"),
            "numDiasAgenda": self.__num_dias_agenda,
            "pagador": self.__pagador.to_dict(),
            "mensagem": mensagem,
            "desconto1": None,
            "desconto2": None,
            "desconto3": None,
            "multa": multa,
            "mora": mora,
            "beneficiarioFinal": self.__beneficiario_final.to_dict() if self.__beneficiario_final else None,
        } | descontos

    @classmethod
    def from_dict(cls, data: dict) -> "Boleto":
        descontos = [
            componente
            for componente in [
                ComponenteFinanceiro.from_dict(data[desconto]) for desconto in ("desconto1", "desconto2", "desconto3")
            ]
            if componente is not None
        ] or None
        return cls(
            seu_numero=data["seuNumero"],
            valor_nominal=data["valorNominal"],
            data_vencimento=date.fromisoformat(data["dataVencimento"]),
            num_dias_agenda=(date.fromisoformat(data["dataLimite"]) - date.fromisoformat(data["dataVencimento"])).days,
            pagador=Pessoa.from_dict(data["pagador"]),
            beneficiario_final=Pessoa.from_dict(data["beneficiarioFinal"]) if data.get("beneficiarioFinal") else None,
            mensagem=[linha for linha in list(data["mensagem"].values()) if linha] or None,
            descontos=descontos,
            multa=ComponenteFinanceiro.from_dict(data["multa"]),
            mora=ComponenteFinanceiro.from_dict(data["mora"]),
        )
