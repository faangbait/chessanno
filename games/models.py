import io
import chess.pgn
from django.db import models
from events.models import ChessEvent, ChessRound
from players.models import ChessPlayer
from parse.state import pgn_to_game

class ChessGame(models.Model):
    event = models.ForeignKey(ChessEvent, on_delete=models.SET_NULL, blank=True, null=True, help_text="The tournament or match event")
    round = models.ForeignKey(ChessRound, on_delete=models.SET_NULL, blank=True, null=True, help_text="The round of the tournament")
    date = models.DateField(blank=True, null=True, help_text="Starting date of the game")
    white = models.ForeignKey(ChessPlayer, on_delete=models.CASCADE, help_text="Player of the white pieces", related_name='white_games')
    white_elo = models.IntegerField(blank=True, null=True)
    black = models.ForeignKey(ChessPlayer, on_delete=models.CASCADE, help_text="Player of the black pieces", related_name='black_games')
    black_elo = models.IntegerField(blank=True, null=True)
    winner = models.ForeignKey(ChessPlayer, blank=True, null=True, on_delete=models.CASCADE, help_text="Winner of the game; None for draw")
    hashcode = models.CharField(max_length=8, help_text="A hash code of the moves in the game")
    total_ply_count = models.IntegerField()
    imported_pgn = models.TextField(help_text="The imported PGN of the game")
    processed_pgn = models.TextField(blank=True, null=True, help_text="The PGN after the annotator has visited it")

    def __str__(self):
        return self.hashcode

    @property
    def game(self) -> chess.pgn.Game:
        if self.processed_pgn is not None:
            pgn = chess.pgn.read_game(io.StringIO(self.processed_pgn))    
        else:
            pgn = chess.pgn.read_game(io.StringIO(self.imported_pgn))
        
        if pgn is None:
            raise Exception("Error reading pgn string")
        return pgn
    
    @property
    def result(self) -> str:
        if not self.winner:
            return "1/2 - 1/2"
        if self.winner == self.black:
            return "0-1"
        if self.winner == self.white:
            return "1-0"
        return "*"

    def at_ply(self, ply: int) -> chess.pgn.ChildNode:
        if ply > self.total_ply_count:
            raise Exception("This game has fewer plies than requested")

        game = self.game.variation(0)

        if game is None:
            raise Exception("Couldn't get main variation for game")
        
        for _ in range(1, ply):
            next_child = game.next()
            if next_child is not None:
                game = next_child

        return game

