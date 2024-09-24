from flask import Blueprint, request

from auth.middleware import token_required

project_route = Blueprint('project', __name__)

@project_route.route('/', methods=['GET'])
def get():
    pass

@project_route.route('/', methods=['POST'])
def create():
    pass