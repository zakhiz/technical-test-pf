from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employees/', include('apps.employees.routes.urls')),
    path('api/positions/', include('apps.positions.routes.urls')),
]
