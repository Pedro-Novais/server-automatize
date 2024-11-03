class UserException(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserValuesNotFound(UserException):
    def __init__(
            self, 
            message: str = "Values is empty!"
            ) -> None:
        super().__init__(message, status_code=404)

class UserAlreadyRegister(UserException):
    def __init__(
            self,
            message: str = "User already exist!"
    ) -> None:
        super().__init__(message, status_code=409)

class UserInvalidDataUpdate(UserException):
    def __init__(
            self,
            message: str = "Parametros não foram passados para o servidor corretamente!"
    ) -> None:
        super().__init__(message, status_code=406)

class UserDeleteWhitoutSucess(UserException):
    def __init__(
            self,
            message: str = "Ocorreu um erro ao realizar a exclusão do usuário!"
    ) -> None:
        super().__init__(message, status_code=404)

class UserNotCanBeDeleted(UserException):
       def __init__(
            self,
            message: str = "Usuário não pode ser excluído pois possui pendências!"
    ) -> None:
        super().__init__(message, status_code=400)

class UserMemberInvalid(UserException):
    def __init__(
            self,
            message: str = "Membro inserido já é chefe ou possui uma equipe"
    ) -> None:
        super().__init__(message, status_code=404)

class ErrorCreatingClientFromUser(UserException):
    def __init__(
            self,
            message: str = "Algum erro ocorreu ao criar o usuário"
    ) -> None:
        super().__init__(message, status_code=400)