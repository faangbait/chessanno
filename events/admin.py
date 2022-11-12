from django.contrib import admin
from .models import ChessEvent, ChessRound
# Register your models here.
admin.site.register(ChessEvent)
admin.site.register(ChessRound)
