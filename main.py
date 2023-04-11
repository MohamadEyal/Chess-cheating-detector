from stockfish import Stockfish

stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")

stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

print(stockfish.get_best_move())

