from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
class Employee(models.Model):
    """Employee model representing staff records."""
    DEPARTMENT_CHOICES = [
        ('ENG', 'Engineering'),
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('SAL', 'Sales'),
        ('OPS', 'Operations'),
        ('IT', 'Information Technology'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CT', 'Contract'),
        ('IN', 'Intern'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_regex = RegexValidator(
        regex=r'^\+27\d{9}$',
        message="Phone number must be in the format +27123456789."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Phone Number", help_text="Format: +27123456789")

    # Employment Details
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID", help_text="Enter your unique Employee ID" )
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, verbose_name="Department", help_text=" Select your department")
    job_title = models.CharField(max_length=50, verbose_name="Job Title", help_text="Enter your job title")
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES, default='FT', verbose_name="Employment Type", help_text="Select your employment type")
    hire_date = models.DateField(verbose_name="Hire Date", help_text="Select your hire date")
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Salary")

    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active Employee")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_employees')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def years_of_service(self):
        return (date.today() - self.hire_date).days // 365

    def clean(self):
        if self.hire_date and self.hire_date > date.today():
            raise ValidationError({"hire_date": "Hire date cannot be in the future."})