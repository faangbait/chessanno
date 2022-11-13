import chess
import chess.engine, chess.pgn

def pov_eval(score: chess.engine.PovScore) -> int:
    return score.pov(chess.WHITE).score(mate_score=100000)

def fish_eval(info: chess.engine.InfoDict) -> int:
    score = info.get("score",None)
    if score is not None:
        return pov_eval(score)
    return 0


def fish(fen: str, depth = 10) -> chess.engine.InfoDict:
    engine = chess.engine.SimpleEngine.popen_uci("bin/stockfish")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    engine.quit()
    return info

def set_nag(node: chess.pgn.ChildNode):
    node.nags
