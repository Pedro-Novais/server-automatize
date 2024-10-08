class TeamRepository:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['teams']
    
    def get_team(self, query_filter: dict) -> bool:
        team = self.collection.find_one(query_filter)
        return team
    
    def insert_team(self, team):
        insert = self.collection.insert_one(team)
        return insert

    def update_team(self, query_filter, team):
        update = self.collection.update_one(query_filter, team)
        return update

    def delete_team(self, query_filter):
        delete = self.collection.delete_one(query_filter)
        return delete