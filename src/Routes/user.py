from flask import Blueprint, request
from auth.middleware import token_required

from Services._UserService import UserService

user_route = Blueprint('user', __name__)

@user_route.route('/create', methods=['POST'])
def create():
    response = UserService.create_user(request=request)
    return response

@user_route.route('/', methods=['GET'])
@token_required 
def get(userId):
    response = UserService.get_user(user=userId)
    return response

@user_route.route('/update', methods=['PUT'])
@token_required 
def update(userId):
    response = UserService.update_geral(user=userId, request=request)
    return response

@user_route.route('/updatePassword', methods=['PUT'])
@token_required 
def update_password(userId):
    response = UserService.update_password(user=userId, request=request)
    return response

@user_route.route('/delete', methods=['DELETE'])
@token_required 
def delete(userId):
    response = UserService.delete_user(user=userId)
    return response