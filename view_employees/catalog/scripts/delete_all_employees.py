from ..models import Employee


def run(*args):
    employees = Employee.objects.all()
    employees.delete()
