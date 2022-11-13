from django.urls import path
from .views import GameDetail, GameList, create_analysis, create_comment

app_name='games'

urlpatterns = [
    path("<int:pk>/<int:ply>/", GameDetail.as_view(), name="detail"),
    path("<int:pk>/", GameDetail.as_view(), name="detail"),
    path("<int:pk>/analyze", create_analysis, name="analyze"),
    path("<int:pk>/<int:ply>/comment", create_comment, name="comment"),
    path("", GameList.as_view(), name="list"),
]
