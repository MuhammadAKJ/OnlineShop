from django.urls import path
from .views import ProductListApiView

app_name = 'api'

urlpatterns = [
    path('api', ProductListApiView.as_view()),
]