import requests

from flask import jsonify, g, Request
from bson import ObjectId
from Models import User
from Repository import UserRepository

from auth import (
    hash_password,
    check_password
)

from config import ENDPOINTS, HEADER_PREVIEW

from CustomExceptions import (
    UserAlreadyRegister,
    UserInvalidDataUpdate,
    UserCredentialsInvalids,
    UserDeleteWhitoutSucess,
    UserNotFound,
    ErrorCreatingClientFromUser
    )

from .utils.validators import (
    validation_user_data,
    validation_password
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
            
            insert_user = user_repo.post(data=user.to_dict())

            if not insert_user.inserted_id:
                raise UserNotFound("Ocorreu algum erro ao realizar o registro do usuário!")

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
        """Atualizar esse  método para realizar a remoção do id excluido de algum time, projetos, etc"""
        try:

            user_repo = UserRepository(g.db)

            filter = {
                '_id': user
            }

            result = user_repo.delete(
                query_filter=filter
            )

            if not result.deleted_count:
                raise UserDeleteWhitoutSucess("Ocorreu um erro ao realizar a exclusão do usuário!")

            return jsonify({"msg": "Usuário excluido com sucesso!"}), 200

        except UserDeleteWhitoutSucess as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao deletar o usuário, erro: {}".format(str(e))}), 500