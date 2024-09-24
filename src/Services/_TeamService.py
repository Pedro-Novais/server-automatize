from flask import g, jsonify

from CustomExceptions import (
    TeamDatasNotSend,
    TeamNotFound,
    BossTeamDoesExist,
    BossAlreadyGotTeam,
    TeamAlreadyExist,
    BossAlreadyInsertTeam
)
from Repository import (
    TeamRepository,
    UserRepository
)

from Models import Team

from .utils.valdiatorTeam import valdiator_create_team

class TeamService:

    def get(request):
        return jsonify({'retornei': 'sim'})

    def create(request, user):
        try:
            data = request.get_json()

            valdiator_create_team(data=data)

            user_repo = UserRepository(g.db)

            filter_user = {
                '_id': user
            }

            boss_exist = user_repo.get_user(filter_user)

            if not boss_exist:
                raise BossTeamDoesExist("Id do boss da equipe não foi identificado em nosso banco de dados")
            
            if boss_exist.get('boss'):
                raise BossAlreadyGotTeam("Cada usuário só pode possuir uma equipe!")

            if not boss_exist.get('team') == None:
                raise BossAlreadyInsertTeam("Usuário já é membro de uma equipe!")

            team_repo = TeamRepository(g.db)

            team_filter = {
                "teamName": data.get('name')
            }

            team_exist = team_repo.get_team(team_filter)

            if team_exist:
                raise TeamAlreadyExist("Nome informado para sua equipe já está em uso!") 

            boss = str(user)

            team = Team(
                teamName= data.get('name'),
                boss=boss,
                projects= boss_exist.get('project'),
            )

            insert_team = team_repo.insert_team(team.to_dict())

            if insert_team == None:
                pass

            return jsonify({'msg': 'Equipe criada com sucesso', 'team': team.to_dict()}), 200
        
        except TeamDatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossTeamDoesExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except TeamAlreadyExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossAlreadyGotTeam as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossAlreadyInsertTeam as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def update(request): 
        pass