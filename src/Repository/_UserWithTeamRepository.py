from flask import jsonify
from pymongo.errors import PyMongoError

class UserTeamRepository:
    def __init__(
            self, 
            db,
            client,
            user_repo,
            team_repo,
            ):
        self.db = db
        self.client = client
        self.user_repo = user_repo
        self.team_repo = team_repo

    def update_boss_create_team(
            self,
            query_user,
            filter_user,
            query_team
            ):
        
        with self.client.start_session() as session:
            try:
                with session.start_transaction():

                    self.db.teams.insert_one(
                        query_team,
                        session=session
                    )

                    self.db.users.update_one(
                        filter_user,
                        query_user,
                        session=session
                    )

                    return True
                
            except PyMongoError as e:
                raise