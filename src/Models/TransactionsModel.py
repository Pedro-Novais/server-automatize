from datetime import datetime

class Transactions:
    """Tabela de transações financeiras realizadas na aplicação"""
    def __init__(
            self,
            userId: str,
            amount: float,
            currency: str,
            payment_method: str,
            status: str,
            transaction_date: str,
            payment_provider: str,
            payment_id: int,
            created_at: str = datetime.now()
    ) -> None:
        
        self.user = userId
        self.amount = amount
        self.currency = currency
        self.method = payment_method
        self.status = status
        self.transaction_date = transaction_date
        self.payment_provider = payment_provider
        self.paymenr_id = payment_id
        self.created_at = created_at

    def to_dict(self) -> dict:
        return{
            "userId":  self.user,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.method,
            "status": self.status,
            "transaction_date": self.transaction_date,
            "payment_provider": self.payment_provider,
            "payment_id": self.paymenr_id,
            "created_at": self.created_at,
        }