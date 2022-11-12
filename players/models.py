from typing import List
from django.db import models

# Create your models here.
class ChessPlayer(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, help_text="Romanicized name")
    
    def __str__(self):
        return self.name
        

