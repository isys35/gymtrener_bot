from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_bot = serializers.BooleanField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    language_code = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    date = serializers.IntegerField()
    text = serializers.CharField()
    user = UserSerializer()

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


class UpdateSerializer(serializers.Serializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer()
