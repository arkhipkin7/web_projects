import django_filters

from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'departament': ['exact'],
            'start_date': ['exact'],
        }
