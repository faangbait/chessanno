import chess
import chess.engine

def pov_eval(score: chess.engine.PovScore) -> int:
    centipawns = score.pov(chess.WHITE)

    return centipawns.score(mate_score=100000)


def fish(fen: str, depth = 20) -> int:
    engine = chess.engine.SimpleEngine.popen_uci("bin/stockfish")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    engine.quit()

    cp = info.get("score",None)

    if cp is not None:
        return pov_eval(cp)
    return 0

