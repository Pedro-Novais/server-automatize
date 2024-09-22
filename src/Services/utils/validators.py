import re

from CustomExceptions import (
    UserValuesNotFound, 
    UserInvalidDataUpdate
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
              
    if not new:
        raise UserInvalidDataUpdate("Senha não está no padrão exigido")
    
    if len(new) < 7:
        raise UserInvalidDataUpdate("Senha não está no padrão exigido")

    if not re.match(regex, new):
        raise UserInvalidDataUpdate("Senha não está no padrão exigido")