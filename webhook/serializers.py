from typing import Any

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_bot = serializers.BooleanField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(default=None)
    username = serializers.CharField()
    language_code = serializers.CharField(default=None)


class InlineKeyboardSerializer(serializers.Serializer):
    text = serializers.CharField()
    callback_data = serializers.CharField()


class ReplyMarkUpSerializer(serializers.Serializer):
    inline_keyboard = serializers.ListField(
        child=serializers.ListField(
            child=InlineKeyboardSerializer(
            )
        )
    )


class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    date = serializers.IntegerField()
    text = serializers.CharField()
    user = UserSerializer()
    reply_markup = ReplyMarkUpSerializer(default=None)

    def to_internal_value(self, data):
        if data['from']:
            data['user'] = data['from']
        return super(MessageSerializer, self).to_internal_value(data)


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    type = serializers.CharField()


class CallBackQuerySeriaizer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    message = MessageSerializer()
    chat_instance = serializers.IntegerField()
    data = serializers.CharField()  # type: ignore

    def to_internal_value(self, data):
        if data['from']:
            data['user'] = data['from']
        return super(CallBackQuerySeriaizer, self).to_internal_value(data)


class UpdateSerializer(serializers.Serializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer(default=None)
    callback_query = CallBackQuerySeriaizer(default=None)
