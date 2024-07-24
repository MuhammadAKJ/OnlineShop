from django.urls import path
from .views import ProductListApiView, ProductDetailApiView

app_name = 'api'

urlpatterns = [
    path('product-list/', ProductListApiView.as_view()),
    path('detail/<str:name>/<slug:slug>/', ProductDetailApiView.as_view()),

]
