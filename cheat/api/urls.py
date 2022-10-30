from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register(
    "create-view-task", views.CreateViewTaskViewSet, basename="create_view_task"
)
router.register(
    "create-sub-task", views.CreateSubTaskViewSet, basename="create_sub_task"
)

router.register(
    "create-vote-task", views.CreateVoteTaskViewSet, basename="create_vote_task"
)
router.register(
    "create-reaction-task",
    views.CreateReactionTaskViewSet,
    basename="create_reaction_task",
)
router.register(
    "create-comment-task",
    views.CreateCommentTaskViewSet,
    basename="create_comment_task",
)


router.register("tasks", views.ViewTaskApi)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("all-tasks/", views.GetAllTaskView.as_view(), name="auth_register"),
    path("", include("rest_framework.urls", namespace="rest_framework")),
]
