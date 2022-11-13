from django.test import TestCase
import pytest
import io
from datetime import datetime
import chess.pgn
from parse.state import pgn_to_game

from .models import ChessGame
from players.models import ChessPlayer

@pytest.fixture
def loaded_pgn():
    return pgn_to_game("1. e4 f6 2. d4 c6 3. Nf3 d6 4. Bd3 e5 5. c3 Be6")

def test_game_at_ply():
    game = ChessGame(
        white=ChessPlayer(name="white_player"),
        black=ChessPlayer(name="black_player"),
        hashcode="aoeuhtns",
        date=datetime.now(),
        total_ply_count=10,
        imported_pgn="1. e4 f6 2. d4 c6 3. Nf3 d6 4. Bd3 e5 5. c3 Be6"
    )
    node = game.at_ply(1)
    assert node.move.uci() == "e2e4"
    node = game.at_ply(2)
    assert node.move.uci() == "f7f6"
    node = game.at_ply(3)
    assert node.move.uci() == "d2d4"
    node = game.at_ply(4)
    assert node.move.uci() == "c7c6"
    node = game.at_ply(10)
    assert node.move.uci() == "c8e6"
    
