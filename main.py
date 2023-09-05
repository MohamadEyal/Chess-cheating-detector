from alive_progress import alive_it

import os 
import plotext as plt
import sys


import chessDataBase
from ReadGame import ChessGameReader

from chess.stockfish import Stockfish

# Database connection
uri = "mongodb+srv://swalha:12345678911@chess.t4z9lx3.mongodb.net/?retryWrites=true&w=majority"
database = chessDataBase.ChessGameDatabase(uri)
database.connect()


game = ChessGameReader(sys.argv[1])
gameDict = game.get_headers()

if database.getGames().find_one({"hash": game.get_hash()}):
    print("The game", sys.argv[1], "is in the database")
    exit()


# check if the os is windows or linux
stockfish = Stockfish("./stockfish_15_linux.bin")
if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    
stockfish.set_skill_level(20)

max_eval = 2000
board = game.board()
is_white = True

white_player = game.headers["White"]
black_player = game.headers["Black"]

white_move_accuracy = []
black_move_accuracy = []
evalution_list = []

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
    

# save the game in the database and each player average accuracy

if database.getGames().find_one({"hash": gameDict["hash"]}):
    print("The game is in the database")
else:
    print("The game is not in the database")
    database.addPlayer(white_player, sum(white_move_accuracy)/len(white_move_accuracy), game.headers["Date"])
    database.addPlayer(black_player, sum(black_move_accuracy)/len(black_move_accuracy), game.headers["Date"])
    database.getGames().insert_one(gameDict)

white_all_time_accuracy = []
for PlayerGame in database.getPlayer(white_player):
    white_all_time_accuracy.append(PlayerGame["accuracy"])

black_all_time_accuracy = []
for PlayerGame in database.getPlayer(black_player):
    black_all_time_accuracy.append(PlayerGame["accuracy"])

print("White player all time accuracy: ", white_all_time_accuracy)
print("Black player all time accuracy: ", black_all_time_accuracy)

print("White player: ", white_player)
print("Black player: ", black_player)

plt.plot(evalution_list)
plt.title("Evaluation of the game")
plt.xlabel("Move")
plt.ylabel("Evaluation")
plt.ylim(-max_eval, max_eval)
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(white_all_time_accuracy)
plt.title("White all time accuracy")
plt.xlabel("Games")
plt.ylabel("Accuracy")
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(black_all_time_accuracy)
plt.title("Black all time accuracy")
plt.xlabel("Games")
plt.ylabel("Accuracy")
plt.theme("clear")
plt.show()


database.close()

