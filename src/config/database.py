
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def init_connect():
    try:
        uri = "mongodb+srv://phnovais7:9bFjBz7t8juhwry6@automatize.gqwk6.mongodb.net/?retryWrites=true&w=majority&appName=automatize"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['automatize']
        client.admin.command('ping')
        print("Conection with database, sucesfull")
        return db
    except Exception as e:
        print(e)