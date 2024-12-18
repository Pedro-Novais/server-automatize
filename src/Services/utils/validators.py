import re

from config import KEYS

from CustomExceptions import (
    UserValuesNotFound, 
    UserInvalidDataUpdate,
    EmailsInvalidToAdd,
    HeaderInvalid
    )

def validation_user_data(data: dict) -> None:
    name = data.get('name')
    email = data.get('email')

    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if  name is None or not isinstance(name, str) or len(name) < 3:
        raise UserValuesNotFound("Name was not informed!")
    
    if not re.match(regex, email):
        raise UserValuesNotFound("Email não está no padrão exigido")

def validation_password(new: str) -> bool:
    regex = r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).*$'
              
    if not new or len(new) < 7 or not re.match(regex, new):
        raise UserInvalidDataUpdate("Senha não está no padrão exigido!")
    
def validate_email(emails: list) -> dict | None:
    if len(emails) == 0:
        raise EmailsInvalidToAdd("Destinatários não foram enviados ao servidor!")
    
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    for email in emails:
        if not isinstance(email, str):
            raise EmailsInvalidToAdd()
        if not re.match(regex, email):
            result_invalid = {
                "emailNotValid": email
            }
            return result_invalid
        
def validate_headers(key_from_request):
    if key_from_request in KEYS:
        return True
     
    raise HeaderInvalid()