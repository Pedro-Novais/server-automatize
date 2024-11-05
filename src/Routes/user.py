from flask import Blueprint, request
from auth.middleware import token_required

from Services._UserService import UserService

user_route = Blueprint('user', __name__)

@user_route.route('/', methods=['POST'])
def create():
    response = UserService.create_user(request=request)
    return response

@user_route.route('/', methods=['GET'])
@token_required 
def get(userId):
    response = UserService.get_user(user=userId)
    return response

@user_route.route('/', methods=['PATCH'])
@token_required 
def update(userId):
    response = UserService.update_geral(user=userId, request=request)
    return response

@user_route.route('/card', methods=['GET'])
@token_required 
def get_card_token(userId):
    response = UserService.get_token_card(user=userId)
    return response

@user_route.route('/card', methods=['PATCH'])
@token_required 
def update_card_token(userId):
    response = UserService.update_token_card(user=userId, request=request)
    return response

@user_route.route('/card/<cardId>', methods=['DELETE'])
@token_required 
def delete_card_token(userId, cardId):
    response = UserService.delete_token_card(user=userId, cardId=cardId)
    return response

@user_route.route('/updatepassword', methods=['PATCH'])
@token_required 
def update_password(userId):
    response = UserService.update_password(user=userId, request=request)
    return response

@user_route.route('/delete', methods=['DELETE'])
@token_required 
def delete(userId):
    response = UserService.delete_user(user=userId)
    return response