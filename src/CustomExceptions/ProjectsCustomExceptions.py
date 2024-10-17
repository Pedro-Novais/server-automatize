class ProjectException(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DatasNotSend(ProjectException):
    def __init__(
            self, 
            message: str = "Dados não enviados ao servidor para a criação de um tipo de projerto",
    ):
        super().__init__(message, status_code=406)

class ProjectAlreadyExist(ProjectException):
    def __init__(
            self, 
            message: str = "Um projeto já foi criado com os seguintes atributos!",
    ):
        super().__init__(message, status_code=409)

class ProjectTypeNotFound(ProjectException):
    def __init__(
            self, 
            message: str = "Tipo de projeto não foi encontrado",
    ):
        super().__init__(message, status_code=404)

class UserWithoutPermission(ProjectException):
    def __init__(
            self, 
            message: str = "Usuário não possui permição de criar projeto do tipo compania",
    ):
        super().__init__(message, status_code=403)
   