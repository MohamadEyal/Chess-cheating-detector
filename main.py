from chess.stockfish import Stockfish
import chess.pgn
import os 
import plotext as plt

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

print(stockfish.get_top_moves(10))
print(stockfish.get_evaluation())


for move in game.mainline_moves():
    print(move)
    evalution = stockfish.get_evaluation()["value"]
    print("The best move is: ", stockfish.get_best_move())
    print("The current evaluation is: ", evalution)
    

    if abs(evalution) > max_eval:
        evalution = max_eval if evalution > 0 else -max_eval

    evalution_list.append(evalution)

    print( board.unicode())
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