from django.contrib.auth.models import User
from django.views import View

from django.http.response import JsonResponse

from tasks.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.serializers import ModelSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework import mixins, viewsets

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, ChoiceFilter, DateFromToRangeFilter

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

class TaskFilter(FilterSet):
    priority = CharFilter(lookup_expr="iexact")
    title = CharFilter(lookup_expr="icontains")
    description = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)

class TaskHistoryFilter(FilterSet):
    date_time = DateFromToRangeFilter()
    old_status = ChoiceFilter(choices=STATUS_CHOICES)
    new_status = ChoiceFilter(choices=STATUS_CHOICES)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)

class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only = True)

    class Meta:
        model = Task
        fields = ("title","description","completed","priority","user","status",)

class TaskHistorySerializer(ModelSerializer):

    task = TaskSerializer(read_only = True)

    class Meta:
        model = TaskHistory
        fields = ("task","old_status","new_status","date_time",)


class TaskHistoryViewSet(mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet,
                        mixins.ListModelMixin
                        ):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter
    
    def get_queryset(self):
        if 'task_pk' in self.kwargs :
            look_up = self.kwargs['task_pk']
            return TaskHistory.objects.filter(task__user=self.request.user, task__deleted=False, task__id = look_up)
        else :
            return TaskHistory.objects.filter(task__user=self.request.user, task__deleted=False)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
