from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register(
    "create-view-task", views.CreateViewTaskViewSet, basename="create_view_task"
)

router.register("tasks", views.ViewTaskApi)
# router.register("all-tasks", views.GetAllTaskView)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("all-tasks/", views.GetAllTaskView.as_view(), name="auth_register"),
    path("", include("rest_framework.urls", namespace="rest_framework")),
]
