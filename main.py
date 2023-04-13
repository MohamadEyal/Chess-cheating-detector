from stockfish import Stockfish
import chess
import chess.pgn

# read the pgn gmae and get all the moves

pgn_file = open("game.pgn")
game = chess.pgn.read_game(pgn_file)
board = game.board()
sf = Stockfish("stockfish_20011801_x64.exe")
# we can access the moves in the game using the mainline_moves() method
# we get an array of moves and we can iterate over it

for move in game.mainline_moves():
    print(move)

