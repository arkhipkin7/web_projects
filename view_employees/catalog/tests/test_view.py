import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import Department, Employee

STATUS_CODE_OK = 200
STATUS_CODE_NOT_FOUND = 404


class EmployeeDetailModelTests(TestCase):
    def setUp(self) -> None:
        self.departament = Department.objects.create(id=0, name='back-end dev')
        self.employee = Employee.objects.create(
            id=4,
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

    def test_view_url_employees(self) -> None:
        resp = self.client.get(f'/employee/{self.employee.id}/')
        self.assertEqual(resp.status_code, STATUS_CODE_OK)

    def test_view_url_employee_detail(self) -> None:
        resp = self.client.get(reverse('employee-detail', args=[str(self.employee.id)]))
        self.assertEqual(resp.status_code, STATUS_CODE_OK)

    def test_view_use_correct_template(self) -> None:
        resp = self.client.get(reverse('employee-detail', args=[str(self.employee.id)]))
        self.assertEqual(resp.status_code, STATUS_CODE_OK)
        self.assertTemplateUsed(resp, 'catalog/employee_detail.html')

    def test_view_if_id_is_out_of_range(self) -> None:
        resp = self.client.get(f'/employees/{self.employee.id + 7}/')
        self.assertEqual(resp.status_code, STATUS_CODE_NOT_FOUND)
