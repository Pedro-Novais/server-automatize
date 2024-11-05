class PaymentsExceptions(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class HeaderInvalid(PaymentsExceptions):
    def __init__(
            self, 
            message: str = "Acesso negado!",
    ):
        super().__init__(message, status_code=403)

class ErrorToSaveData(PaymentsExceptions):
    def __init__(
            self, 
            message: str = "Erro ao salvar dados no gateway de pagamentos!",
    ):
        super().__init__(message, status_code=400)

class CardsNotFound(PaymentsExceptions):
    def __init__(
            self, 
            message: str = "Nenhum cartão foi encontrado!",
    ):
        super().__init__(message, status_code=404)