from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializerHelper:
    def validate(self, data):
        password = data.get("password", None)
        password_confirm = data.get("password_confirm", None)
        if not password or not password_confirm:
            raise serializers.ValidationError(
                {"password": "Password is required"}
            )
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Password confirm must be the same as password"}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)
        designation = validated_data.pop("designation", None)
        validated_data['username'] = validated_data.get('email')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
