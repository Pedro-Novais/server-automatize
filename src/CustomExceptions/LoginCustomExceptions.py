class LoginException(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserNotFound(LoginException):
    def __init__(
            self, 
            message: str = "Usuário não registrado",
    ):
        super().__init__(message, status_code=404)

class UserCredentialsInvalids(LoginException):
       def __init__(
            self, 
            message: str = "Credenciais incorretas",
    ):
        super().__init__(message, status_code=401)  

class UserDatasNotSend(LoginException):
       def __init__(
            self, 
            message: str = "Dados do usuário não foram enviados",
    ):
        super().__init__(message, status_code=406)  