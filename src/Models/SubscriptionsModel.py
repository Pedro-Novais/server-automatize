from datetime import datetime

class Subscriptions:
    """Tabela de pagamentos recorrentes"""
    def __init__(
            self,
            subscriptionId: str,
            userId: int,
            planId: str,
            payer: str,
            auto_recurring: object,
            status: str,
            created_at: str = datetime.now(),
            last_update: str = datetime.now(),
            ) -> None:
        
        self.subscriptionId = subscriptionId
        self.userId = userId
        self.planId = planId
        self.payer = payer
        self.auto_recurring = auto_recurring
        self.status = status
        self.created_at = created_at
        self.last_update = last_update

    def to_dict(self) -> dict:
        return {
            "subscriptionId": self.subscriptionId,
            "userId": self.userId,
            "planId": self.planId,
            "payer": self.payer,
            "auto_recurring": self.auto_recurring,
            "status": self.status,
            "created_at": self.created_at,
            "last_update": self.last_update,
        }