# quiz/serializers.py
from rest_framework import serializers
from .models import Subject, Question, TestAttempt


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class QuestionListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Question
        fields = [
            "id",
            "grade",
            "subject",
            "text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "created_at",
        ]


class SubmitAnswerItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected = serializers.ChoiceField(choices=["A", "B", "C", "D"])


class SubmitTestSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField(required=False)
    duration_seconds = serializers.IntegerField(required=False, min_value=0)  # ✅ qo‘shildi
    answers = SubmitAnswerItemSerializer(many=True)



class SubmitResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = ["id", "grade", "subject", "total", "correct", "wrong", "created_at"]

class LeaderboardItemSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    correct = serializers.IntegerField()
    total = serializers.IntegerField()
    duration_seconds = serializers.IntegerField()
    created_at = serializers.DateTimeField()
