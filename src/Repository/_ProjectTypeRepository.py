from ._BaseRepository import BaseRepository

class ProjectTypeRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.collection = self.db['projectType']