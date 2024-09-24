from flask import Blueprint, request
from Services._TeamService import TeamService

from auth.middleware import token_required

team_route = Blueprint('team', __name__)

@team_route.route('/', methods=['GET'])
@token_required
def get():
    response = TeamService.get()
    return response

@team_route.route('/', methods=['POST'])
@token_required
def create(userId):
    response = TeamService.create(request=request, user=userId)
    return response