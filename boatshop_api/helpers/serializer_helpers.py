from rest_framework import serializers


class UserSerializerHelper:

    def validate(self, data):
        password = data.get("password", None)
        password_confirm = data.get("password_confirm", None)
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Password confirm must be the same as password"}
            )
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance.first_name = validated_data.pop("first_name", instance.first_name)
        instance.last_name = validated_data.pop("last_name", instance.last_name)
        instance.email = validated_data.pop("email", instance.email)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
