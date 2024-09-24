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

    def get_info_from_user_about_team(
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
         
        except Exception as e:
            raise