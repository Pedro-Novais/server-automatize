from flask import Blueprint, request
from Services._TeamService import TeamService

from auth.middleware import token_required

team_route = Blueprint('team', __name__)

@token_required
@team_route.route('/', methods=['GET'])
def get():
    response = TeamService.get()
    return response

@token_required
@team_route.route('/create', methods=['POST'])
def post(id):
    response = TeamService.create(request=request, user=id)
    return response