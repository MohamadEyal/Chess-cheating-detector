from stockfish import Stockfish
import chess
import chess.pgn

# read the pgn gmae and get all the moves

pgn_file = open("game.pgn")
game = chess.pgn.read_game(pgn_file)

board = game.board() # get the board from the game object

white_player = game.headers["White"] # get the white player name
black_player = game.headers["Black"] # get the black player name


sf = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
# we can access the moves in the game using the mainline_moves() method
# we get an array of moves and we can iterate over it

for move in game.mainline_moves():
    # we can use the push() method to make the move on the board
    board.push(move)

    print(move)

print(white_player, "vs", black_player)