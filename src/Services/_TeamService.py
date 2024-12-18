from flask import Request, g, jsonify
from bson import ObjectId
from pymongo.errors import PyMongoError

from CustomExceptions import (
    TeamDatasNotSend,
    TeamNotFound,
    BossTeamDoesExist,
    BossAlreadyGotTeam,
    TeamAlreadyExist,
    BossAlreadyInsertTeam,
    OperationAggregationFailed,
    UserNotFound,
    UserMemberInvalid
)
from Repository import (
    TeamRepository,
    UserRepository,
    UserTeamRepository
)

from Models import (
    Team,
    Members
)

from .utils.valdiatorTeam import (
    valdiator_create_team,
    validator_new_member,
)

from .utils.pipelines import create_pipeline

class TeamService:

    def get(user: ObjectId) -> dict:
        try:
            user_team_repo = UserTeamRepository(
                db=g.db, 
                client=g.client
                )
            
            result = user_team_repo.get_info_from_user_about_team(user_id=user)
            team_info = result[0]["team_info"]

            return jsonify(team_info), 200
        
        except OperationAggregationFailed as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error in aggregation operation: {}".format(str(e))}), 500

    def create(request: Request, user: ObjectId) -> dict:
        try:
            data = request.get_json()

            valdiator_create_team(data=data)

            user_repo = UserRepository(g.db)

            filter_user = {
                '_id': user
            }

            projection = {
                'boss': 1,
                'team': 1,
                'project': 1,
                'userName': 1,
                'email': 1
            }

            boss_exist = user_repo.get(query_filter=filter_user, projection=projection)

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

            # member_boss = Members(
            #     id_member=user,
            #     name=boss_exist.get('userName'),
            #     email=boss_exist.get('email'),
            #     boss=True
            # )

            team = Team(
                teamName= data.get('name'),
                boss= user,
                boss_name=boss_exist.get('userName'),
                projects= boss_exist.get('project'),
                # members= member_boss.to_dict()
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

    def update(request: Request, user: ObjectId): 
        try:
            return jsonify({'msg': 'Não implementado!'}), 405
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
    
    def delete_team(user: ObjectId) -> dict:
        try:
            user_repo = UserRepository(g.db)
            team_repo = TeamRepository(g.db)
            user_team_repo = UserTeamRepository(db=g.db, client=g.client)

            query_user = {
                "_id": user
            }

            boss = user_repo.get(query_filter=query_user)

            if not boss:
                raise UserNotFound()
            
            if not boss.get('boss') or not boss.get('team'):
                raise BossTeamDoesExist("Usuário não possui permissão para excluir uma equipe!")
            
            query_team = {
                "_id": boss.get('team')
            }

            team = team_repo.get_team(query_filter=query_team)

            if not team:
                raise TeamNotFound()

            query_user = {
                "team": boss.get('team')
            }

            filter_user = {
                "$set":{
                    "boss": False,
                    "team": None
                }
            }

            result = user_team_repo.updates_users_and_delete_team(
                query_team=query_team,
                query_user=query_user,
                filter_user=filter_user
            )

            return jsonify({'msg': 'Equipe deletada com sucesso!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
        except TeamNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossTeamDoesExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def config_team(request: Request, user: ObjectId) -> dict:
        try:
            return jsonify({'msg': 'Não implementado!'}), 405
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
            
    def disabled_team(user: ObjectId) -> dict:
        try:
            user_repo = UserRepository(g.db)
            team_repo = TeamRepository(g.db)

            query_user = {
                "_id": user
            }

            boss = user_repo.get(query_filter=query_user)

            if not boss:
                raise UserNotFound()
            
            if not boss.get('boss') or not boss.get('team'):
                raise BossTeamDoesExist("Usuário não possui permissão para excluir uma equipe!")
            
            query_team = {
                "_id": boss.get('team')
            }

            team = team_repo.get_team(query_filter=query_team)

            if not team:
                raise TeamNotFound()

            update_team = {"$set":{"status": False}}

            result = team_repo.update_team(query_filter=query_team, team=update_team)

            return jsonify({'msg': 'Equipe desabilitada com sucesso!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
        except TeamNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossTeamDoesExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def enabled_team(user: ObjectId) -> dict:
        try:
            user_repo = UserRepository(g.db)
            team_repo = TeamRepository(g.db)

            query_user = {
                "_id": user
            }

            boss = user_repo.get(query_filter=query_user)

            if not boss:
                raise UserNotFound()
            
            if not boss.get('boss') or not boss.get('team'):
                raise BossTeamDoesExist("Usuário não possui permissão para excluir uma equipe!")
            
            query_team = {
                "_id": boss.get('team')
            }

            team = team_repo.get_team(query_filter=query_team)

            if not team:
                raise TeamNotFound()

            update_team = {"$set":{"status": True}}

            result = team_repo.update_team(query_filter=query_team, team=update_team)

            return jsonify({'msg': 'Equipe habilitada com sucesso!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
        except TeamNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except BossTeamDoesExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def add_member(request: Request, user: ObjectId) -> dict:
        try:
            data = request.get_json()

            email = data.get('email')

            if not email:
                raise TeamDatasNotSend("Parametros não enviados para o servidor!")
            
            user_repo = UserRepository(db=g.db)

            query_user = {
                "email": email
            }

            filter_many_users = {
                "$or":[
                    {"email": email},
                    {"_id": user}
                ]
            }

            users_querys = list(user_repo.get_many(
                query_filter=filter_many_users
            ))

            new_member, member_adding = validator_new_member(
                data=users_querys,
                email=email,
                )

            if not new_member.get('team') == None or new_member.get('boss'):
                raise TeamDatasNotSend("Usuário já está em uma equipe ou possui uma!")
            
            member = Members(
                id_member=str(new_member.get('_id')),
                name=new_member.get('userName'),
                email=new_member.get('email'),
            )

            user_team_repo = UserTeamRepository(g.db, g.client)
            
            query_team = {
                "_id": member_adding.get('team')
            }

            filter_team = {
                "$push": {"members": member.to_dict()}
            }

            query_user = {
                "_id": new_member.get('_id')
            }

            filter_user = {
                "$set": {"team": member_adding.get('team')}
            }

            user_team_repo.update_user_and_team(
                query_user= query_user,
                filter_user= filter_user,
                query_team= query_team,
                filter_team= filter_team
            )

            return jsonify({'msg': 'Novo membro adicionado a equipe!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
        except TeamDatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def get_members(user: ObjectId) -> dict:
        try:
            user_team_repo = UserTeamRepository(
                db=g.db, 
                client=g.client
                )

            rules = {
                "id": user,
                "from": "teams",
                "local": "team",
                "foreign": "_id",
                "as": "members_from_team",
                "project": {
                    "members_from_team.members._id": 1,
                    "members_from_team.members.name": 1,
                    "members_from_team.members.email": 1,
                    "members_from_team.members.level": 1,
                    "members_from_team.members.status": 1,
                    "members_from_team.members.added_at": 1
                }
            }

            pipeline = create_pipeline(rules=rules)

            result = user_team_repo.get_members_from_team(pipeline=pipeline)
            members = result[0].get('members_from_team')[0]
            
            return jsonify({'msg': 'membros listados com sucesso!', "members": members.get('members')}), 200
        
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
        
    def edit_member(request: Request, user: ObjectId, member: str) -> dict:
        try:
            pass
            return jsonify({'msg': 'Não implementado!'}), 405
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def delete_member(user: ObjectId, member: str) -> dict:
        try:
            user_repo = UserRepository(g.db)
            user_team_repo = UserTeamRepository(db=g.db, client=g.client)

            filter_boss = {
                "_id": user
            }

            boss = user_repo.get(query_filter=filter_boss)

            if not boss:
                raise UserNotFound("Usuário não foi encontrado!")

            if not boss.get('boss') or not boss.get('team'):
                raise BossTeamDoesExist("Usuário não é boss de um equipe")
            
            query_member = {
                "_id": ObjectId(member)
            }

            member_search = user_repo.get(query_filter=query_member)

            if not member_search:
                raise UserNotFound("Membro não está cadastrado no sistema!")

            if not member_search.get('team') or member_search.get('boss'):
                raise UserMemberInvalid("Membro inserido não faz parte da equipe!")
            
            filter_team = {
                "boss": user
            }

            update_team = {
                "$pull": {"members":{"_id": ObjectId(member)}}
            }

            filter_user = {
                "_id": ObjectId(member)
            }

            update_user = {
                "team": None
            }

            user_team_repo.update_user_and_team(
                query_user=update_user,
                filter_user=filter_user,
                query_team=update_team,
                filter_team=filter_team
            )


            return jsonify({'msg': 'Membro deletado com sucesso!'}), 200
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao realizar as atualizações no banco de dados!", "type": "database"}), 500
        
        except TeamDatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserMemberInvalid as e:
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