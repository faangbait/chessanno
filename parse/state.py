import chess, chess.pgn
import io, re

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

def pgn_to_game(pgn: str) -> chess.pgn.Game:
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        raise Exception
    return game

def game_to_pgn(game: chess.pgn.Game) -> str:
    return game.accept(chess.pgn.StringExporter(headers=True, variations=True, comments=True))

def get_comment(node: chess.pgn.ChildNode) -> str:
    matches = re.match(r'(.*)\[', node.comment)
    if matches:
        return matches.groups()[0].strip()
    return ""

def set_comment(node: chess.pgn.ChildNode, comment: str) -> chess.pgn.ChildNode:
    node.comment = re.sub(r'(.*)\[', comment + "[", node.comment)
    return node
