from django.urls import path
from ..views import EmployeeViewSet, EmployeeDetailView, SalaryReportView


urlpatterns = [
    path('', EmployeeViewSet.as_view(), name='employee-list'),
    path('<str:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('salary-report/', SalaryReportView.as_view(), name='salary-report'),
]
