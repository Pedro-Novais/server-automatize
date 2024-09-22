import bcrypt
import jwt

SECRET_KEY = 'gtdd45845fv15bgg84fgerfrds864f5A4AS8GRD4G684465546'

def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id
    }, SECRET_KEY, algorithm='HS256')

    return token

def hash_password(
        password: str
        ) -> str:
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(
        password_save: str, 
        password_sended: str
        ) -> bool:
    
    return bcrypt.checkpw(password_sended.encode('utf-8'), password_save.encode('utf-8'))