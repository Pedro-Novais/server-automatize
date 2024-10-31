from flask import Blueprint, request
from Services import LoginService

from auth.middleware import token_required

login_route = Blueprint('login', __name__)

@login_route.route('/', methods=['POST'])
def make_login():
    response = LoginService.login(request=request)
    return response

@login_route.route('/out', methods=['GET'])
@token_required
def make_login(user):
    response = LoginService.sign_out(user=user)
    return response
