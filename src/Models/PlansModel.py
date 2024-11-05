class Plans:
    """Tabela que armazena as informações sobre os planos"""
    def __init__(
            self,
            planId: str,
            namePlan: str,
            auto_recurring: object,
            status: str,
            date_created: str,
            details: list = [],
    ) -> None:
        self.planId = planId,
        self.namePlan = namePlan
        self.auto_recurring= auto_recurring
        self.status = status,
        self.date_created = date_created
        self.details = details

    def to_dict(self) -> dict:
        return {
            "planId": self.planId,
            "namePlan": self.namePlan,
            "auto_recurring": self.auto_recurring,
            "status": self.status,
            "date_created": self.date_created,
            "details": self.details
        }
