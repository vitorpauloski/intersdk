class BoletoJaEmitido(Exception):
    def __init__(self) -> None:
        super().__init__("O boleto já foi emitido")


class BoletoNaoEmitido(Exception):
    def __init__(self) -> None:
        super().__init__("O boleto ainda não foi emitido")


class BoletoNaoAtualizado(Exception):
    def __init__(self) -> None:
        super().__init__("O boleto não foi atualizado")
