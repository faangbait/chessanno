from django.db import models
from events.models import ChessEvent, ChessRound
from players.models import ChessPlayer
# Create your models here.
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
