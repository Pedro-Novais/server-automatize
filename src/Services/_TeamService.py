from flask import Request, g, jsonify
from bson import ObjectId
from pymongo.errors import PyMongoError

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
    UserRepository,
    UserTeamRepository
)

from Models import Team

from .utils.valdiatorTeam import valdiator_create_team

class TeamService:

    def get(user: ObjectId) -> dict:
        try:
            pass

            return jsonify({'retornei': 'sim'})
        except Exception as e:
            return jsonify({"error": "Internal server error to connect in database: {}".format(str(e))}), 500

    def create(request: Request, user: ObjectId) -> dict:
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

            team = Team(
                teamName= data.get('name'),
                boss= user,
                projects= boss_exist.get('project'),
            )

            user_team_repo = UserTeamRepository(
                db=g.db,
                client=g.client,
            )

            filter_update_user = {
                "_id": user
            }

            query_update_user = {
                "$set": {"boss": True}
            }

            user_team_repo.update_boss_create_team(
                query_team=team.to_dict(),
                filter_user=filter_update_user,
                query_user=query_update_user
            )

            return jsonify({'msg': 'Equipe criada com sucesso!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
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