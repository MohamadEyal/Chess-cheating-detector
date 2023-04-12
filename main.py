from stockfish import Stockfish
import chess

black_accuracy = 0
white_accuracy = 0

chess_board = chess.Board()

# read a pgn file and play the game and get the all the moves 

moves = []
game_moves_string = ""

with open("game.pgn") as f:
    for line in f:
        if line.startswith("["):
            continue
        
        # join the lines to get the moves
        game_moves_string += (line.strip("\n") + " ")


for move in game_moves_string.split("."):
    split_move = move.split(" ")
    
    
    if len(split_move) < 3:
        continue
    
    if "-" in split_move[1]: 
        continue
    
    #make white move
    moves.append(str(chess_board.push_san(split_move[1])))

    #make black move
    if "-" not in split_move[2]:
            moves.append(str(chess_board.push_san(split_move[2])))    
    
    
    
print(moves)

stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")

#go throw all the moves and get the best move for each move
move_number_w = 1
move_number_b = 1

black_accuracy = 0
white_accuracy = 0

for move in moves:
    best_move = stockfish.get_best_move_time(1000)
    if move_number_b < move_number_w:
        print("black " + str(move_number_b)+". " + "played move: "+move +" --> best move: " + best_move)
        move_number_b += 1
        if move == best_move:
            black_accuracy += 1
    else:
        print("white "+ str(move_number_w)+". " + "played move: "+move +" --> best move: " + best_move)
        move_number_w += 1
        if move == best_move:
            white_accuracy += 1
    stockfish.make_moves_from_current_position([move])


print ("white accuracy: " + str(white_accuracy/(move_number_w-1)))
print ("black accuracy: " + str(black_accuracy/(move_number_b-1)))