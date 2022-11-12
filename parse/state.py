import chess

def slugify(board: chess.Board) -> str:
    raw_fen = board.fen()

    return raw_fen.translate({
        ord(" "): ord("_"),
        ord("/"): ord(".")
    })

def deslugify(slug_fen: str) -> chess.Board:
    return chess.Board(slug_fen.translate({
        ord("_"): ord(" "),
        ord("."): ord("/")
    }))
