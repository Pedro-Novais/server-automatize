class ProjectTypeRepository:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['projectType']
    
    def get_project(self, query_filter: dict, projection: dict | None = None) -> bool:
        team = self.collection.find_one(query_filter, projection)
        return team
    
    def insert_project(self, team):
        insert = self.collection.insert_one(team)
        return insert

    def update_project(self, query_filter, team):
        update = self.collection.update_one(query_filter, team)
        return update

    def delete_project(self, query_filter):
        delete = self.collection.delete_one(query_filter)
        return delete