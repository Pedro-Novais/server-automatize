from pymongo.errors import (
    OperationFailure, ConfigurationError, ConnectionFailure, InvalidOperation,
    DocumentTooLarge, PyMongoError
)

from CustomExceptions.OperationsDatabaseExceptions import OperationAggregationFailed

class UserAndTeamWithProject:
    def __init__(
            self, 
            db,
            client,
            ) -> None:
        self.db = db
        self.client = client

    def owner_individual(
            self,
            query_user,
            filter_user,
            insert_project
            ):
         with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    response = self.db.project.insert_one(
                        insert_project,
                        session=session
                    )

                    query_user["$push"]["projects"] = response.inserted_id

                    self.db.users.update_one(
                        filter_user,
                        query_user,
                        session=session
                    )

            except PyMongoError as e:
                raise

    def owner_company(
            self,
            query_team,
            filter_team,
            insert_project
            ):
         with self.client.start_session() as session:
            try:
                with session.start_transaction():
                    
                    response = self.db.project.insert_one(
                        insert_project,
                        session=session
                    )

                    query_team["$push"]["projects"] = response.inserted_id

                    self.db.teams.update_one(
                        filter_team,
                        query_team,
                        session=session
                    )

            except PyMongoError as e:
                raise

    def get_projects(self, pipeline: dict) -> list:
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