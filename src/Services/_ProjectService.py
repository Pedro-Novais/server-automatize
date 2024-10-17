from Repository import (
    ProjectRepository,
    ProjectTypeRepository,
    UserRepository,
    UserAndTeamWithProject
)

from CustomExceptions import (
    DatasNotSend,
    ProjectAlreadyExist,
    ProjectTypeNotFound,
    UserWithoutPermission
)

from Models import (
    ProjectType,
    Project
)

from pymongo.errors import PyMongoError

from flask import Request, jsonify, g
from bson import ObjectId

class ProjectService:
    def create_project_type(request: Request, user: ObjectId) -> dict:
        try:
            project_type_repo = ProjectTypeRepository(g.db)

            data = request.get_json()

            if not data.get('name'):
                raise DatasNotSend()
            
            query_filter = {
                "$or": [
                    {"code": data.get('code')},
                    {"name": data.get('name')}
                ]
            }

            project_type_exist = project_type_repo.get(query_filter=query_filter)

            if project_type_exist:
                raise ProjectAlreadyExist()

            project_type = ProjectType(
                code= data.get('code'),
                name= data.get('name'),
                description= data.get('description'),
                type= data.get('type'),
                structure= data.get('structure'),
                rules= data.get('rules')
            )
            
            project_type_repo.post(project_type.to_dict())

            return jsonify({'msg': 'ProjectType criado com sucesso!'}), 200
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except ProjectAlreadyExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar tipo projeto"}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def create_project(request: Request, user: ObjectId) -> dict:
        try:
            project_type_repo = ProjectTypeRepository(g.db)

            data = request.get_json()

            type_owner = data.get('typeOwner')
            code_project_type = data.get('projetcType')
            name_project = data.get('name')

            if not type_owner or not code_project_type or not name_project:
                raise DatasNotSend("Dados não enviados ao servidor para a criação de um projerto")

            query_project_type = {
                "code": code_project_type
            }

            if not project_type_repo.get(query_project_type):
                raise ProjectTypeNotFound()

            if not type_owner == 'individual' and not type_owner == 'company':
                raise DatasNotSend("Dados não enviados ao servidor para a criação de um projerto")

            if type_owner == 'individual':
                
                user_project_repo = UserAndTeamWithProject(
                    db=g.db,
                    client=g.client
                )

                project = Project(
                    projectName=name_project,
                    owner=user,
                    typeOwner=type_owner,
                    typeProject=code_project_type
                    )
                
                query_user = {
                    "$push": {
                        "project": None
                    }
                }

                filter_user = {
                    "_id": user
                }

                user_project_repo.owner_individual(
                    query_user=query_user,
                    filter_user = filter_user,
                    insert_project=project.to_dict()
                )

            elif type_owner == 'company':
                user_repo = UserRepository(g.db)
                team_project_repo = UserAndTeamWithProject(
                    db=g.db,
                    client=g.client
                )

                query = {
                    "_id": user
                }

                projection = {
                    "boss": 1,
                    "team": 1,

                }

                boss = user_repo.get_user(
                    query_filter=query, 
                    projection=projection
                    )

                if not boss:
                    raise Exception()

                if not boss.get('team') or not boss.get('boss'):
                    raise UserWithoutPermission()

                project = Project(
                    projectName=name_project,
                    owner=boss.get('team'),
                    typeOwner=type_owner,
                    typeProject=code_project_type
                )

                query_team = {
                    "$push": {
                        "projects": None
                    }
                }

                filter_team = {
                    "_id": boss.get('team')
                }

                team_project_repo.owner_company(
                    query_team=query_team,
                    filter_team = filter_team,
                    insert_project=project.to_dict()
                )

            return jsonify({'msg': 'Projeto criado com sucesso!'}), 200
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except ProjectTypeNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar projeto, {}".format(str(e))}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500