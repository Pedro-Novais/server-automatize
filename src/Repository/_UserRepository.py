class UserRepository:
    def __init__(self, db):
        self.collection = db['users']

    def get_user(self, query_filter, projection):
        user = self.collection.find_one(query_filter, projection)
        return user

    def insert_user(self, user):
        self.collection.insert_one(user)

    def update_user(self, query_filter, update_values):
        self.collection.update_one(query_filter, update_values)
        return True

    def delete_user(self, query_filter):
        delete = self.collection.delete_one(query_filter)
        
        return delete
    