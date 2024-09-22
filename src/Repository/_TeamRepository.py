class TeamRepository:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['teams']
    
    def get_team(self, team_name: str) -> bool:
        team = self.collection.find_one({"team": team_name})
        return team is not None
    
    def insert_team(self):
        pass

    def update_team():
        pass

    def delete_team():
        pass