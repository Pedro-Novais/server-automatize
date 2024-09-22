from datetime import datetime

class PaymentMethods:
    """Tabela de métodos de pagamentos utilizados pelo usuário"""
    def __init__(
            self,
            userId: str,
            method_type: str,
            provider: str,
            last_four_digits: int,
            created_at: str = datetime.now()
    ) -> None:
        
        self.userId = userId
        self.method = method_type
        self.provider = provider
        self.last_digits = last_four_digits
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "userId": self.userId,
            "method_type": self.method,
            "provider": self.provider,
            "last_four_digits": self.last_digits,
            "created_at": self.created_at,
        }