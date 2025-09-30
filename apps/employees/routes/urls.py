from django.urls import path
from ..views import EmployeeViewSet, EmployeeDetailView


urlpatterns = [
    path('', EmployeeViewSet.as_view(), name='employee-list'),
    path('<str:pk>', EmployeeDetailView.as_view(), name='employee-detail'),
]
