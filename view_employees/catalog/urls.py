from django.urls import path
from django.views.generic import TemplateView
from .views import EmployeesView, EmployeeDetailView, EmployeesAlphabetView


urlpatterns = [
    path('', TemplateView.as_view(template_name='catalog/base.html'), name='home'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('alphabetical_list/', EmployeesAlphabetView.as_view(), name='alphabetical-list'),
]
