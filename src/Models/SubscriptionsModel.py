from datetime import datetime

class Subscriptions:
    """Tabela de pagamentos recorrentes"""
    def __init__(
            self,
            userId: int,
            plan: str,
            amount: float,
            billing_cycle_date: str,
            status: str,
            created_at: str = datetime.now(),
            last_update: str = datetime.now(),
            ) -> None:
        
        self.userId = userId
        self.plan = plan
        self.amount = amount
        self.billing_cycle_date = billing_cycle_date
        self.status = status
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        return {
            "userId": self.userId,
            "plan": self.plan,
            "amount": self.amount,
            "billing_cycle_date": self.billing_cycle_date,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }