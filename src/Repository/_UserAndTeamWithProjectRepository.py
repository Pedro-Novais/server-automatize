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

                    query_user["$push"]["project"] = response.inserted_id

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