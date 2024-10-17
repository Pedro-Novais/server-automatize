class BaseRepository:
    def get(self, query_filter: dict, projection: dict | None = None) -> bool:
        team = self.collection.find_one(query_filter, projection)
        return team
    
    def post(self, team):
        insert = self.collection.insert_one(team)
        return insert

    def update(self, query_filter, team):
        update = self.collection.update_one(query_filter, team)
        return update

    def delete(self, query_filter):
        delete = self.collection.delete_one(query_filter)
        return delete