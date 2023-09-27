from datetime import datetime, timedelta, timezone
from urllib import parse

import loguru
import requests
from requests.exceptions import SSLError

from intersdk.misc.typing import TokenScope

from .token import Token


class Autenticacao:
    def __init__(self, certificate_path: str, private_key_path: str, client_id: str, client_secret: str) -> None:
        self.certificate_path = certificate_path
        self.private_key_path = private_key_path
        self.client_id = client_id
        self.client_secret = client_secret
        self.__token: Token | None = None

    @staticmethod
    def __dict_to_token(data: dict) -> Token:
        return Token(
            token_type=data["token_type"],
            access_token=data["access_token"],
            scope=data["scope"].split(),
            expires_in=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=data["expires_in"]),
        )

    def __request_token(self, scope: list[TokenScope]) -> dict:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": " ".join(scope),
        }
        loguru.logger.info(f"Obtendo token de acesso com escopo {scope}")
        try:
            response = requests.post(
                url="https://cdpj.partners.bancointer.com.br/oauth/v2/token",
                data=parse.urlencode(data),
                cert=(self.certificate_path, self.private_key_path),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )
        except SSLError as error:
            loguru.logger.error("Erro de SSL: verifique se o certificado e a chave privada estão corretos")
            raise error
        if not response.ok:
            loguru.logger.error(f"Erro ao obter token de acesso: {response.text}")
            response.raise_for_status()
        loguru.logger.debug(f"Resposta da requisição: {response.text}")
        return response.json()

    def token(self, scope: list[TokenScope]) -> Token:
        old_scope: list[TokenScope] | None = None
        request_scope: list[TokenScope] | None = None
        if self.__token is not None:
            if not self.__token.expired:
                if all(item in self.__token.scope for item in scope):
                    return self.__token
                loguru.logger.info("Token de acesso já existe, mas não abrange o escopo solicitado")
                old_scope = self.__token.scope
                request_scope = list(set(self.__token.scope + scope))
            else:
                loguru.logger.info("Token de acesso já existe, mas está expirado")
                self.__token = None
        else:
            loguru.logger.info("Token de acesso não existe")
        request_scope = scope if request_scope is None else request_scope
        new_token = self.__dict_to_token(self.__request_token(request_scope))
        if not all(item in new_token.scope for item in scope):
            loguru.logger.error("Erro ao obter token de acesso: escopo solicitado não foi concedido")
            raise AssertionError("escopo solicitado não foi concedido")
        if old_scope is not None and not all(item in new_token.scope for item in old_scope):
            loguru.logger.warning("Escopo anterior não foi concedido e será substituído pelo novo escopo")
        loguru.logger.success("Token de acesso obtido com sucesso")
        self.__token = new_token
        return self.__token
