from datetime import datetime

class Team:
    """Tabela das equipes que estão criadas no sistema"""
    def __init__(
            self,
            teamName: str,
            boss: str,
            members: list = [],
            projects: list = [],
            status: bool = True,
            created_at: str = datetime.now(),
            last_update: str = datetime.now(),
    ) -> None:
        self.name = teamName
        self.boss = boss
        self.members = members
        self.projects = projects
        self.created_at = created_at
        self.last_update = last_update
        self.status = status

    def to_dict(self) -> dict:
        """Converte o modelo para um dicionário, adequado para inserção no MongoDB"""
        return {
            "teamName": self.name,
            "boss": self.boss,
            "members": self.members,
            "projects": self.projects,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }