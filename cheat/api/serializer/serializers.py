from dataclasses import fields
from importlib.metadata import requires

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from loguru import logger
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from tasks.models import (CommentTask, CustomUser, ReactionTask, SubscribeTask,
                          TaskMixin, ViewTask, VotingTask)


class RegisterSerializer(serializers.ModelSerializer):
    """Валидируем и регистрируем пользователя"""

    User = get_user_model()
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("password", "password2", "email")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "id"]


class ViewTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    begin_time = serializers.DateTimeField(required=False)


    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(ViewTaskSerializer, self).to_representation(instance)

    class Meta:
        model = ViewTask
        fields = ['id', 'channel', 'amount', 'count_last_posts', 'count_per_post',
                  'count_avg', 'processed_count', 'price', 'duration', 'task_duration', 
                  'max_speed', 'processed', 'begin_time', 'user']


class GetSubTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задания подписки"""

    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(GetSubTaskSerializer, self).to_representation(instance)

    class Meta:
        model = SubscribeTask
        exclude = ("gender_choice",)


class CommentTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задания комментариев"""

    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(CommentTaskSerializer, self).to_representation(instance)

    class Meta:
        model = CommentTask
        fields = "__all__"


class VoteTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задания голосования"""

    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(VoteTaskSerializer, self).to_representation(instance)

    class Meta:
        model = VotingTask
        fields = "__all__"


class ReactionTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задания голосования"""

    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(ReactionTaskSerializer, self).to_representation(instance)

    class Meta:
        model = ReactionTask
        fields = "__all__"
