from flask import Blueprint, request
from Services._TeamService import TeamService

team_route = Blueprint('team', __name__)

@team_route.route('/', methods=['GET'])
def get():
    response = TeamService.get()
    return response

@team_route.route('/create', methods=['POST'])
def post():
    response = TeamService.create(request=request)
    return response