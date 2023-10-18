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

if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
else:
    stockfish = Stockfish("./stockfish_15_linux.bin")   
stockfish.set_skill_level(20)

max_eval = 2000
board = game.board()
is_white = True

white_player = game.headers["White"]
black_player = game.headers["Black"]

white_best_moves = 0
white_vgood_moves = 0
white_good_moves = 0
white_all_moves =0 
black_best_moves = 0
black_vgood_moves = 0
black_good_moves = 0
black_all_moves = 0
evalution_list = []

moves = list(game.mainline_moves())


for move in alive_it(moves, bar='bubbles'):    
    if is_white: 
        li=stockfish.get_top_moves(3)
        for i in range(len(li)):
            if(str(li[i].get('Move'))==str(move)):
                if i==0:
                    white_best_moves=white_best_moves+1
                elif i==1:
                    white_vgood_moves=white_vgood_moves+1
                elif i==1:
                    white_good_moves=white_good_moves+1
        white_all_moves=white_all_moves+1
        #white_move_accuracy.append(stockfish.move_eval(str(stockfish.get_best_move()), max_eval) - stockfish.move_eval(move, max_eval))
        is_white = False
    else:
        li=stockfish.get_top_moves(3)
        for i in range(len(li)):
            if(str(li[i].get('Move'))==str(move)):
                if i==0:
                    black_best_moves=black_best_moves+1
                elif i==1:
                    black_vgood_moves=black_vgood_moves+1
                elif i==1:
                    black_good_moves=black_good_moves+1
        black_all_moves=black_all_moves+1
        #black_move_accuracy.append(stockfish.move_eval(str(stockfish.get_best_move()), max_eval) - stockfish.move_eval(move, max_eval))
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
    database.addPlayer(white_player, white_best_moves/white_all_moves, white_vgood_moves/white_all_moves, white_vgood_moves/white_all_moves, game.headers["Date"])
    database.addPlayer(black_player, black_best_moves/black_all_moves, black_vgood_moves/black_all_moves, black_good_moves/black_all_moves, game.headers["Date"])
    database.getGames().insert_one(gameDict)

white_all_time_best = []
white_all_time_vgood = []
white_all_time_good = []
for PlayerGame in database.getPlayer(white_player):
    white_all_time_best.append(PlayerGame["best"])
    white_all_time_vgood.append(PlayerGame["vgood"])
    white_all_time_good.append(PlayerGame["good"])


black_all_time_best = []
black_all_time_vgood = []
black_all_time_good = []
for PlayerGame in database.getPlayer(black_player):
    black_all_time_best.append(PlayerGame["best"])
    black_all_time_vgood.append(PlayerGame["vgood"])
    black_all_time_good.append(PlayerGame["good"])

print("White player all time best moves percent: ", white_all_time_best)
print("White player all time very good moves percent: ", white_all_time_vgood)
print("White player all time good moves percent: ", white_all_time_good)
print("Black player all time best moves percent: ", black_all_time_best)
print("Black player all time very good moves percent: ", black_all_time_vgood)
print("Black player all time good moves percent: ", black_all_time_good)

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
plt.plot(white_all_time_best)
plt.title(white_player + " White all time best moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(white_all_time_vgood)
plt.title(white_player + " White all time very good moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(white_all_time_good)
plt.title(white_player + " White all time good moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()



plt.clear_data()
plt.plot(black_all_time_best)
plt.title(black_player + " black all time best moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(black_all_time_vgood)
plt.title(black_player + " black all time very good moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()

plt.clear_data()
plt.plot(black_all_time_good)
plt.title(black_player + " black all time good moves percent")
plt.xlabel("Games")
plt.ylabel("Percent")
plt.ylim(-1, 1)
plt.theme("clear")
plt.show()


database.close()

