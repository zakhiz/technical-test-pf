from django.urls import path
from ..views import (
    TaskViewSet,
    TaskDetailView,
    TaskStatusUpdateView
)

urlpatterns = [
    path('', TaskViewSet.as_view(), name='task-list'),
    path('<str:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('<str:pk>/status/', TaskStatusUpdateView.as_view(),
         name='task-status-update'),
]
