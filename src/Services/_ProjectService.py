from Repository import (
    ProjectRepository,
    ProjectTypeRepository
)

from CustomExceptions import (
    DatasNotSend,
    ProjectAlreadyExist
)

from pymongo.errors import PyMongoError

from Models import ProjectType
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

            project_type_exist = project_type_repo.get_project(query_filter=query_filter)

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
            
            project_type_repo.insert_project(project_type.to_dict())

            return jsonify({'msg': 'ProjectType criado com sucesso!'}), 200
        
        except DatasNotSend as e:
            return jsonify({"error": e.message}), e.status_code
        
        except ProjectAlreadyExist as e:
            return jsonify({"error": e.message}), e.status_code
        
        except PyMongoError as e:
            return jsonify({"error": "Erro ao criar projeto"}), 500
        
        except Exception as e:
            return jsonify({"error": "Internal server error: {}".format(str(e))}), 500

    def create_project(request, user):
        data = request.get_json()
        
        pass