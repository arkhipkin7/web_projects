import datetime

from django.test import TestCase
from ..models import Department, Employee


class TestEmployeeModel(TestCase):
    def setUp(self) -> None:
        self.departament = Department.objects.create(id=0, name='back-end dev')
        self.employee = Employee.objects.create(
            first_name='Алексей',
            second_name='Алексеевич',
            last_name='Алексеев',
            date_of_birth=datetime.date.today(),
            email='alex@test.ru',
            phone_number='+123456789',
            start_date=datetime.date.today(),
            stop_date=datetime.date.today(),
            role='Back-end',
            departament=self.departament,
        )

    def test_first_name_max_length(self):
        max_length = self.employee._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 32)

    def test_second_name_max_length(self):
        max_length = self.employee._meta.get_field('second_name').max_length
        self.assertEqual(max_length, 32)

    def test_last_name_max_length(self):
        max_length = self.employee._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 32)

    def test_date_of_birth(self):
        date = self.employee.date_of_birth
        self.assertEqual(date, datetime.date.today())

    def test_email(self):
        email = self.employee.email
        self.assertEqual(email, 'alex@test.ru')

    def test_phone_number(self):
        phone_number = self.employee.phone_number
        self.assertEqual(phone_number, '+123456789')

    def test_start_date(self):
        date = self.employee.start_date
        self.assertEqual(date, datetime.date.today())

    def test_stop_date(self):
        date = self.employee.stop_date
        self.assertEqual(date, datetime.date.today())

    def test_role(self):
        role = self.employee.role
        self.assertEqual(role, 'Back-end')

    def test_departament(self):
        departament = self.employee.departament.name
        name_departament = self.departament.name
        self.assertEqual(departament, name_departament)


class TestDepartmentModel(TestCase):
    def setUp(self) -> None:
        self.departament = Department.objects.create(id=1, name='front-end dev')

    def test_id(self):
        id = self.departament.id
        self.assertEqual(id, 1)

    def test_name_departament(self):
        name = self.departament.name
        self.assertNotEqual(name, 'back-end dev')

    def test_max_length_name(self):
        max_length = self.departament._meta.get_field('name').max_length
        self.assertEqual(max_length, 32)
