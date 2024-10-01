class LoginException(Exception):
    def __init__(
            self, 
            message: str ="Ocorreu um erro interno!", 
            status_code: int = 500
            ) -> None: 
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class TeamNotFound(LoginException):
    def __init__(
            self, 
            message: str = "Equipe não registrada",
    ):
        super().__init__(message, status_code=404)

class TeamDatasNotSend(LoginException):
       def __init__(
            self, 
            message: str = "Dados da equipe não foram enviados",
    ):
        super().__init__(message, status_code=406)  

class BossTeamDoesExist(LoginException):
       def __init__(
            self, 
            message: str = "Id do boss da equipe não foi encontrado!",
    ):
        super().__init__(message, status_code=406)

class TeamAlreadyExist(LoginException):
       def __init__(
            self, 
            message: str = "Nome informado para sua equipe já está em uso!",
    ):
        super().__init__(message, status_code=409)    

class BossAlreadyGotTeam(LoginException):
       def __init__(
            self, 
            message: str = "Chefe de equipe já possui uma equipe",
    ):
        super().__init__(message, status_code=409)

class BossAlreadyInsertTeam(LoginException):
       def __init__(
            self, 
            message: str = "Usuário já está dentro de uma equipe, impossibilidade de criar uma equipe própria!",
    ):
        super().__init__(message, status_code=409)      