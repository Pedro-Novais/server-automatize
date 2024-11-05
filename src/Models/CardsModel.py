from bson import ObjectId

class Cards:
    def __init__(
            self,
            userId: ObjectId,
            customer_id: str,
            token: str,
            last_four_digits: str,
            expiration_month: int,
            expiration_year: int,
            payment_method_id: str,
            thumbnail: str,
            cardholder_name: str,
            cardholder_document_type: str | None,
            cardholder_document_number: str | None
            ) -> None:
        self.userId = userId
        self.customer_id = customer_id,
        self.token = token
        self.last_four_digits = last_four_digits
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.payment_method_id = payment_method_id
        self.thumbnail = thumbnail
        self.cardholder_name = cardholder_name
        self.cardholder_document_type = cardholder_document_type
        self.cardholder_document_number = cardholder_document_number

    def to_dict(self) -> dict:
        return {
            "owner": self.userId,
            "customer_id": self.customer_id,
            "token":  self.token, 
            "last_four_digits": self.last_four_digits,  
            "expiration_month": self.expiration_month,  
            "expiration_year": self.expiration_year,  
            "payment_method_id": self.payment_method_id,
            "thumbnail": self.thumbnail,  
            "cardholder_name": self.cardholder_name, 
            "cardholder_document_type": self.cardholder_document_type,
            "cardholder_document_number": self.cardholder_document_number 
        }