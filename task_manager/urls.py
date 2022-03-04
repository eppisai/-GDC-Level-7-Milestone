from django.contrib import admin
from django.urls import path

from tasks.views import *

from tasks.apiviews import *

from django.contrib.auth.views import LogoutView

from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = routers.SimpleRouter()

router.register(r"api/task",TaskViewSet)

history_router = routers.NestedSimpleRouter(router, r'api/task', lookup='task')
history_router.register(r'history', TaskHistoryViewSet)

router.register("api/history",TaskHistoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', GenericTaskView.as_view()),

    #user management
    path('user/login', UserLoginView.as_view()),
    path('user/signup', UserCreateView.as_view()),
    path('user/logout', LogoutView.as_view()),
    
    #tasks
    path('tasks',GenericTaskView.as_view()),
    path('create-task', GenericTaskCreateView.as_view()),
    path('update-task/<pk>', GenericTaskUpdateView.as_view()),

    path('delete-task/<pk>', GenericTaskDeleteView.as_view()),
] + router.urls + history_router.urls

'''
    path('tasks',GenericTaskView.as_view()),
    path('create-task', GenericTaskCreateView.as_view()),

    path('user/signup', UserCreateView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('user/logout', LogoutView.as_view()),

    path('update-task/<pk>', GenericTaskUpdateView.as_view()),
    path('detail-task/<pk>', GenericTaskDetailView.as_view()),
    path('delete-task/<pk>', GenericTaskDeleteView.as_view()),
    path('add-task', add_task_view),
    #path("delete-task/<int:index>", delete_task_view),
    path('sessiontest', session_storage_view),
    path("complete_task/<int:index>", complete_task_view),
    path("completed_tasks", completed_tasks_view),
    path("all_tasks", all_tasks_view)
'''