from bson import ObjectId

from CustomExceptions import (
    TeamDatasNotSend
)

def valdiator_create_team(data):
    if not data.get('name'):
        raise TeamDatasNotSend('Dados necessários para criação do time não foi enviado ao servidor!')
    
def validator_new_member(data, email):
    new_member = {}
    member_adding = {}

    for doc in data:
        if doc['email'] == email:
            new_member = doc
        else:
            member_adding = doc

    if new_member == {}:
        raise TeamDatasNotSend("Usuário a ser adicionado não está cadastrado na plataforma!")
    
    return new_member, member_adding