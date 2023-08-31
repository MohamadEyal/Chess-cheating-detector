
import chess.pgn
from chess.hashgame import gameHash

class ChessGameReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name)
        self.game = chess.pgn.read_game(self.file)
        self.moves = list(self.game.mainline_moves())
        self.headers = dict(self.game.headers)
        
        self.file = open(file_name)
        self.headers["hash"] = gameHash(self.file)

        self.file = open(file_name)

    def get_headers(self):
        return self.headers

    def get_game(self):
        return self.game

    def get_file_name(self):
        return self.file_name

    def get_file(self):
        return self.file

    def close_file(self):
        self.file.close()

    def board(self):
        board = self.game.board()
        return board
    
    def mainline_moves(self):
        return self.moves
    
    def get_hash(self):
        return self.headers["hash"]