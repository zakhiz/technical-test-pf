from django.urls import path
from ..views import PositionViewSet, PositionDetailView


urlpatterns = [
    path('', PositionViewSet.as_view(), name='position-list'),
    path('<str:pk>/', PositionDetailView.as_view(), name='position-detail'),
]
