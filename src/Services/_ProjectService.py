import re

from Repository import (
    ProjectRepository,
    ProjectTypeRepository,
    UserRepository,
    UserAndTeamWithProject,
)

from CustomExceptions import (
    DatasNotSend,
    ProjectAlreadyExist,
    ProjectTypeNotFound,
    UserWithoutPermission,
    OperationAggregationFailed,
    DatasInvalidsToChange,
    UserNotFound,
    ProjectNotFound,
    ConflictAboutTheOwner,
    EmailsInvalidToAdd
)

from Models import (
    ProjectType,
    Project
)

from pymongo.errors import PyMongoError
from flask import Request, jsonify, g
from bson import ObjectId

from .utils.pipelines import create_pipeline
from .utils.validators import validate_email

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

    def get_project(user: ObjectId) -> dict:
        try:
            project_repo = ProjectRepository(db=g.db) 
            project_shared_repo = UserAndTeamWithProject(
                db=g.db,
                client=g.client
            )

            pipeline_unformated = {
                "id": user,
                "from": "teams",
                "local": "team",
                "foreign": "_id",
                "as": "projects_team",
                "project": {
                    "projects": 1,
                    "projects_team.projects": 1
                }
            }

            pipeline = create_pipeline(pipeline_unformated)

            projects = project_shared_repo.get_projects(pipeline=pipeline)[0]

            project_user = projects.get('projects')
            project_team = projects.get('projects_team')[0]['projects']
            
            project_final = []

            for project in project_user:
                project_final.append(project)
            
            for project in project_team:
                project_final.append(project)

            query = {
                "_id": {"$in": project_final},
                "status": True
            }

            projection = {
                "_id": 0,
                "owner": 0
            }

            project_search = list(project_repo.get_many(query_filter=query, projection=projection))

            return jsonify({'msg': 'Operação concluida com sucesso!', 'projects': project_search}), 200

        except OperationAggregationFailed as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
        
    def create_project(request: Request, user: ObjectId) -> dict:
        try:
            project_repo = ProjectRepository(db=g.db) 
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

            code = 1

            if type_owner == 'individual':
                
                user_project_repo = UserAndTeamWithProject(
                    db=g.db,
                    client=g.client
                )
                 
                query_filter = {
                    "owner": user
                }

                last_code = project_repo.get_sort(
                        key="code",
                        type_search=-1,
                        filter=query_filter
                    )
                
                if last_code and "code" in last_code:
                    code = last_code["code"] + 1

                project = Project(
                    code=code,
                    projectName=name_project,
                    owner=user,
                    typeOwner=type_owner,
                    typeProject=code_project_type
                    )
                
                query_user = {
                    "$push": {
                        "projects": None
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
                    raise UserNotFound()

                if not boss.get('team') or not boss.get('boss'):
                    raise UserWithoutPermission()

                query_filter = {
                    "owner": boss.get("team")
                }

                last_code = project_repo.get_sort(
                        key="code",
                        type_search=-1,
                        filter=query_filter
                    )
                
                if last_code and "code" in last_code:
                    code = last_code["code"] + 1
                
                project = Project(
                    code=code,
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
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except ProjectTypeNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar projeto, {}".format(str(e))}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500
    
    def update_project(self, request: Request, user: ObjectId, projectId: str) -> dict:
        try:
            data = request.get_json()

            name_project_type = data.get("nameProjectType")
            type_project_type = data.get("typeProjectType")

            if not name_project_type or not type_project_type:
                 raise DatasInvalidsToChange()

            project_repo = ProjectRepository(g.db)
            project_type_repo = ProjectTypeRepository(g.db)
            
            query = {
                "name": name_project_type,
                "type": type_project_type
            }

            projection = {
                "structure": 1,
                "_id": 1
            }

            project_type = project_type_repo.get(
                query_filter=query,
                projection=projection
                )
            
            if not project_type:
                raise DatasInvalidsToChange("Tipo de projeto a ser atualizado não foi encontrado!")

            possibles_changes = ["projectName", "structure", "nameProjectType", "typeProjectType"]
            changes = {}

            for change in data:
                if not change in possibles_changes:
                    raise DatasInvalidsToChange()

                if change == possibles_changes[0]:
                    self.update_project_name(name=data.get("projectName"))
                    changes["projectName"] = data.get("projectName")

                if change == possibles_changes[1]:
                    
                    self.update_project_structure(
                        structure=data.get("structure"),
                        possibles_structures=project_type["structure"]
                        )
                    changes["structure"] = data.get("structure")

            filter_update = {
                "owner": user,
                "code": int(projectId)
            }

            query_update = {
                "$set": changes
            }

            result_update = project_repo.update(
                query_filter=filter_update, 
                update=query_update
            )

            if not result_update.modified_count:
                raise DatasInvalidsToChange("Projeto a ser atualizado não existe!")

            return jsonify({'msg': 'Projeto atualizado com sucesso!'}), 200

        except DatasInvalidsToChange as e:
            return jsonify({"error": e.message}), e.status_code
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar tipo projeto"}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    @staticmethod
    def update_project_name(name: str) -> None:
        if not name:
            raise DatasNotSend("Nome do projeto não foi enviado ao servidor!")
        
    @staticmethod
    def update_project_structure(structure: int, possibles_structures: list = []) -> None:
        if not structure:
            raise DatasNotSend("Tipo de estrutura não foi enviado ao servidor!")
        
        if not structure in possibles_structures:
            raise DatasNotSend("Estrutura a ser atualizada não existe!")

    def delete_project(user: ObjectId, projectId: str, typeOwner: str) -> dict:
        try:
            project_repo = ProjectRepository(g.db)
            project_shared_repo = UserAndTeamWithProject(
                db=g.db,
                client=g.client
            )
            owner_final = user

            if not typeOwner == "individual" and not typeOwner == "company":
                raise DatasNotSend("Parametros não foram enviados ao servidor!")
            
            if typeOwner == "company":
                user_repo = UserRepository(g.db)

                filter_user = {
                    "_id": user
                }

                projection = {
                    "boss": 1,
                    "team": 1
                }

                user_exist = user_repo.get_user(
                    query_filter=filter_user,
                    projection=projection
                    )
                
                if not user_exist:
                    raise UserNotFound("usuário não está autenticado")

                if not user_exist.get("boss") or not user_exist.get("team"):
                    raise UserWithoutPermission("Usuário não possui permição de excluir esse projeto!")

                owner_final = user_exist.get("team")

            query_filter = {
                "code": int(projectId),
                "owner": owner_final,
            }

            projection = {
                "_id": 1,
                "typeOwner": 1,
                "owner": 1,
            }

            project_exist = project_repo.get(
                query_filter=query_filter,
                projection=projection
                )

            if not project_exist:
                raise ProjectNotFound("Projeto não foi encontrado para ser excluído!")
            
            if not project_exist.get("typeOwner") == typeOwner or not project_exist.get("owner") == owner_final:
                raise ConflictAboutTheOwner("Informações enviadas ao servidor não coincidem com informações da base de dados!")

            project_id_to_delete = project_exist.get("_id")

            filter_project_delete = {
                "_id": project_id_to_delete
            }

            filter_project_delete = {
                "_id": project_id_to_delete
            }

            filter_owner_update = {
                    "_id": owner_final
            }

            query_owner_update = {
                "$pull": {
                    "projects": project_id_to_delete
                }
            }

            if typeOwner == "individual":
                project_shared_repo.delete_owner_individual(
                    query_user=query_owner_update,
                    filter_user=filter_owner_update,
                    delete_project=filter_project_delete
                ) 

            elif typeOwner == "company":
                project_shared_repo.delete_owner_company(
                    query_user=query_owner_update,
                    filter_user=filter_owner_update,
                    delete_project=filter_project_delete
                ) 

            return jsonify({'msg': 'Projeto deletado com sucesso!'}), 200
        
        except ConflictAboutTheOwner as e:
            return jsonify({"error": e.message}), e.status_code
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserWithoutPermission as e:
            return jsonify({"error": e.message}), e.status_code
        
        except ProjectNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar projeto, {}".format(str(e))}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def get_recipients(user: ObjectId, projectId: str, typeOwner: str) -> dict:
        try:

            if not typeOwner == "individual" and not typeOwner == "company" :
                raise DatasNotSend("Dados sobre dono do projeto não foi enviado corretamente!")

            project_repo = ProjectRepository(g.db)

            filter_project = {
                "owner": user,
                "code": int(projectId)
            }

            projection_project = {
                "recipients": 1
            }

            if typeOwner == "company":
                user_repo = UserRepository(g.db)

                filter_user = {
                    "_id": user
                }

                projection = {
                    "boss": 1,
                    "team": 1
                }

                user_exist = user_repo.get_user(
                    query_filter=filter_user,
                    projection=projection
                )

                if not user_exist:
                    raise UserNotFound()
                
                if not user_exist.get("boss") or not user_exist.get("team"):
                    raise UserWithoutPermission("Usuário não possui permissão de visualizar destinátarios!")
                
                filter_project["owner"] = user_exist.get("team")
            
            project_exist = project_repo.get(
                query_filter=filter_project,
                projection=projection_project
            )

            if not project_exist:
                raise ProjectNotFound()
            
            return jsonify({"msg": "Destinatários listados com sucesso", "recipients": project_exist["recipients"]}), 200
        
        except ProjectNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserWithoutPermission as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def add_recipient(request: Request, user: ObjectId, projectId: str, typeOwner: str) -> dict:
        try:
            data = request.get_json()
            emails = data.get("emails")

            if not isinstance(emails, list):
                raise DatasNotSend("Paramêtros não enviados ao servidor!")

            if not typeOwner == "individual" and not typeOwner == "company":
                raise DatasNotSend("Paramêtros não enviados ao servidor!")

            project_repo = ProjectRepository(g.db)

            filter_project = {
                "owner": user,
                "code": int(projectId)
            }

            if typeOwner == "company":
                user_repo = UserRepository(g.db)

                filter_user = {
                    "_id": user
                }

                projection = {
                    "boss": 1,
                    "team": 1
                }

                user_exist = user_repo.get_user(
                    query_filter=filter_user,
                    projection=projection
                )

                if not user_exist:
                    raise UserNotFound()
                
                if not user_exist.get("boss") or not user_exist.get("team"):
                    raise UserWithoutPermission("Usuário não possui permissão de visualizar destinátarios!")
                
                filter_project["owner"] = user_exist.get("team")
            
            validator_emails = validate_email(emails=emails)

            if validator_emails:
                raise EmailsInvalidToAdd()

            filter_update = {
                "$addToSet":{
                    "recipients": {
                        "$each": emails
                    }
                }
            }

            project_exist = project_repo.update(
                query_filter=filter_project,
                update=filter_update
            )

            if not project_exist:
                raise ProjectNotFound()

            if project_exist.modified_count:
                return jsonify({"msg": "Destinatários atualizados com sucesso"}), 200
            else:
                return jsonify({"msg": "Destinatário já está adicionado"}), 200
        
        except ProjectNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserWithoutPermission as e:
            return jsonify({"error": e.message}), e.status_code
        
        except UserNotFound as e:
            return jsonify({"error": e.message}), e.status_code
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except EmailsInvalidToAdd as e:
            return jsonify({"error": e.message}), e.status_code
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def remove_recipient():
        pass

    def out_sign_recipient():
        pass