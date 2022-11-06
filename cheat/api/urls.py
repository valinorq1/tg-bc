from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register("view-task", views.ViewTaskViewSet, basename="view_task")
router.register("sub-task", views.SubTaskViewSet, basename="create_sub_task")

router.register("vote-task", views.VoteTaskViewSet, basename="create_vote_task")
router.register(
    "reaction-task",
    views.ReactionTaskViewSet,
    basename="create_reaction_task",
)
router.register(
    "comment-task",
    views.CommentTaskViewSet,
    basename="create_comment_task",
)


router.register("tasks", views.ViewTaskApi)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("all-tasks/", views.GetAllTaskView.as_view(), name="auth_register"),
    path("", include("rest_framework.urls", namespace="rest_framework")),
]
