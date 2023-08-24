from flask import Flask, render_template, request, redirect, url_for, session
from chess.stockfish import Stockfish
import chess.pgn
import os 
import plotext as plt
from alive_progress import alive_it

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from chess.hashgame import gameHash

import chessDataBase


uri = "mongodb+srv://swalha:12345678911@chess.t4z9lx3.mongodb.net/?retryWrites=true&w=majority"
database = chessDataBase.ChessGameDatabase(uri)
database.connect()


print("reading the game from the file")

# lets check if the seen the game before by hashing the game and check if it exists in the database

pgn = open("game.pgn")
game = chess.pgn.read_game(pgn)
moves = list(game.mainline_moves())
gameDict = dict(game.headers)

# reload the file for the hash function
pgn = open("game.pgn")
gameDict["hash"] = gameHash(pgn)
print (gameDict["hash"])

if database.getGames().find_one({"hash": gameDict["hash"]}):
    print("The game is in the database")
else:
    database.getGames().insert_one(gameDict)
    print("The game is not in the database")

# check if the os is windows or linux
stockfish = Stockfish("./stockfish_15_linux.bin")
if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    
# set the power of the engine to the max
stockfish.set_skill_level(20)

# read the board from the file



max_eval = 2000
board = game.board()
evalution_list = []
is_white = True

white_player = game.headers["White"]
black_player = game.headers["Black"]

white_move_accuracy = []
black_move_accuracy = []

moves = list(game.mainline_moves())


database.getGames().insert_one(gameDict)
database.getGames().delete_one({"hash": hash(pgn)})
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