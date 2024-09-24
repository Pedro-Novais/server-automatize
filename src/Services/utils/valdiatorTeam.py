from CustomExceptions import (
    TeamDatasNotSend
)

def valdiator_create_team(data):
    if not data.get('name'):
        raise TeamDatasNotSend('Dados necessários para criação do time não foi enviado ao servidor!')