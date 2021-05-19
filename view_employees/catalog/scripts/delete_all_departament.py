from ..models import Department


def run(*args):
    departaments = Department.objects.all()
    departaments.delete()
