from flask import jsonify
from pymongo.errors import PyMongoError

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