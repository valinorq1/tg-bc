from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()


router.register("users", views.ProfileApiView)
router.register("create-view-task", views.CreateViewTaskViewSet, basename="cutareadel")

router.register("test2", views.ViewTaskApi)


urlpatterns = [
    path("", include(router.urls)),
    path("test/", views.create_task, name="hihih"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("", include("rest_framework.urls", namespace="rest_framework")),
]
