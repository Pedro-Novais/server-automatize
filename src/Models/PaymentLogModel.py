from datetime import datetime

class PaymentLog:
    """Tabela dos logs de tentativa de pagamento"""
    def __init__(
            self,
            transaction_id: str,
            log_message: str,
            log_date: str = datetime.now()
            ) -> None:
        self.transaction = transaction_id
        self.message = log_message
        self.date = log_date

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction,
            "log_message": self.message,
            "log_date": self.date,
        }