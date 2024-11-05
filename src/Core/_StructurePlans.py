from config import ENDPOINTS

class StructurePlans:
    def __init__(
            self, 
            namePlan: str, 
            pricePlan: float,
            frequency: int = 1,
            frequency_type: str = "months",
            currency_id: str = "BRL",
            billing_day: int = 20,
            frequency_free: int = 1,
            frequency_type_free: str = "months"
            ) -> dict:
        self.name = namePlan
        self.price = pricePlan

    def to_dict(self):
        return {
            "reason": self.name,
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": self.price,
                "currency_id": "BRL",
                "billing_day": 20
            },
             "free_trial": {
                "frequency": 7,
                "frequency_type": "days"
            },
            "back_url": ENDPOINTS.BACK_URL_TEST
        }
