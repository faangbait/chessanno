import chess, chess.pgn
from datetime import datetime


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
