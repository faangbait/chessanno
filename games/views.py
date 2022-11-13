from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic import DetailView, ListView
from .models import ChessGame
from typing import Any, Dict
import chess, chess.pgn, chess.svg
from parse import analyze, state
from .forms import CommentForm
class GameDetail(DetailView):
    model = ChessGame

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # UI
        context["nav"] = "games"

        # Traverse to correct ply
        current_ply = self.kwargs.get("ply", 1)
        context["current_ply"] = current_ply
        current_position: chess.pgn.ChildNode = self.object.at_ply(current_ply) # type: ignore

        # Describe the game for the template
        fish = current_position.eval()
        if fish is not None:
            context["eval"] = fish.pov(chess.WHITE).score(mate_score=100000) / 100

        if current_ply > 1:
            context["last_href"] = reverse("games:detail",kwargs={"pk": self.kwargs.get("pk"), "ply": current_ply - 1})
        if current_ply < self.object.total_ply_count: # type: ignore
            context["next_href"] = reverse("games:detail",kwargs={"pk": self.kwargs.get("pk"), "ply": current_ply + 1})

        check=None
        lastmove=None

        context["last_move"] = current_position.move
        
        if current_position.board().is_check():
            check=current_position.move.to_square
        else:
            lastmove=current_position.move

        context["comment"] = state.get_comment(current_position)
        context["comment_form"] = CommentForm(initial={"comment": context["comment"]})
        context["variations"] = current_position.variations
        context["svg"] = chess.svg.board(current_position.board(), lastmove=lastmove, check=check)
    
        return context

class GameList(ListView):
    model = ChessGame

def create_analysis(request, pk, depth=10):
    try:
        obj = ChessGame.objects.get(pk=pk)
        game = obj.game
        for node in game.mainline():
            fish = analyze.fish(node.board().fen(), depth)
            node.set_eval(fish.get("score"), depth)
        
        obj.processed_pgn = state.game_to_pgn(game)
        obj.save()

    except Exception:
        raise Exception("Unspecified analysis error")

    
    return redirect("games:detail", pk)

def create_comment(request: HttpRequest, pk: int, ply: int):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = ChessGame.objects.get(pk=pk)
            game = obj.at_ply(ply)
            game = state.set_comment(game, request.POST.get("comment", ""))
            obj.processed_pgn = state.game_to_pgn(game.game())
            obj.save()
    else:
        obj = ChessGame.objects.get(pk=pk)
        game = obj.at_ply(ply)
        existing_comment = state.get_comment(game)
        form = CommentForm(initial={"comment": existing_comment})
    return redirect("games:detail", pk, ply+1)
        
