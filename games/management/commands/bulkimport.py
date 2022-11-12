from django.core.management.base import BaseCommand, CommandError
import glob
from datetime import datetime
import chess, chess.pgn

from games.models import ChessGame
from events.models import ChessEvent, ChessRound
from players.models import ChessPlayer



class PGNImporter:
    def __init__(self, filename: str):
        self.filename = filename
        with open(self.filename) as pgn:
            self.game = chess.pgn.read_game(pgn)
            self.date = None
            self.standardize_tags()

    def standardize_tags(self) -> dict:
        header_dict = {}

        for k,v in self.game.headers.items():
            if "?" not in v:
                header_dict[k] = v

        date = self.game.headers.get("Date", None)
        if date is not None:
            self.date = datetime.strptime(date, "%Y.%m.%d")

        self.game.headers.clear()
        self.game.headers.update(header_dict)

        return header_dict

def romanicize_name(name: str) -> str:
    return f"Test {name}"


class Command(BaseCommand):
    help = 'Imports all available files into the database'

    def handle(self, *args, **options):
        files = glob.glob("pgn/*.pgn")
        count = 0
        created_count = 0

        for file in files:
            self.stdout.write(self.style.NOTICE('Processing "%s"' % file))
            try:
                importer = PGNImporter(file)
                
                # Process the event, if specified
                event_header = importer.game.headers.get("Event", None)
                if event_header is not None:
                    event, e_created = ChessEvent.objects.get_or_create(name=event_header, defaults={
                        'site': importer.game.headers.get("Site", None)
                    })

                    round_header = importer.game.headers.get("Round", None)
                    if round_header is not None:
                        round, r_created = ChessRound.objects.get_or_create(event=event, num=round_header)

                # Save a copy of the imported PGN
                pgn_string = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
                imported_pgn = importer.game.accept(pgn_string)

                # Get the object of each player
                white_player, w_created = ChessPlayer.objects.get_or_create(
                    name=romanicize_name(importer.game.headers.get("White"))
                )
                
                black_player, b_created = ChessPlayer.objects.get_or_create(
                    name=romanicize_name(importer.game.headers.get("Black"))
                )
                
                white_elo = importer.game.headers.get("WhiteELO", None)
                if white_elo is not None:
                    white_elo = int(white_elo)
                
                black_elo = importer.game.headers.get("BlackELO", None)
                if black_elo is not None:
                    black_elo = int(black_elo)
                

                # Determine the winner of the game
                winner = None
                if importer.game.headers.get("Result", None) == "1-0":
                    winner=white_player
                elif importer.game.headers.get("Result", None) == "0-1":
                    winner=black_player


                # Create the game object
                game_obj, g_created = ChessGame.objects.get_or_create(
                    date=importer.date,
                    hashcode=importer.game.headers.get("HashCode"),
                    winner=winner,
                    defaults={
                        "event": event,
                        "round": round,
                        "white": white_player,
                        "black": black_player,
                        "white_elo": white_elo,
                        "black_elo": black_elo,
                        "total_ply_count": int(importer.game.headers.get("TotalPlyCount")),
                        "imported_pgn": imported_pgn
                    }
                )

                if g_created:
                    created_count += 1
                
                count += 1


            except Exception as e:
                self.stderr.write(self.style.ERROR_OUTPUT('Unspecified error processing %s: %s' % (file, e)))
            
        self.stdout.write(self.style.SUCCESS('Successfully processed %s/%s files (%s new)' % (count, len(files), created_count)))
