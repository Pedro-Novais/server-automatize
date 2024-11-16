from ._BaseRepository import BaseRepository

class SubscriptionsRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.collection = self.db['subscriptions']