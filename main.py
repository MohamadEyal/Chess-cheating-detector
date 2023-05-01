from chess.stockfish import Stockfish
import chess.pgn
import os 

# check if the os is windows or linux
stockfish = Stockfish("./stockfish_15_linux.bin")
if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    
# set the power of the engine to the max
stockfish.set_skill_level(20)


# read the board from the file
pgn = open("game.pgn")

game = chess.pgn.read_game(pgn)

for move in game.mainline_moves():
    print("The best move is: ", stockfish.get_best_move())
    print("The current board is:\n", stockfish.get_board_visual())
    stockfish.make_moves_from_current_position([move])