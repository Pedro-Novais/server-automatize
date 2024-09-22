from flask import Blueprint, request
from Services import LoginService
login_route = Blueprint('login', __name__)

@login_route.route('/', methods=['POST'])
def make_login():
    response = LoginService.login(request=request)
    return response
