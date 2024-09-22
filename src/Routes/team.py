from flask import Blueprint, request
from Services._TeamService import get_team

team_route = Blueprint('team', __name__)

@team_route.route('/', methods=['GET'])
def get():
    response = get_team()
    return response

@team_route.route('/create', methods=['POST'])
def post():
    response = post_team(request=request)
    return response