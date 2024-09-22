from flask import jsonify, g
from Models import User
from Repository import UserRepository

from auth import (
    hash_password,
    check_password
)

from CustomExceptions import (
    UserValuesNotFound,
    UserAlreadyRegister,
    UserInvalidDataUpdate,
    UserCredentialsInvalids,
    UserDeleteWhitoutSucess
    )

from .utils.validators import (
    validation_user_data,
    validation_password
    )

class UserService:
    def get_user(
            user: str
            ) -> dict:
        try:
            user_repo = UserRepository(g.db)

            filter = {
                "_id": user
            }

            projection = {
                "password": 0,
                "created_at": 0,
                "last_update": 0,
                "_id": 0
            }

            datas = user_repo.get_user(
                query_filter=filter,
                projection=projection
            )

            if not datas:
                raise UserValuesNotFound("Erro ao selecionar os dados do usuário!")
            
            return jsonify({'response': datas}), 200
        
        except UserValuesNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def create_user(request) -> dict:
        try:
            data = request.get_json()
            validation_user_data(data)
            validation_password(data.get('password'))

            user_repo = UserRepository(g.db)

            email_exist = user_repo.get_user({"email": data.get('email')})
            if email_exist is not None:
                raise UserAlreadyRegister("Usuário já está registrado!")

            password_hash = hash_password(data.get("password"))

            user = User(
                name= data.get("name"),
                email= data.get("email"), 
                password= password_hash, 
                team= data.get("team")
                )
            
            user_repo.insert_user(user.to_dict())

            return jsonify({"msg": "User created with sucess"}), 201
        
        except UserInvalidDataUpdate as e:
            return jsonify({'error': e.message}), e.status_code
        
        except UserValuesNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserAlreadyRegister as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
    
    def update_geral(user, request) -> dict:
        try:
            data = request.get_json()

            user_repo = UserRepository(g.db)

            filter = {
                "_id": user
            }
            update = {"$set": data}

            user_repo.update_user(
                query_filter=filter, 
                update_values=update
                )
            
            return jsonify({"msg": "Usuário atualizado com sucesso"}), 200
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def update_password(user, request):
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

            find_user = user_repo.get_user(
                query_filter=filter
            )

            authentic = check_password(
                password_save=find_user.get('password'),
                password_sended=password_old
                )
            
            if not authentic:
                raise UserCredentialsInvalids("Senha atual informada, está incorreta!")

            password_hash_new = hash_password(password=password_new)

            update = {
                "$set": {
                    "password": password_hash_new
                }
            }

            user_repo.update_user(
                query_filter=filter,
                update_values=update
                )

            return jsonify({"msg": "Senha atualizada com sucesso"}), 200
        
        except UserCredentialsInvalids as e:
            return jsonify({'error': e.message}), e.status_code
        
        except UserInvalidDataUpdate as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao atualizar dados do usuário: {}".format(str(e))}), 500

    def delete_user(user):
        try:

            user_repo = UserRepository(g.db)

            filter = {
                '_id': user
            }

            result = user_repo.delete_user(
                query_filter=filter
            )

            if not result.deleted_count:
                raise UserDeleteWhitoutSucess("Ocorreu um erro ao realizar a exclusão do usuário!")

            return jsonify({"msg": "Usuário excluido com sucesso!"}), 200

        except UserDeleteWhitoutSucess as e:
            return jsonify({'error': e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Erro ao deletar o usuário, erro: {}".format(str(e))}), 500