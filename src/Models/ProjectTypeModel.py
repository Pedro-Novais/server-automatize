from datetime import datetime

class Project:
    """Tabela dos projetos, Automações, ChatBots que os usuários ou times possuem"""
    def __init__(
            self,
            name: str,
            description: str,
            type: int,
            structure: dict,
            status: bool = True,
            created_at: str = datetime.now(),
            last_update: str = datetime.now()
            ) -> None:
        self.name = name
        self.description = description
        self.type = type
        self.structure = structure
        self.status = status
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        return{
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "structure": self.structure,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }