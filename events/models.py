from django.db import models

# Create your models here.
class ChessEvent(models.Model):
    name = models.TextField(blank=True, null=True, help_text="Name of the tournament or match event")
    site = models.CharField(max_length=64, blank=True, null=True, help_text="Location of the event. City, Region, COUNTRY")

    def __str__(self):
        return self.name

class ChessRound(models.Model):
    event = models.ForeignKey(ChessEvent, on_delete=models.CASCADE)
    num = models.IntegerField(blank=True, null=True, help_text="Playing round ordinal of the game within the event")

    def __str__(self):
        return f"{self.event.name} R{self.num}"
