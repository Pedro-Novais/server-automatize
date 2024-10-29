class BaseRepository:
    def get(self, query_filter: dict, projection: dict | None = None) -> dict:
        team = self.collection.find_one(query_filter, projection)
        return team
    
    def get_sort(self, key: str, type_search: int, filter: dict) -> dict:
        get = self.collection.find_one(filter, sort=[(key, type_search)])
        return get
    
    def get_many(self, query_filter: dict, projection: dict | None = None) -> list:
        team = self.collection.find(query_filter, projection)
        return team
    
    def get_update(self, query_filter: dict, update: dict, return_doc: bool = False):
        data = self.collection.find_one_and_update(query_filter, update, return_document=return_doc)
        return data
    
    def post(self, data):
        insert = self.collection.insert_one(data)
        return insert

    def update(self, query_filter, update):
        update = self.collection.update_one(query_filter, update)
        return update

    def delete(self, query_filter):
        delete = self.collection.delete_one(query_filter)
        return delete