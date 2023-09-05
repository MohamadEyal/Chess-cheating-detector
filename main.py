from alive_progress import alive_it

import os 
import plotext as plt


import chessDataBase
from ReadGame import ChessGameReader

from chess.stockfish import Stockfish

# Database connection
uri = "mongodb+srv://swalha:12345678911@chess.t4z9lx3.mongodb.net/?retryWrites=true&w=majority"
database = chessDataBase.ChessGameDatabase(uri)
database.connect()

game =  ChessGameReader("game.pgn")
print(database.check_if_game_exist(game))
print(game.get_hash())


# for game in database.playerGames("swalha1999"):
#     print(game)


print("reading the game from the file")

game = ChessGameReader("game.pgn")
gameDict = game.get_headers()


if database.getGames().find_one({"hash": gameDict["hash"]}):
    print("The game is in the database")
else:
    database.getGames().insert_one(gameDict)
    print("The game is not in the database")

# check if the os is windows or linux
stockfish = Stockfish("./stockfish_15_linux.bin")
if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    
stockfish.set_skill_level(20)

max_eval = 2000
board = game.board()
evalution_list = []
is_white = True

white_player = game.headers["White"]
black_player = game.headers["Black"]

white_move_accuracy = []
black_move_accuracy = []

moves = list(game.mainline_moves())


for move in alive_it(moves, bar='bubbles'):    
    if is_white:
        white_move_accuracy.append(stockfish.move_eval(move, max_eval))
        is_white = False
    else:
        black_move_accuracy.append(stockfish.move_eval(move, max_eval))
        is_white = True    
    evalution_list.append(stockfish.decode_eval(max_eval))
    print("The best move is: ", stockfish.get_best_move())
    print("The move evalution is: ", stockfish.move_eval(move, max_eval))
    
    print( board.unicode(), "-----------------")

    board.push(move)
    stockfish.make_moves_from_current_position([move])
    

print("White player: ", white_player)
print("Black player: ", black_player)

plt.plot(evalution_list)
plt.title("Evaluation of the game")
plt.xlabel("Move")
plt.ylabel("Evaluation")
plt.ylim(-max_eval, max_eval)
plt.theme("clear")
plt.show()



database.close()

