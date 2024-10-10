from flask import Blueprint, request
from Services import ProjectService

from auth.middleware import token_required

type_project_route = Blueprint('typeproject', __name__)

@type_project_route.route('/', methods=['POST'])
@token_required
def create(userId):
    response = ProjectService.create_project_type(request=request, user=userId)
    return response
