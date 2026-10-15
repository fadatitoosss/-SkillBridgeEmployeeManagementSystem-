from typing import List, Optional
from django.core.cache import cache
from employees.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    CACHE_KEY_ALL = 'employees:all'
    CACHE_KEY_STATS = 'employees:stats'
    CACHE_TIMEOUT = 300

    def __init__(self, repository: EmployeeRepository = None):
        self.repository = repository or EmployeeRepository()

    def get_all_employees(self) -> List:
        cached = cache.get(self.CACHE_KEY_ALL)
        if cached is not None:
            return cached
        employees = list(self.repository.get_all())
        cache.set(self.CACHE_KEY_ALL, employees, self.CACHE_TIMEOUT)
        return employees

    def get_employee_by_id(self, pk: int):
        return self.repository.get_by_id(pk)

    def search_employees(self, query: str) -> List:
        if not query or len(query) < 2:
            return self.get_all_employees()
        return list(self.repository.search(query))

    def filter_employees(self, department: str = None, is_active: bool = None) -> List:
        return list(self.repository.filter(department=department, is_active=is_active))

    def create_employee(self, data: dict):
        if self.repository.email_exists(data.get('email')):
            raise ValueError("An employee with this email already exists.")
        if self.repository.employee_id_exists(data.get('employee_id')):
            raise ValueError("This employee ID is already in use.")
        employee = self.repository.create(data)
        self._invalidate_cache()
        return employee

    def update_employee(self, pk: int, data: dict):
        if not self.repository.get_by_id(pk):
            raise ValueError(f"Employee with ID {pk} not found.")
        new_email = data.get('email')
        if new_email and self.repository.email_exists(new_email, exclude_id=pk):
            raise ValueError("An employee with this email already exists.")
        updated = self.repository.update(pk, data)
        self._invalidate_cache()
        return updated

    def delete_employee(self, pk: int) -> bool:
        result = self.repository.delete(pk)
        self._invalidate_cache()
        return result

    def get_statistics(self) -> dict:
        cached = cache.get(self.CACHE_KEY_STATS)
        if cached is not None:
            return cached
        stats = {
            'total': self.repository.count(),
            'active': self.repository.count(is_active=True),
            'inactive': self.repository.count(is_active=False),
            'by_department': self.repository.count_by_department(),
        }
        cache.set(self.CACHE_KEY_STATS, stats, self.CACHE_TIMEOUT)
        return stats

    def _invalidate_cache(self):
        cache.delete(self.CACHE_KEY_ALL)
        cache.delete(self.CACHE_KEY_STATS)

    def get_all_employees(self):
        return self.repository.get_all()

    def get_card_statistics(self):
        stats = cache.get('card_stats')
        if stats is None:
            stats = self.repository.get_card_statistics()
            cache.set('card_stats', stats, 300)
        return stats
