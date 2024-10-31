from flask import jsonify, g, Request
from bson import ObjectId
from Repository import UserRepository

from auth import (
    generate_token,
    check_password
)

from CustomExceptions.LoginCustomExceptions import (
    UserNotFound,
    UserCredentialsInvalids,
    UserDatasNotSend
)

class LoginService():
    def login(request: Request) -> dict:
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                 raise UserDatasNotSend("Conteúdo de informações não foram enviados ao servidor!")
            
            user_repo = UserRepository(g.db)
            
            filter = {
                "email": email
            }


            find_user = user_repo.get_user(
                query_filter=filter
                )

            if not find_user:
                raise UserNotFound("Usuário não encontrado")
            
            authentic = check_password(
                password_save = find_user.get('password'), 
                password_sended=password
                )
            
            if not authentic:
                raise UserCredentialsInvalids("Credenciais incorretas!")
            
            id = str(find_user.get('_id'))

            token = generate_token(user_id=id)

            return jsonify({"msg": 'Login realizado com sucesso!', "token": token}), 200

        except UserDatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserCredentialsInvalids as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:  
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def sign_out(user: ObjectId) -> dict:
        pass