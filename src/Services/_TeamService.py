from flask import jsonify

from Repository import (
    TeamRepository,
    UserRepository
)
from Models import Team

class TeamService:

    def get(request):
        return jsonify({'retornei': 'sim'})

    def create(request, user):
        data = request.get_json()

        boss = str(user)

        team = Team(
            teamName= data.get('name'),
            boss=boss,
            members=[],
            projects=[],
        )
        return jsonify({'retornei': 'sim'}), 200

    def update(request): 
        pass