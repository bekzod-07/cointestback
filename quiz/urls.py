from django.urls import path
from .views import QuestionListView, SubmitTestView

from .views import QuestionListView, SubmitTestView, LeaderboardTop10View, MyRankView

urlpatterns = [
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("submit/", SubmitTestView.as_view(), name="test-submit"),
    path("leaderboard/top10/", LeaderboardTop10View.as_view(), name="leaderboard-top10"),
    path("leaderboard/me/", MyRankView.as_view(), name="leaderboard-me"),
]

