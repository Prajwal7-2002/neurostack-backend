from rest_framework import serializers
from .models import QueryLog, Feedback


class AskSerializer(serializers.Serializer):
    query = serializers.CharField()


class FeedbackSerializer(serializers.ModelSerializer):
    query_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'query_id', 'value', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_query_id(self, value):
        if not QueryLog.objects.filter(id=value).exists():
            raise serializers.ValidationError("query_id not found")
        return value

    def create(self, validated_data):
        qid = validated_data.pop("query_id")
        qlog = QueryLog.objects.get(id=qid)
        user = self.context["request"].user
        return Feedback.objects.create(
            query_log=qlog,
            user=user if user.is_authenticated else None,
            **validated_data
        )
