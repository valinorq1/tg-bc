from django.contrib.auth.models import User
from django.shortcuts import render
from loguru import logger
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser, ViewTask

from .serializer.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    ViewTaskSerializer,
)


class ProfileApiView(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all().values()

    logger.debug(queryset[0]["balance"])

    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]


@api_view(["POST", "GET"])
def create_task(request):

    serializer = ViewTaskSerializer(data=request.data)
    logger.debug(request.data)
    if serializer.is_valid():
        logger.debug("is VALID")
        serializer.save()
        # logger.debug(serializer)
    else:
        logger.debug("NOT A VALID")
    return Response(serializer.data)


class ViewTaskApi(viewsets.ModelViewSet):

    queryset = ViewTask.objects.all().values()

    serializer_class = ViewTaskSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        user = self.request.user
        return ViewTask.objects.filter(user=user)


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
