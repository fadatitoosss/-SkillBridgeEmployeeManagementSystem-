from typing import List, Optional
from django.db.models import Q, Count
from employees.models import Employee


class EmployeeRepository:
    @property
    def model(self):
        from employees.models import Employee
        return Employee

    def get_all(self) -> List:
        return self.model.objects.select_related('created_by').all()

    def get_by_id(self, pk: int):
        try:
            return self.model.objects.select_related('created_by').get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def search(self, query: str) -> List:
        return self.model.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query)
        )

    def filter(self, department: str = None, is_active: bool = None) -> List:
        qs = self.model.objects.all()
        if department:
            qs = qs.filter(department=department)
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
        return qs

    def create(self, data: dict):
        return self.model.objects.create(**data)

    def update(self, pk: int, data: dict):
        self.model.objects.filter(pk=pk).update(**data)
        return self.get_by_id(pk)

    def delete(self, pk: int) -> bool:
        deleted, _ = self.model.objects.filter(pk=pk).delete()
        return deleted > 0

    def email_exists(self, email: str, exclude_id: int = None) -> bool:
        qs = self.model.objects.filter(email__iexact=email)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()

    def employee_id_exists(self, employee_id: str, exclude_id: int = None) -> bool:
        qs = self.model.objects.filter(employee_id__iexact=employee_id)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()

    def count(self, **filters) -> int:
        return self.model.objects.filter(**filters).count()

    def count_by_department(self) -> dict:
        return dict(
            self.model.objects.values('department')
            .annotate(count=Count('id'))
            .values_list('department', 'count')
        )
    def get_card_statistics(self):
        return Employee.objects.aggregate(
        total=Count("id"),
        active=Count("id", filter=Q(is_active=True)),
        inactive=Count("id", filter=Q(is_active=False)),
        full_time=Count("id", filter=Q(employment_type="FT")),
    )
