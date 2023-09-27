import base64
import typing
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import loguru
import requests

if TYPE_CHECKING:
    from intersdk.autenticacao import Autenticacao

from intersdk.misc.typing import MotivoCancelamento
from intersdk.misc.validators import BoletoValidator, PathValidator

from .components import Boleto


class Cobranca:
    def __init__(self, autenticacao: "Autenticacao") -> None:
        self.__autenticacao = autenticacao
        self.__boletos_emitidos: dict = {}

    @property
    def boletos_emitidos(self) -> dict:
        return self.__boletos_emitidos

    def __request_recuperar_boleto(self, nosso_numero: str, _type: Literal["DATA", "PDF"] = "DATA") -> dict:
        url = f"https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/{nosso_numero}"
        if _type == "PDF":
            url += "/pdf"
            loguru.logger.info(f"Recuperando PDF do boleto {nosso_numero}")
        else:
            loguru.logger.info(f"Recuperando dados do boleto {nosso_numero}")
        response = requests.get(
            url=url,
            headers={"Authorization": self.__autenticacao.token(["boleto-cobranca.read"]).authorization_header},
            cert=(self.__autenticacao.certificate_path, self.__autenticacao.private_key_path),
            timeout=30,
        )
        if not response.ok:
            loguru.logger.error(f"Erro ao recuperar boleto {nosso_numero}: {response.text}")
            response.raise_for_status()
        loguru.logger.debug(f"Resposta da requisição: {response.text}")
        return response.json()

    def __request_emitir_boleto(self, boleto: dict) -> dict:
        loguru.logger.info(f"Emitindo boleto {boleto['seuNumero']}")
        response = requests.post(
            url="https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos",
            headers={"Authorization": self.__autenticacao.token(["boleto-cobranca.write"]).authorization_header},
            cert=(self.__autenticacao.certificate_path, self.__autenticacao.private_key_path),
            json=boleto,
            timeout=30,
        )
        if not response.ok:
            loguru.logger.error(f"Erro ao emitir boleto {boleto['seuNumero']}: {response.text}")
            response.raise_for_status()
        loguru.logger.debug(f"Resposta da requisição: {response.text}")
        return response.json()

    def __request_cancelar_boleto(self, nosso_numero: str, motivo: MotivoCancelamento) -> None:
        loguru.logger.info(f"cancelando boleto {nosso_numero}")
        response = requests.post(
            url=f"https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/{nosso_numero}/cancelar",
            headers={"Authorization": self.__autenticacao.token(["boleto-cobranca.write"]).authorization_header},
            cert=(self.__autenticacao.certificate_path, self.__autenticacao.private_key_path),
            json={"motivoCancelamento": motivo},
            timeout=30,
        )
        if not response.ok:
            loguru.logger.error(f"Erro ao cancelar boleto {nosso_numero}: {response.text}")
            response.raise_for_status()
        loguru.logger.debug(f"Resposta da requisição: {response.text}")

    def recuperar_boleto(self, nosso_numero: str) -> Boleto:
        response = self.__request_recuperar_boleto(nosso_numero)
        boleto = Boleto.from_dict(response)
        self.__boletos_emitidos[boleto.seu_numero] = response
        boleto.set_emissao(self)
        boleto.set_atualizacao(self)
        self.__boletos_emitidos.pop(boleto.seu_numero)
        loguru.logger.success(f"Boleto {nosso_numero} recuperado com sucesso")
        return boleto

    def recuperar_boleto_pdf(self, nosso_numero: str, file_path: str) -> None:
        path = Path(file_path)
        PathValidator(path, must_exist=False, extension=".pdf").validate()
        response = self.__request_recuperar_boleto(nosso_numero, _type="PDF")
        path.write_bytes(base64.b64decode(response["pdf"]))
        loguru.logger.success(f"Boleto {nosso_numero} salvo em {path.absolute()}")

    def emitir_boleto(self, boleto: Boleto) -> None:
        BoletoValidator(boleto).validate()
        response = self.__request_emitir_boleto(boleto.to_dict())
        loguru.logger.success(f"Boleto {boleto.seu_numero} emitido com sucesso")
        self.__boletos_emitidos[boleto.seu_numero] = response
        boleto.set_emissao(self)
        self.__boletos_emitidos.pop(boleto.seu_numero)

    def cancelar_boleto(self, nosso_numero: str, motivo: MotivoCancelamento) -> None:
        motivos_cancelamento = typing.get_args(MotivoCancelamento)
        if motivo not in motivos_cancelamento:
            raise ValueError(f"Motivo de cancelamento deve ser um dos seguintes: {motivos_cancelamento}")
        self.__request_cancelar_boleto(nosso_numero, motivo)
        loguru.logger.success(f"Boleto {nosso_numero} cancelado com sucesso")
