from datetime import datetime

class Invoices:
    """Tabela de faturas emitidas para os usuários"""
    def __init__(
            self,
            userId: str,
            transaction_id: int,
            amount: float,
            status: str,
            due_date: str,
            created_at: str = datetime.now(),
    ) -> None:
        
        self.userId = userId
        self.transaction_id = transaction_id
        self.amount = amount
        self.status = status
        self.due_date = due_date
        self.created_at = created_at

    def to_dict(self) -> dict:
        return{
            "userId": self.userId,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "status": self.status,
            "due_date": self.due_date,
            "created_at": self.created_at,
        }