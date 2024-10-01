from flask import jsonify

from pymongo.errors import (
    OperationFailure, ConfigurationError, ConnectionFailure, InvalidOperation,
    DocumentTooLarge, PyMongoError
)

from CustomExceptions.OperationsDatabaseExceptions import OperationAggregationFailed

class UserTeamRepository:
    def __init__(
            self, 
            db,
            client,
            ) -> None:
        self.db = db
        self.client = client

    def update_boss_create_team(
            self,
            query_user: dict,
            filter_user: dict,
            query_team: dict
            ) -> None:
        
        with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    response = self.db.teams.insert_one(
                        query_team,
                        session=session
                    )

                    query_user["$set"]["team"] = response.inserted_id

                    self.db.users.update_one(
                        filter_user,
                        query_user,
                        session=session
                    )
                
            except PyMongoError as e:
                raise
    
    def update_user_and_team(
            self,
            query_user,
            filter_user,
            query_team,
            filter_team
    ):

        with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    self.db.teams.update_one(
                        query_team,
                        filter_team,
                        session=session
                    )

                    self.db.users.update_one(
                        query_user,
                        filter_user,
                        session=session
                    )

            except PyMongoError as e:
                raise
    
    def updates_users_and_delete_team(
            self,
            query_user,
            filter_user,
            query_team,
    ):

        with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    self.db.teams.delete_one(
                        query_team,
                        session=session
                    )

                    self.db.users.update_many(
                        query_user,
                        filter_user,
                        session=session
                    )

            except PyMongoError as e:
                raise

    def  get_info_from_user_about_team(
            self,
            user_id
    ):
        try:
            pipeline = [
                {
                    "$match": {"_id": user_id} 
                },
                {
                    "$lookup": {
                        "from": "teams", 
                        "localField": "team", 
                        "foreignField": "_id",  
                        "as": "team_info"  
                    }
                },
                {
                    "$project": {  
                        "team_info.teamName": 1,
                        "team_info.bossName": 1,  
                        "team_info.members": 1,  
                        "team_info.projects": 1,
                        "team_info.status": 1,
                        "team_info.created_at": 1
                    }
                }
            ]

            result = list(self.db.users.aggregate(pipeline))
            return result
         
        except OperationFailure as e:
            raise OperationAggregationFailed(f"Erro na operação de agregação: {str(e)}")
        
        except ConfigurationError as e:
            raise OperationAggregationFailed(f"Erro de configuração: {str(e)}")
        
        except ConnectionFailure as e:
            raise OperationAggregationFailed(f"Falha na conexão com o MongoDB: {str(e)}")
        
        except InvalidOperation as e:
            raise OperationAggregationFailed(f"Operação inválida: {str(e)}")
        
        except DocumentTooLarge as e:
            raise OperationAggregationFailed(f"O documento é muito grande: {str(e)}")
        
        except PyMongoError as e:
            raise OperationAggregationFailed(f"Erro inesperado com MongoDB: {str(e)}")
        
    def get_members_from_team(
            self,
            pipeline
    ):
        try:
            result = list(self.db.users.aggregate(pipeline))
            return result
        
        except OperationFailure as e:
            raise OperationAggregationFailed(f"Erro na operação de agregação: {str(e)}")
        
        except ConfigurationError as e:
            raise OperationAggregationFailed(f"Erro de configuração: {str(e)}")
        
        except ConnectionFailure as e:
            raise OperationAggregationFailed(f"Falha na conexão com o MongoDB: {str(e)}")
        
        except InvalidOperation as e:
            raise OperationAggregationFailed(f"Operação inválida: {str(e)}")
        
        except DocumentTooLarge as e:
            raise OperationAggregationFailed(f"O documento é muito grande: {str(e)}")
        
        except PyMongoError as e:
            raise OperationAggregationFailed(f"Erro inesperado com MongoDB: {str(e)}")