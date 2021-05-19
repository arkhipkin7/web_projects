from django.urls import path
from django.contrib.auth import views
from .views import ProductListView, ParserView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('parser/', ParserView.as_view(), name='parser'),
    path('products/<int:pk>/', ProductListView.as_view(), name='list_product'),
]
