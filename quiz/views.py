# quiz/views.py
from django.db import transaction
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Question, Subject, TestAttempt, TestAnswer
from .serializers import (
    QuestionListSerializer,
    SubmitTestSerializer,
    SubmitResultSerializer,
)


class QuestionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionListSerializer

    def get_queryset(self):
        qs = Question.objects.select_related("subject").all()

        grade = self.request.query_params.get("grade")
        subject_id = self.request.query_params.get("subject_id")
        subject_name = self.request.query_params.get("subject")

        # grade bo'lsa filter, bo'lmasa filter qilmaydi
        if grade:
            qs = qs.filter(grade=int(grade))

        if subject_id:
            qs = qs.filter(subject_id=int(subject_id))
        if subject_name:
            qs = qs.filter(subject__name__iexact=subject_name)

        return qs


class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        ser = SubmitTestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = request.user
        grade = user.grade

        subject = None
        subject_id = ser.validated_data.get("subject_id")
        if subject_id:
            subject = Subject.objects.filter(id=subject_id).first()

        answers = ser.validated_data["answers"]
        q_ids = [a["question_id"] for a in answers]

        # Faqat user sinfiga mos savollar qabul qilinadi
        qs = Question.objects.select_related("subject").filter(id__in=q_ids, grade=grade)
        if subject:
            qs = qs.filter(subject=subject)

        q_map = {q.id: q for q in qs}

        correct = 0
        wrong = 0

        attempt = TestAttempt.objects.create(
            user=user,
            grade=grade,
            subject=subject,
            total=0,
            correct=0,
            wrong=0,
        )

        for item in answers:
            qid = item["question_id"]
            selected = item["selected"]

            q = q_map.get(qid)
            if not q:
                continue

            is_ok = (selected == q.correct)
            if is_ok:
                correct += 1
            else:
                wrong += 1

            TestAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected=selected,
                is_correct=is_ok,
            )

        total = correct + wrong
        attempt.total = total
        attempt.correct = correct
        attempt.wrong = wrong
        attempt.save(update_fields=["total", "correct", "wrong"])

        return Response(
            {
                "attempt": SubmitResultSerializer(attempt).data,
                "message": "Natija saqlandi",
            },
            status=status.HTTP_200_OK,
        )

from django.db.models import F

class LeaderboardTop10View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        grade = request.query_params.get("grade")
        subject_id = request.query_params.get("subject_id")

        qs = TestAttempt.objects.select_related("user", "subject").all()

        if grade:
            qs = qs.filter(grade=int(grade))
        if subject_id:
            qs = qs.filter(subject_id=int(subject_id))

        # Ranking qoidasi: correct DESC, duration ASC, created_at ASC
        qs = qs.order_by("-correct", "duration_seconds", "created_at")

        top = qs[:10]

        data = [
            {
                "user_id": a.user_id,
                "username": a.user.username,
                "correct": a.correct,
                "total": a.total,
                "duration_seconds": a.duration_seconds,
                "created_at": a.created_at,
            }
            for a in top
        ]
        return Response({"top10": data})


class MyRankView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        grade = request.query_params.get("grade")
        subject_id = request.query_params.get("subject_id")

        qs = TestAttempt.objects.select_related("user").all()

        # default: user sinfi
        if grade:
            qs = qs.filter(grade=int(grade))
        else:
            qs = qs.filter(grade=user.grade)

        if subject_id:
            qs = qs.filter(subject_id=int(subject_id))

        qs = qs.order_by("-correct", "duration_seconds", "created_at")

        # userning eng oxirgi attemptini rank qilamiz (xohlasangiz eng yaxshisini ham qilamiz)
        my_attempt = (
            TestAttempt.objects.filter(user=user)
            .order_by("-id")
            .first()
        )
        if not my_attempt:
            return Response({"rank": None, "message": "Sizda hali natija yo‘q"}, status=200)

        # shu filtrga mos bo‘lsin
        if grade and my_attempt.grade != int(grade):
            return Response({"rank": None, "message": "Bu sinf bo‘yicha sizda natija yo‘q"}, status=200)
        if subject_id and (my_attempt.subject_id != int(subject_id)):
            return Response({"rank": None, "message": "Bu fan bo‘yicha sizda natija yo‘q"}, status=200)

        # rank hisoblash (1-based)
        ids = list(qs.values_list("id", flat=True))
        try:
            rank = ids.index(my_attempt.id) + 1
        except ValueError:
            rank = None

        return Response({
            "rank": rank,
            "attempt": {
                "id": my_attempt.id,
                "correct": my_attempt.correct,
                "wrong": my_attempt.wrong,
                "total": my_attempt.total,
                "duration_seconds": my_attempt.duration_seconds,
            }
        })
