
# interface for mongoDB to save chess games data 

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ChessGameDatabase:
    def __init__(self, mongoUrl='chess_games.db'):
        self.db_url = mongoUrl
        self.conn = None
    
    def connect(self):
        # Create a new client and connect to the server
        self.conn = MongoClient(self.db_url, server_api=ServerApi('1'))
        try:
            self.conn.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB! Database:", self.conn.list_database_names())
        except Exception as e:
            print(e)

    def getGames(self):
        return self.conn["chess"]["games"]
    
    def getPlayers(self):
        return self.conn["chess"]["players"]
    
    def addplayer(self, player):
        self.getPlayers().insert_one(player)

    def close(self):
        self.conn.close()