from bson import ObjectId
from datetime import datetime

from CustomExceptions import UserValuesNotFound

class User:
    """Tabela dos usuários da aplicação"""
    def __init__(
            self,
            client_id: str,
            name: str,  
            email: str, 
            password: str,
            token_card: list = [], 
            boss: bool = False,
            project: list = [],
            team: str = None,
            created_at: str = datetime.now(),
            last_update: str = datetime.now(),
            ) -> None:
        if not name or not isinstance(name, str):
            raise UserValuesNotFound("Name must be a non-empty string")
        if not email or not isinstance(email, str):
            raise UserValuesNotFound("Email must be a non-empty string")
        if not password or not isinstance(password, str):
            raise UserValuesNotFound("Password must be a non-empty string")
        
        self.client_id = client_id
        self.token_card = token_card
        self.name = name
        self.email = email
        self.password = password
        self.team = team
        self.boss = boss
        self.project = project
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        """Converte o modelo para um dicionário, adequado para inserção no MongoDB"""
        return {
            "clientId": self.client_id,
            "token_card": self.token_card,
            "userName": self.name,
            "email": self.email,
            "password": self.password,
            "team": self.team,
            "boss": self.boss,
            "projects": self.project,
            "created_at:": self.created_at,
            "last_update": self.last_update,
        }