from loguru import logger
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import CommentTask, CustomUser, SubscribeTask, ViewTask, VotingTask

from .serializer.serializers import (
    CommentTaskSerializer,
    GetSubTaskSerializer,
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


class CreateViewTaskViewSet(viewsets.ModelViewSet):
    """Добавляем задачу для клиента: Просмотры"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ViewTaskSerializer
    http_method_names = ["post"]

    def get_queryset(self):
        return ViewTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GetAllTaskView(generics.ListAPIView):
    serializer_sub_task = GetSubTaskSerializer
    serializer_view_task = ViewTaskSerializer
    serializer_comment_task = CommentTaskSerializer
    serializer_vote_task = VoteTaskSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset_comment_task(self):
        return CommentTask.objects.filter(user=self.request.user)

    def get_queryset_views_task(self):
        return ViewTask.objects.filter(user=self.request.user)

    def get_queryset_sub_task(self):
        return SubscribeTask.objects.filter(user=self.request.user)

    def get_queryset_vote_task(self):
        return VotingTask.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        view_t = self.serializer_view_task(self.get_queryset_views_task(), many=True)
        sub_t = self.serializer_sub_task(self.get_queryset_sub_task(), many=True)
        com_t = self.serializer_comment_task(
            self.get_queryset_comment_task(), many=True
        )
        vote_t = self.serializer_vote_task(self.get_queryset_vote_task(), many=True)
        return Response(
            {
                "sub_task": sub_t.data,
                "view_task": view_t.data,
                "comment_task": com_t.data,
                "vote_task": vote_t.data,
            }
        )
