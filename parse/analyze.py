import chess
import chess.engine

def pov_eval(score: chess.engine.PovScore) -> int:
    centipawns: chess.engine.Cp | chess.engine.Mate = score.pov(chess.WHITE)

    if centipawns.is_mate():
        return 100000
    else:
        return centipawns.cp


def fish(fen: str, depth = 20) -> int:
    engine = chess.engine.SimpleEngine.popen_uci("bin/stockfish")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    engine.quit()
    return pov_eval(info["score"])

