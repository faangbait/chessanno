from parse import state, analyze
import pytest
import chess, chess.engine
from datetime import datetime

@pytest.fixture
def default_board():
    return chess.Board()

def test_slugify(default_board):
    assert state.slugify(default_board) == "rnbqkbnr.pppppppp.8.8.8.8.PPPPPPPP.RNBQKBNR_w_KQkq_-_0_1"

def test_deslugify(default_board):
    assert state.deslugify("rnbqkbnr.pppppppp.8.8.8.8.PPPPPPPP.RNBQKBNR_w_KQkq_-_0_1") == default_board

@pytest.fixture
def mate_in_one():
    return chess.Board("rnbqkbnr/ppppp2p/5p2/6p1/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 3")

def test_analyze(mate_in_one):
    assert analyze.fish(mate_in_one.fen())  > 90000

# TODO rewrite as command call
# def test_import():
#     importer = load.PGNImporter("tests/single-game.pgn")
#     assert importer.game.headers.get("Event") == "Chess.com RCC Wk16 Swiss"
#     assert importer.game.headers.get("Site") == "chess.com INT"
#     assert importer.game.headers.get("Date") == "2022.05.28"
#     assert importer.date == datetime(2022, 5, 28)
#     assert importer.game.headers.get("WhiteElo") == "2501"
#     assert importer.game.headers.get("White") == "Priasmoro, Novendra"

