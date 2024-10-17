from flask import Blueprint, request
from Services import ProjectService
from auth.middleware import token_required

project_route = Blueprint('project', __name__)

@project_route.route('/', methods=['GET'])
@token_required
def get(user):
    response = ProjectService.get_project(user=user)
    return response

@project_route.route('/', methods=['POST'])
@token_required
def create(user):
    response = ProjectService.create_project(request=request, user=user)
    return response