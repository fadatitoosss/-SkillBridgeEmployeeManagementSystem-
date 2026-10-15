from datetime import date
from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Employee
from employees.services.employee_service import EmployeeService

# Create your tests here.
def make_employee(**kw):
    data = dict(employee_id="E001", first_name="Thabo", last_name="Mokoena",
        email="t@example.com", phone="+27821234567", department="IT",
        job_title="Developer", employment_type="FT",
        hire_date=date(2024, 1, 1), salary=1000)
    data.update(kw)
    return Employee.objects.create(**data)

class ModelTests(TestCase):
    def test_str(self):
        self.assertIn("Thabo", str(make_employee()))
    def test_negative_salary_invalid(self):
        with self.assertRaises(ValidationError):
            make_employee(salary=-5).full_clean()

class FakeRepository:
    def get_by_id(self, pk):
        return "fake" if pk == 1 else None


class ServiceTests(SimpleTestCase):
    def test_service_uses_fake_repository(self):
        service = EmployeeService(FakeRepository())
        self.assertEqual(service.get_employee_by_id(1), "fake")

class ViewTests(TestCase):
    def test_anonymous_redirected(self):
        self.assertEqual(self.client.get(reverse("index")).status_code, 302)
    def test_logged_in_sees_list(self):
        User.objects.create_user("u", password="p")
        self.client.login(username="u", password="p")
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)