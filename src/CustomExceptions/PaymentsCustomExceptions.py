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