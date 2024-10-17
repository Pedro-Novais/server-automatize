from ._BaseRepository import BaseRepository

class ProjectRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.collection = self.db['project']