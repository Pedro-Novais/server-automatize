from datetime import datetime

class ProjectType:
    """Tabela dos projetos, Automações, ChatBots que os usuários ou times possuem"""
    def __init__(
            self,
            code: int,
            name: str,
            description: str,
            type: str,
            structure: list,
            rules: list,
            status: bool = True,
            created_at: str = datetime.now(),
            last_update: str = datetime.now()
            ) -> None:
        self.code = code
        self.name = name
        self.description = description
        self.type = type
        self.structure = structure
        self.rules = rules
        self.status = status
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        return{
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "structure": self.structure,
            "rules": self.rules,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }