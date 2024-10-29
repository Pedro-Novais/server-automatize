from bson import ObjectId
from datetime import datetime

class Project:
    """Tabela dos projetos, automações, chatbots que os usuários ou times possuem"""
    def __init__(
            self,
            code: int,
            projectName: str,
            owner: ObjectId,
            typeOwner: str,
            typeProject: str,
            recipients: list = [],
            structure: int = 1,
            status: bool = True,
            created_at: str = datetime.now(),
            last_update: str = datetime.now()
            ) -> None:
        self.code = code
        self.name = projectName
        self.owner = owner
        self.typeOwner = typeOwner
        self.typeProject = typeProject
        self.recipients = recipients
        self.structure = structure
        self.status = status
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        return{
            "code": self.code,
            "projectName": self.name,
            "owner": self.owner,
            "typeOwner": self.typeOwner,
            "typeProject": self.typeProject,
            "recipients": self.recipients,
            "structure": self.structure,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }