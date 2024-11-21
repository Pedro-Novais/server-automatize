import requests
import time

from flask import jsonify, g, Request
from bson import ObjectId
from bson.errors import InvalidId

from Models import User, Cards

from config import ENDPOINTS, HEADER_PREVIEW

from auth import (
    hash_password,
    check_password
)

from .utils.validators import (
    validation_user_data,
    validation_password
)

from Repository import (
    UserRepository, 
    UserAndTeamWithProject, 
    CardsClientsRepository, 
    UserAndPaymentsRepository
)

from CustomExceptions import (
    UserAlreadyRegister,
    UserInvalidDataUpdate,
    UserCredentialsInvalids,
    UserDeleteWhitoutSucess,
    UserNotFound,
    UserValuesNotFound,
    ErrorCreatingClientFromUser,
    UserNotCanBeDeleted,
    ErrorToSaveData,
    CardsNotFound
)


class UserService:
    def get_user(user: ObjectId) -> dict:
        try:
            user_repo = UserRepository(g.db)

            filter = {
                "_id": user
            }

            projection = {
                "password": 0,
                "created_at": 0,
                "last_update": 0,
                "_id": 0,
                "team": 0,
                "projects": 0
            }

            user_exist = user_repo.get(
                query_filter=filter,
                projection=projection
            )

            if not user_exist:
                raise UserNotFound()
            
            return jsonify({'response': user_exist}), 200
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def create_user(request: Request) -> dict:
        try:
            data = request.get_json()

            validation_user_data(data)
            validation_password(data.get('password'))

            user_repo = UserRepository(g.db)

            query_email_exist = {
                "email": data.get('email')
            }

            email_exist = user_repo.get(query_filter=query_email_exist)

            if email_exist is not None:
                raise UserAlreadyRegister("Usuário já está registrado!")

            password_hash = hash_password(data.get("password"))
            
            customer_client = {
                "email": data.get('email'),
                "first_name": data.get("name"),
            }

            create_client = requests.post(
                url=ENDPOINTS.CREATE_CLIENT,
                headers=HEADER_PREVIEW,
                json=customer_client
            )
            
            response_data = create_client.json()

            if not create_client.status_code == 201:
                raise ErrorCreatingClientFromUser()

            user = User(
                client_id=response_data["id"],
                name= data.get("name"),
                email= data.get("email"), 
                password= password_hash
            )
            
            MAX_ATTEMPTS = 3  
            cont = 0  

            while cont < MAX_ATTEMPTS:
                try:
                 
                    insert_user = user_repo.post(data=user.to_dict())

                    if insert_user.inserted_id:
                        print("Usuário inserido com sucesso!")
                        break 

                except Exception as e:
                    print(f"Ocorreu um erro durante a inserção: {e}")

                cont += 1

                if cont < MAX_ATTEMPTS:
                    print(f"Tentativa {cont} falhou, tentando novamente...")
                    time.sleep(2)  
                else:
                  
                    raise UserNotFound("Ocorreu algum erro ao realizar o registro do usuário após várias tentativas!")

            return jsonify({"msg": "Usuário criado com sucesso!"}), 201
        
        except (
            UserAlreadyRegister,
            ErrorCreatingClientFromUser
            ) as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
    
    def update_geral(user: ObjectId, request: Request) -> dict:
        try:
            data = request.get_json()

            user_repo = UserRepository(g.db)

            filter = {
                "_id": user
            }
            update = {"$set": data}

            user_update = user_repo.update(
                query_filter=filter, 
                update=update
                )
            
            if not user_update.modified_count:
                return jsonify({"msg": "Usuário não foi atualizado!"}), 200
            
            return jsonify({"msg": "Usuário atualizado com sucesso"}), 200
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def get_token_card(user: ObjectId) -> dict:
        try:
            card_repo = CardsClientsRepository(db=g.db)

            query_card = {
                "owner": user
            }

            projection = {
                "owner": 0,
                "token": 0,
                "customer_id": 0
            }

            cards_get = list(card_repo.get_many(
                query_filter=query_card,
                projection=projection
            ))
            
            if len(cards_get) == 0:
                raise CardsNotFound("Nenhum cartão foi encontrado")
            
            for card in cards_get:
                card["_id"] = str(card["_id"])

            return jsonify({"msg": "Operação realizada com sucesso!", "cards": cards_get}), 200
        
        except (
            CardsNotFound,
            ) as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500
         
    def create_token_card(user: ObjectId, request: Request) -> dict:
        try:
            user_repo = UserRepository(db=g.db)
            user_card_repo = UserAndPaymentsRepository(db=g.db, client=g.client)

            data = request.get_json()

            if not data["tokenCard"]:
                raise UserValuesNotFound("Dados não foram enviados corretamente para o servidor!")

            query_user = {
                "_id": user
            }

            projection = {
                "clientId": 1,
                "token_card": 1
            }

            user_exist = user_repo.get(
                query_filter=query_user,
                projection=projection
                )
            
            if not user_exist:
                raise UserNotFound()
            
            default = False
            if not user_exist.get("token_card") or len(user_exist.get("token_card")) == 0:
                default = True

            id_gateway = user_exist.get("clientId")
            if not id_gateway:
                raise UserValuesNotFound("Dados do usuário não foi enviados ao parceiro de gateway")
            
            json_send = {
                "token": data["tokenCard"]
            }

            add_card_at_gateway = requests.post(
                url=ENDPOINTS.CARD.format(customer_id=id_gateway),
                headers=HEADER_PREVIEW,
                json=json_send
            )

            if not add_card_at_gateway.status_code == 201 and not add_card_at_gateway.status_code == 200:
                print("Erro ao salvar cartão do cliente no gateway de pagamentos")
                raise ErrorToSaveData("Algum erro ocorreu ao salvar o token do cartão no gatewy de pagamentos")
            
            response_data = add_card_at_gateway.json()

            card = Cards(
                userId=user,
                customer_id=response_data.get("customer_id"),
                token=response_data.get("id"),
                last_four_digits=response_data.get("last_four_digits"),
                expiration_month=response_data.get("expiration_month"),
                expiration_year=response_data.get("expiration_year"),
                payment_method_id=response_data.get("payment_method", {}).get("id"),
                thumbnail=response_data.get("payment_method", {}).get("thumbnail"),
                cardholder_name=response_data.get("cardholder", {}).get("name"),
                cardholder_document_type=response_data.get("cardholder", {}).get("identification", {}).get("type"),
                cardholder_document_number=response_data.get("cardholder", {}).get("identification", {}).get("number"),
                default=default
            )

            update_user = {
                "$push":{
                    "token_card": None
                }
            }

            result_operations = user_card_repo.update_user_and_create_card(
                query_user=query_user,
                update_user=update_user,
                create_card=card.to_dict()
            )

            if not result_operations["user_update"] or not result_operations["card_inserted_id"]:
                raise ErrorToSaveData("Erro ao atualizar usuário com novo cartão/salvar informações do cartão no banco de dados!")

            return jsonify({"msg": "Cartão adicionado com sucesso"}), 200
        
        except (
            UserValuesNotFound,
            UserNotFound,
            ErrorToSaveData
            ) as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def update_token_card(user: ObjectId, cardId: str) -> dict:
        pass
    
    def delete_token_card(user: ObjectId, cardId: str) -> dict:
        try:
            card_repo = CardsClientsRepository(db=g.db)
            user_card_repo = UserAndPaymentsRepository(
                db=g.db,
                client=g.client
            )

            filter_card = {
                "owner": user,
                "_id": ObjectId(cardId)
            }

            projection_card = {
                "customer_id": 1,
                "token": 1
            }

            card_exist = card_repo.get(
                query_filter=filter_card,
                projection=projection_card
            )

            if not card_exist:
                raise CardsNotFound("Cartão não foi encontrado em nossa base de dados para realizar a exclusão!")
            
            client_id = card_exist.get("customer_id")[0]
            token_card = card_exist.get("token")

            response_delete = requests.delete(
                url=ENDPOINTS.CARD_ACTION.format(
                    customer_id = client_id,
                    id = token_card
                ),
                headers=HEADER_PREVIEW
            )

            if not response_delete.status_code == 200 and not response_delete.status_code == 201:
                print("Erro ao deletar cartão do cliente no gateway de pagamentos")
                raise ErrorToSaveData("Algum erro ocorreu ao deletar o token do cartão no gatewy de pagamentos")

            filter_user_update = {
                "_id": user
            }

            update_user = {
                "$pull":{
                    "token_card": ObjectId(cardId)
                }
            }

            result_operations = user_card_repo.update_user_and_delete_card(
                query_user=filter_user_update,
                update_user=update_user,
                delete_card=filter_card
            )

            if not result_operations["user_update"] or not result_operations["card_delete"]:
                raise ErrorToSaveData("Erro ao atualizar usuário excluindo cartão/deletar cartão do banco de dados!")
            
            return jsonify({"msg": "Operação realizada com sucesso!"}), 200
        
        except (
            CardsNotFound,
            ) as e:
            return jsonify({'error': e.message}), e.status_code
        
        except InvalidId as e:
            print(f"Erro: {str(e)}")
            return jsonify({'error': "Ocorreu algum erro inesperado ao validar o id do cartão! error: {err}".format(err=str(e))}), 500
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def update_password(user: ObjectId, request: Request) -> dict:
        try:
            data = request.get_json()

            password_old = data.get('password')
            password_new = data.get('newPassword')

            if not password_old or not password_new:
                raise UserInvalidDataUpdate()
            
            validation_password(new=password_new)
            
            user_repo = UserRepository(g.db)
            
            filter = {
                "_id": user
            }

            find_user = user_repo.get(
                query_filter=filter
            )

            authentic = check_password(
                password_save=find_user.get('password'),
                password_sended=password_old
                )
            
            if not authentic:
                raise UserCredentialsInvalids("Senha atual informada, está incorreta!")

            password_hash_new = hash_password(password=password_new)

            update_value = {
                "$set": {
                    "password": password_hash_new
                }
            }

            user_update = user_repo.update(
                query_filter=filter,
                update=update_value
                )

            if not user_update:
                raise UserInvalidDataUpdate("Ocorreu algum erro ao atualizar a senha do usuário!")
            
            return jsonify({"msg": "Senha atualizada com sucesso"}), 200
        
        except (
            UserCredentialsInvalids,
            UserInvalidDataUpdate
            ) as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def delete_user(user: ObjectId) -> dict:
        try:

            user_repo = UserRepository(g.db)

            filter = {
                '_id': user
            }

            user_exist = user_repo.get(query_filter=filter)

            if not user_exist:
                raise UserNotFound()
            
            if user_exist.get("boss"):
                raise UserNotCanBeDeleted("Necessário excluir sua equipe para prosseguir com a deleção da conta!")

            if user_exist.get("team"):
                raise UserNotCanBeDeleted("Necessário estar sem vincúlo de equipe, para prosseguir com a deleção!")
            
            projects = user_exist.get("projects")

            if len(projects) == 0:
                user_repo.delete(query_filter=filter )
            else:
                user_project_repo = UserAndTeamWithProject(db=g.db, client=g.client)

                filter_project = {
                    "owner": user
                }

                user_project_repo.delete_user_and_projects(
                    delete_user=filter,
                    delete_project=filter_project
                )

            response_delete_client = requests.delete(
                headers=HEADER_PREVIEW,
                url=ENDPOINTS.DELETE_CLIENT.format(id=user_exist.get("clientId"))
            )

            if not response_delete_client.status_code == 200:
                print("Erro ao excluir cliente do gateway de pagamentos!")

            return jsonify({"msg": "Usuário excluido com sucesso!"}), 200

        except UserDeleteWhitoutSucess as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao deletar o usuário, erro: {}".format(str(e))}), 500