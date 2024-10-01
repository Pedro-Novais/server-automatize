from bson import ObjectId
from datetime import datetime

class Members:
    """Tabela das equipes que estão criadas no sistema"""
    def __init__(
            self,
            id_member: str,
            name: str,
            email: str,
            level: int = 0,
            boss: bool = False,
            status: bool = True,
            added_at: str = datetime.now(),
            last_update: str = datetime.now(),
    ) -> None:
        self.id_member = id_member
        self.name = name
        self.email = email
        self.level = level
        self.boss = boss
        self.added_at = added_at
        self.last_update = last_update
        self.status = status

    def to_dict(self) -> dict:
        """Converte o modelo para um dicionário, adequado para inserção no MongoDB"""
        return {
            "_id": self.id_member,
            "name": self.name,
            "email": self.email,
            "level": self.level,
            "boss": self.boss,
            "status": self.status,
            "added_at": self.added_at,
            "last_update": self.last_update,
        }