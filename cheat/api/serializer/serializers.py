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


class CreateViewTaskSerializer(serializers.ModelSerializer):
    begin_time = serializers.DateTimeField(required=False)
    # channel = serializers.CharField(required=False)

    class Meta:
        model = ViewTask
        fields = "__all__"

    def validate(self, attrs):

        self.user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self.user = request.user
            logger.debug(self.context["request"].user)
        return attrs

    def create(self, validated_data):
        logger.debug(validated_data)
        crt = ViewTask.objects.create(
            channel=validated_data["channel"],
            amount=validated_data["amount"],
            processed_count=validated_data["processed_count"],
            price=validated_data["price"],
            duration=validated_data["duration"],
            task_duration=validated_data["task_duration"],
            subscription=validated_data["subscription"],
            max_speed=validated_data["max_speed"],
            viewed=validated_data["viewed"],
            processed=validated_data["processed"],
            begin_time="2022-10-22T17:55",
            count_last_posts=validated_data["count_last_posts"],
            count_per_post=validated_data["count_per_post"],
            count_avg=validated_data["count_avg"],
            user=self.user,
        )
        logger.debug(validated_data)
        return True
        """ user = CustomUser.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user """


class CreateViewTaskSerializer1(serializers.ModelSerializer):
    class Meta:
        model = ViewTask
        fields = "__all__"
