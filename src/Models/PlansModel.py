class Plans:
    """Tabela que armazena as informações sobre os planos"""
    def __init__(
            self,
            planId: str,
            namePlan: str,
            status: str,
            start_date: str,
            end_date: str
    ) -> None:
        self.planId = planId,
        self.namePlan = namePlan
        self.status = status,
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self) -> dict:
        return {
            "planId": self.planId,
            "namePlan": self.namePlan,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
