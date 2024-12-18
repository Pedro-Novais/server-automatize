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

@project_route.route('/<projectId>', methods=['PATCH'])
@token_required
def update(user, projectId):
    project = ProjectService()
    response = project.update_project(request=request, user=user, projectId=projectId)
    return response

@project_route.route('/<projectId>/<typeOwner>', methods=['DELETE'])
@token_required
def delete(userId, projectId, typeOwner):
    response = ProjectService.delete_project(user=userId, projectId=projectId, typeOwner=typeOwner)
    return response

@project_route.route('/recipients/<projectId>/<typeOwner>', methods=['GET'])
@token_required
def get_recipients(userId, projectId, typeOwner):
    response = ProjectService.get_recipients(user=userId, projectId=projectId, typeOwner=typeOwner)
    return response

@project_route.route('/recipients/<projectId>/<typeOwner>', methods=['POST'])
@token_required
def post_recipients(userId, projectId, typeOwner):
    response = ProjectService.add_recipient(user=userId, request=request, projectId=projectId, typeOwner=typeOwner)
    return response

@project_route.route('/recipients/<projectId>/<typeOwner>', methods=['PATCH'])
@token_required
def remove_recipients(userId, projectId, typeOwner):
    response = ProjectService.remove_recipient(user=userId, request=request, projectId=projectId, typeOwner=typeOwner)
    return response

@project_route.route('/<projectId>/out', methods=['DELETE'])
def out_sign_recipient(projectId):
    response = ProjectService.out_sign_recipient(projectId=projectId)
    return response