class Plans:
    """Tabela que armazena as informações sobre os planos"""
    def __init__(
            self,
            planId: str,
            namePlan: str,
            status: str,
            date_created: str,
    ) -> None:
        self.planId = planId,
        self.namePlan = namePlan
        self.status = status,
        self.date_created = date_created

    def to_dict(self) -> dict:
        return {
            "planId": self.planId,
            "namePlan": self.namePlan,
            "status": self.status,
            "date_created": self.date_created,
        }
