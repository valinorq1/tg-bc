from loguru import logger
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import (
    CommentTask,
    CustomUser,
    ReactionTask,
    SubscribeTask,
    ViewTask,
    VotingTask,
)

from .serializer.serializers import (
    CommentTaskSerializer,
    GetSubTaskSerializer,
    ReactionTaskSerializer,
    RegisterSerializer,
    ViewTaskSerializer,
    VoteTaskSerializer,
)


class ViewTaskApi(viewsets.ModelViewSet):
    queryset = ViewTask.objects.all()
    serializer_class = ViewTaskSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get"]

    def get_queryset(self):
        user = self.request.user
        return ViewTask.objects.filter(user=user)


class ViewTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Просмотры"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ViewTaskSerializer
    http_method_names = [
        "post",
        "get",
        "delete",
    ]

    def get_queryset(self):
        return ViewTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"success": False})

        return Response({"success": True})


class SubTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Просмотры"""

    permission_classes = (IsAuthenticated,)
    serializer_class = GetSubTaskSerializer
    http_method_names = ["post", "get", "delete"]

    def get_queryset(self):
        return SubscribeTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"success": False})

        return Response({"success": True})


class VoteTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Голосование"""

    permission_classes = (IsAuthenticated,)
    serializer_class = VoteTaskSerializer
    http_method_names = ["post", "get", "delete"]

    def get_queryset(self):
        return VotingTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"success": False})

        return Response({"success": True})


class ReactionTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Реакции"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ReactionTaskSerializer
    http_method_names = ["post", "get", "delete"]

    def get_queryset(self):
        return ReactionTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"success": False})

        return Response({"success": True})


class CommentTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Сообщения"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentTaskSerializer
    http_method_names = ["post", "get", "delete"]

    def get_queryset(self):
        return CommentTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"success": False})

        return Response({"success": True})


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GetAllTaskView(generics.ListAPIView):
    """Получаем все активные задания пользователя"""

    serializer_sub_task = GetSubTaskSerializer
    serializer_view_task = ViewTaskSerializer
    serializer_comment_task = CommentTaskSerializer
    serializer_vote_task = VoteTaskSerializer
    serializer_reaction_task = ReactionTaskSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset_comment_task(self):
        return CommentTask.objects.filter(user=self.request.user)

    def get_queryset_views_task(self):
        return ViewTask.objects.filter(user=self.request.user)

    def get_queryset_sub_task(self):
        return SubscribeTask.objects.filter(user=self.request.user)

    def get_queryset_vote_task(self):
        return VotingTask.objects.filter(user=self.request.user)

    def get_queryset_reaction_task(self):
        return ReactionTask.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        view_t = self.serializer_view_task(self.get_queryset_views_task(), many=True)
        sub_t = self.serializer_sub_task(self.get_queryset_sub_task(), many=True)
        com_t = self.serializer_comment_task(
            self.get_queryset_comment_task(), many=True
        )
        vote_t = self.serializer_vote_task(self.get_queryset_vote_task(), many=True)
        react_t = self.serializer_reaction_task(
            self.get_queryset_reaction_task(), many=True
        )
        return Response(
            {
                "sub_task": sub_t.data,
                "view_task": view_t.data,
                "comment_task": com_t.data,
                "vote_task": vote_t.data,
                "react_task": react_t.data,
            }
        )
