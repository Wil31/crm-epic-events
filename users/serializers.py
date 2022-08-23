from rest_framework import serializers

from .models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "user_type", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            user_type=validated_data["user_type"],
        )
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.user_type = validated_data.get("user_type", instance.user_type)
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        instance.set_password(password)
        instance.save()
        return instance
