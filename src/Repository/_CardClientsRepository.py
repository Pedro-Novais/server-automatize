from ._BaseRepository import BaseRepository

class CardsClientsRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.collection = self.db['cardsPayments']