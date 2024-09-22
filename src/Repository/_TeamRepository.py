class TeamRepository:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['teams']
    
    def team_exists(self, team_name: str) -> bool:
        team = self.collection.find_one({"team": team_name})

        return team is not None