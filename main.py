from chess.stockfish import Stockfish
import chess.pgn
import os 
import plotext as plt
from alive_progress import alive_it

# check if the os is windows or linux
stockfish = Stockfish("./stockfish_15_linux.bin")
if os.name == "nt":
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    
# set the power of the engine to the max
stockfish.set_skill_level(20)

# read the board from the file
pgn = open("game.pgn")

game = chess.pgn.read_game(pgn)

max_eval = 2000
board = game.board()
evalution_list = []
is_white = True

white_player = game.headers["White"]
black_player = game.headers["Black"]

white_move_accuracy = []
black_move_accuracy = []

moves = list(game.mainline_moves())

print("The game is: ", game.headers["Event"])

for move in alive_it(moves, bar='bubbles'):    
    if is_white:
        white_move_accuracy.append(stockfish.move_eval(move, max_eval))
        is_white = False
    else:
        black_move_accuracy.append(stockfish.move_eval(move, max_eval))
        is_white = True    
    evalution_list.append(stockfish.decode_eval(max_eval))
    # print("The best move is: ", stockfish.get_best_move())
    # print("The move evalution is: ", stockfish.move_eval(move, max_eval))
    
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



