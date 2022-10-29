from importlib.metadata import requires

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from loguru import logger
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from users.models import CustomUser, TaskMixin, ViewTask


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]


class ViewTaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = ViewTask
        fields = "__all__"


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
        fields = "__all__"


class CreateViewTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    begin_time = serializers.DateTimeField(required=False)

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(ProfileSerializer, self).to_representation(instance)

    class Meta:
        model = ViewTask
        fields = "__all__"
