import jwt
from flask import request, jsonify
from bson import ObjectId
from functools import wraps

SECRET_KEY = 'gtdd45845fv15bgg84fgerfrds864f5A4AS8GRD4G684465546'

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None

        if not token:

            response = {
                'message': 'Token is missing!' 
            }
            
            return jsonify(response), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            userId = ObjectId(data['user_id'])

        except Exception as err:

            response = {
                'message': 'Token is not valid!',
                'error': str(err) 
            }

            return jsonify(response), 401
        
        return f(userId, *args, **kwargs)
    
    return decorated