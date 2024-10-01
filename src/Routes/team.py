from flask import Blueprint, request
from Services._TeamService import TeamService

from auth.middleware import token_required

team_route = Blueprint('team', __name__)

@team_route.route('/', methods=['GET'])
@token_required
def get(userId):
    response = TeamService.get(user=userId)
    return response

@team_route.route('/', methods=['POST'])
@token_required
def create(userId):
    response = TeamService.create(request=request, user=userId)
    return response

@team_route.route('/member', methods=['GET'])
@token_required
def get_member(userId):
    response = TeamService.get_members(user=userId)
    return response

@team_route.route('/member', methods=['POST'])
@token_required
def add_member(userId):
    response = TeamService.add_member(request=request, user=userId)
    return response

@team_route.route('/member/<id>', methods=['DELETE'])
@token_required
def delete_member(userId, id):
    response = TeamService.delete_member(user=userId, member=id)
    return response