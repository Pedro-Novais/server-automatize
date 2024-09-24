class OperationsDatabaseException(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class OperationAggregationFailed(OperationsDatabaseException):
    def __init__(
            self, 
            message: str = "Operação de agregação na consulta do banco de dados falhou!",
    ):
        super().__init__(message, status_code=500)